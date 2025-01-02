import json

def remove_state_field(obj):
    if isinstance(obj, dict):
        # 如果字典中有 "State" 字段则删除
        if "initial" in obj:
            del obj["initial"]
        # if "website" in obj:
        #     del obj["website"]
        # if "email" in obj:
        #     del obj["email"]
        # if "birthmonth" in obj:
        #     del obj["birthmonth"]
        # 对字典中所有值进行递归处理
        for key, value in obj.items():
            obj[key] = remove_state_field(value)
        return obj
    elif isinstance(obj, list):
        # 如果是列表，则对列表中的每个元素进行递归处理
        return [remove_state_field(item) for item in obj]
    else:
        # 如果既不是列表也不是字典，直接返回值
        return obj

if __name__ == "__main__":
    input_file = "output6.json"   # 你的输入文件名
    output_file = "output7.json" # 输出文件名

    # 从输入文件中读取数据
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 移除所有对象的 State 字段
    data = remove_state_field(data)

    # 将处理后的数据写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)