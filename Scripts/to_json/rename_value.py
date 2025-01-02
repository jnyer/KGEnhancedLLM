import json

def transform_values(obj):
    if isinstance(obj, dict):
        # 对字典中每一个键值对进行处理
        for key, value in obj.items():
            if key == "性别":
                # 值替换逻辑
                if value == "1":
                    obj[key] = "男"
                elif value == "0":
                    obj[key] = "女"
            else:
                # 对子元素递归处理
                transform_values(value)
    elif isinstance(obj, list):
        # 对列表中每个元素递归处理
        for i, item in enumerate(obj):
            transform_values(item)
    # 如果是其他类型(字符串、数字等)，不做处理直接返回
    return obj

if __name__ == "__main__":
    input_file = "output3.json"
    output_file = "output3.json"

    # 从输入文件中读取数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 执行值替换
    data = transform_values(data)

    # 将处理结果写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)