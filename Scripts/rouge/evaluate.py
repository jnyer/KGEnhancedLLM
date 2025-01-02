import json
from rouge_score import rouge_scorer
import pandas as pd
import numpy as np
import sys

def load_json(file_path):
    """
    加载 JSON 文件。
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def compute_rouge_l(pred, ref):
    """
    计算 ROUGE-L 分数。
    """
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(ref, pred)
    return score['rougeL'].fmeasure  # 返回 F1 分数

def preprocess_field(value):
    """
    预处理字段值，将列表转换为字符串，保留字符串不变。
    """
    if isinstance(value, list):
        return ', '.join(map(str, value))
    elif isinstance(value, str):
        return value
    else:
        return str(value)

def evaluate_json_lists(pred_list, ref_list):
    """
    对比两个 JSON 对象列表，计算每个字段的 ROUGE-L 分数，并计算综合相似性得分。
    """
    if len(pred_list) != len(ref_list):
        print("警告：预测列表和参考列表的长度不一致。将以较短的列表长度为准。")
    
    min_length = min(len(pred_list), len(ref_list))
    evaluation_results = []
    
    for idx in range(min_length):
        pred_obj = pred_list[idx]
        ref_obj = ref_list[idx]
        obj_result = {'object_index': idx}
        
        # 获取所有字段
        all_fields = set(pred_obj.keys()).union(set(ref_obj.keys()))
        
        field_scores = []
        
        for field in all_fields:
            pred_val = preprocess_field(pred_obj.get(field, ""))
            ref_val = preprocess_field(ref_obj.get(field, ""))
            
            # 仅对非空字符串字段计算 ROUGE-L
            if isinstance(pred_val, str) and isinstance(ref_val, str) and pred_val.strip() and ref_val.strip():
                rouge_l = compute_rouge_l(pred_val, ref_val)
            else:
                rouge_l = np.nan  # 使用 NaN 表示未计算的字段
            
            obj_result[field] = rouge_l
            field_scores.append(rouge_l)
        
        # 计算该对象的平均 ROUGE-L 分数，忽略 NaN
        avg_rouge_l = np.nanmean(field_scores)
        obj_result['average_rougeL'] = avg_rouge_l
        
        evaluation_results.append(obj_result)
    
    # 创建 DataFrame
    df = pd.DataFrame(evaluation_results)
    
    # 计算所有对象的综合平均 ROUGE-L 分数
    overall_average = df['average_rougeL'].mean()
    
    return df, overall_average

def main(pred_file, ref_file, output_file='evaluation_results.csv'):
    # 加载 JSON 文件
    try:
        pred_json = load_json(pred_file)
        ref_json = load_json(ref_file)
    except Exception as e:
        print(f"Error loading JSON files: {e}")
        sys.exit(1)
    
    # 检查是否为列表
    if not isinstance(pred_json, list) or not isinstance(ref_json, list):
        print("Error: 两个 JSON 文件应包含 JSON 对象的列表。")
        sys.exit(1)
    
    # 评估
    df, overall_avg = evaluate_json_lists(pred_json, ref_json)
    
    # 显示结果
    pd.set_option('display.max_columns', None)  # 显示所有列
    print(df)
    print(f"\n综合 ROUGE-L 相似性得分（所有对象平均）：{overall_avg:.4f}")
    
    # 保存结果
    df.to_csv(output_file, index=False)
    print(f"评估结果已保存到 {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='使用 ROUGE-L 对两个 JSON 列表进行相似性评估。')
    parser.add_argument('pred_file', type=str, help='预测 JSON 文件路径')
    parser.add_argument('ref_file', type=str, help='参考 JSON 文件路径')
    parser.add_argument('--output', type=str, default='evaluation_results.csv', help='输出 CSV 文件路径')

    args = parser.parse_args()

    main(args.pred_file, args.ref_file, args.output)
