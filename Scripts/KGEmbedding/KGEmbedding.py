import logging
import os
import sys
import yaml
import torch
import csv
from pykeen.pipeline import pipeline
from pykeen.triples import TriplesFactory

# ============================
# 函数定义
# ============================

def load_config(config_path: str):
    """
    加载 YAML 配置文件。
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config

def setup_logging(log_file: str):
    """
    配置日志记录，将日志输出到指定文件和控制台。
    确保日志文件所在的目录存在。
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
        # 临时配置，以记录日志目录创建信息到控制台
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout)
            ]
        )
        logging.info(f"已创建日志文件目录: {log_dir}")
        # 重新配置日志以包含文件处理器
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(log_file, mode='w', encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def ensure_directory(directory_path: str):
    """
    确保给定目录路径存在，如果不存在则创建。
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        logging.info(f"已创建目录: {directory_path}")

def split_triples(triples_factory: TriplesFactory, train_ratio: float, validation_ratio: float, test_ratio: float):
    """
    将 TriplesFactory 分割为训练集、验证集和测试集。
    """
    training, testing, validation = triples_factory.split([train_ratio, test_ratio, validation_ratio])
    return training, testing, validation

def save_metrics(metrics: dict, save_path: str):
    """
    将评估指标保存到 CSV 文件中。
    """
    with open(save_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Metric', 'Value'])
        for metric, value in metrics.items():
            writer.writerow([metric, value])

def main():
    try:
        # 加载配置
        config = load_config('/home/workspace/jnyao/Scripts/KGEmbedding/config.yaml')  # 请替换为实际配置文件路径

        # 配置日志
        setup_logging(config['logging']['log_file'])
        logger = logging.getLogger()

        logger.info("启动知识图谱嵌入训练脚本。")

        # 检查设备
        if torch.cuda.is_available():
            devices = config['device']['devices']
            device = devices if isinstance(devices, str) else 'cuda'
            logger.info(f"使用的设备: {device}")
        else:
            device = 'cpu'
            logger.info("未检测到GPU，使用CPU进行训练。")

        # 加载并划分数据集
        logger.info("开始加载数据集。")
        triples_factory = TriplesFactory.from_path(config['data']['file_path'])
        training, testing, validation = split_triples(
            triples_factory,
            train_ratio=config['dataset_split']['train'],
            validation_ratio=config['dataset_split']['validation'],
            test_ratio=config['dataset_split']['test']
        )
        logger.info("已成功加载并划分数据集。")
        logger.info(f"训练集三元组数: {training.num_triples}")
        logger.info(f"验证集三元组数: {validation.num_triples}")
        logger.info(f"测试集三元组数: {testing.num_triples}")

        # 确保模型保存路径的目录存在
        model_save_dir = config['model']['save_dir']
        if model_save_dir:
            ensure_directory(model_save_dir)

        # 使用 PyKEEN 的 Pipeline API
        logger.info("开始执行 PyKEEN 的 Pipeline。")
        result = pipeline(
            training=training,
            validation=validation,
            testing=testing,
            model=config['model']['model_name'],
            model_kwargs={
                'embedding_dim': config['model']['embedding_dim'],
                'scoring_fct_norm': config['model']['scoring_fct_norm']
            },
            optimizer='adam',
            optimizer_kwargs={
                'lr': config['training']['learning_rate']
            },
            
            device=device,
            random_seed=42,
            result_tracker='csv',
            # 移除 result_tracker_kwargs，因为 'csv' 结果跟踪器不接受 'path' 或 'filename'
            use_tqdm=True
        )
        logger.info("训练和评估完成。")
        logger.info(f"评估结果: {result.metric_results}")

        # 手动保存评估指标到 CSV 文件
        metrics_save_path = os.path.join(config['model']['save_dir'], 'metrics.csv')
        save_metrics(result.metric_results, metrics_save_path)
        logger.info(f"评估结果已保存至: {metrics_save_path}")

        # 保存模型（可选）
        # PyKEEN 的 Pipeline API 会自动保存模型和结果到指定的输出目录
        # 如果需要手动保存特定模型参数，可以使用以下代码：
        # model = result.model
        # model.save_to_file(os.path.join(model_save_dir, 'model.pt'))

        logger.info(f"训练结果已保存至目录: {model_save_dir}")

    except Exception as e:
        logging.exception("在训练过程中发生未捕获的异常。")
        sys.exit(1)

if __name__ == '__main__':
    main()
