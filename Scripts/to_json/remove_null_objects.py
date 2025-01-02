import json

def remove_null_objects(input_file, output_file):
    # 从文件中读取数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 确保 data 是列表
    if not isinstance(data, list):
        raise ValueError("JSON 文件的顶层结构不是列表。")

    # 过滤掉 name 为 "NULL" 的对象
    filtered_data = [obj for obj in data if obj.get('brief_info') != '']

    # 写回文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # 根据需要修改文件路径
    input_file = "output.json"
    output_file = "output2.json"
    remove_null_objects(input_file, output_file)
