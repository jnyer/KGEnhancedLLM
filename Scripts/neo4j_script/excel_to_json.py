import pandas as pd
import json

# 读取 Excel 文件
df = pd.read_excel("/Users/jny/Downloads/test.xlsx")  # 如果有多个 sheet，可加参数 sheet_name="Sheet1"

# 创建一个空的列表来存储结果
result_list = []

# 遍历数据行
for index, row in df.iterrows():
    # 提取相应的列（这里假设列名为“学校名称”和“所在地”）
    university = row["学校名称"]
    level = row["办学层次"]
    
    # 组装成你需要的字典格式
    item = {
        "university": str(university).strip(),
        "level": str(level).strip()
    }
    result_list.append(item)

# 查看结果
# print(result_list)

# 如果需要保存为 JSON 文件
with open("output2.json", "w", encoding="utf-8") as f:
    json.dump(result_list, f, ensure_ascii=False, indent=4)
