import json

def filter_and_rename_fields(obj, field_map):
    """
    递归处理对象：
    - 如果是字典类型（object），则只保留 field_map 中指定的字段并进行重命名
    - 如果是列表类型（array），则对列表中的每个元素进行同样的处理
    - 其他类型原样返回
    """
    if isinstance(obj, dict):
        new_obj = {}
        for old_field, new_field in field_map.items():
            if old_field in obj:
                # 递归处理该字段的值
                new_obj[new_field] = filter_and_rename_fields(obj[old_field], field_map)
        return new_obj
    elif isinstance(obj, list):
        return [filter_and_rename_fields(item, field_map) for item in obj]
    else:
        return obj

if __name__ == "__main__":
    # 定义需要保留和重命名的字段映射
    # 格式：{旧字段名: 新字段名, ...}
    field_map = {
        "brief_info": "人物概要介绍",
        "table_content": "人物基础信息",
        "name": "姓名",
        "sex": "性别",
        "nation": "民族",
        "birthday": "生日",
        "birthplace": "出生地",
        "job": "工作",
        # 这里可以继续增加需要保留和重命名的字段
    }
    
    input_file = "output2.json"
    output_file = "output3.json"

    # 从输入文件中读取数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 对数据进行保留、重命名处理
    filtered_data = filter_and_rename_fields(data, field_map)

    # 将处理后的数据写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)