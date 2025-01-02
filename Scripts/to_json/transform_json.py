import json

def transform_json(source_data):
    # 检查 source_data 是字典还是列表
    if isinstance(source_data, list):
        # 如果是列表，则对每个元素进行转换
        return [transform_single_json(item) for item in source_data]
    elif isinstance(source_data, dict):
        # 如果是字典，则直接转换
        return transform_single_json(source_data)
    else:
        raise TypeError("源 JSON 数据必须是字典或字典列表。")
    
def transform_single_json(source_data):
    # 抽取字段
    brief_info = source_data.get("人物概要介绍","")
    table_info = source_data.get("人物基础信息","")
    name = source_data.get("姓名", "")
    sex = source_data.get("性别", "")
    nation = source_data.get("民族", "")
    birthday = source_data.get("生日", "")
    birthplace = source_data.get("出生地", "")
    job = source_data.get("工作", "")

    # 构建目标 JSON 结构
    target_data = {
        "instruction": "使用给定的JSON格式，从输入的人物概要介绍和人物基础信息中抽取出指定的人物属性信息。你的回复除了给定格式的JSON字符串外，不应包含其他内容。\n按以下JSON格式进行回复：\n{\"姓名\":\"\",\"性别\":\"\",\"民族\":\"\",\"生日\":\"\",\"出生地\":\"\",\"工作\":\"\",}\n请注意，如果从文本中你无法抽取出对应的人物属性，那就把 JSON 字符串中的这一项属性赋值为 \"NULL\" \n人物属性信息包括：\n1.姓名\n2.性别\n3.民族：在56个候选民族中匹配一个：包括汉族、蒙古族、回族、藏族、维吾尔族、苗族、彝族、壮族、布依族、朝鲜族、满族、侗族、瑶族、白族、土家族、哈尼族、哈萨克族、傣族、黎族、傈僳族、佤族、畲族、拉祜族、水族、东乡族、纳西族、景颇族、柯尔克孜族、土族、达斡尔族、仫佬族、羌族、布朗族、撒拉族、毛南族、仡佬族、锡伯族、阿昌族、普米族、塔吉克族、怒族、乌孜别克族、俄罗斯族、鄂温克族、德昂族、保安族、裕固族、京族、塔塔尔族、独龙族、鄂伦春族、赫哲族、门巴族、珞巴族、基诺族、高山族\n4.生日：指人物的出生年份\n5.出生地：指人物的出生地点\n6.工作：指人物曾经担任或现在正在担任的职务\n",
        "input": f'{{"人物概要介绍":"{brief_info}","人物基础信息":"{table_info}"}}\n',
        "output": f'{{"姓名":"{name}","性别":"{sex}","民族":"{nation}","生日":"{birthday}","出生地":"{birthplace}","工作":"{job}"}}\n'
    }
    return target_data

def main():
    # 读取源 JSON 文件
    with open('output3.json', 'r', encoding='utf-8') as f:
        source_json = json.load(f)
    
    # 转换 JSON 结构
    target_json = transform_json(source_json)
    
    # 写入目标 JSON 文件
    with open('target.json', 'w', encoding='utf-8') as f:
        json.dump(target_json, f, ensure_ascii=False, indent=4)
    
    print("JSON 转换完成，已保存为 target.json")

if __name__ == "__main__":
    main()
