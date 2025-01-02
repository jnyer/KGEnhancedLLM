import json
import docx  # python-docx

def docx_to_json(docx_path, json_path):
    # 1. 读取 docx 文件
    document = docx.Document(docx_path)
    
    # 2. 将每个段落的文本保存到一个列表中
    paragraphs = []
    seen = set()
    for paragraph in document.paragraphs:
        text = paragraph.text.strip()
        # 如果段落不为空，就加到列表中
        if text:
            if text not in seen:
                seen.add(text)
                paragraph_obj = {
                    "name": text
                }
                paragraphs.append(paragraph_obj)

    # 3. 将列表转换为 JSON 字符串
    # ensure_ascii=False 保证中文不会被转义为 Unicode
    paragraphs_json = json.dumps(paragraphs, ensure_ascii=False, indent=4)

    # 4. 将 JSON 字符串写入到文件
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(paragraphs_json)
    
    print(f"成功将 {docx_path} 转换为 JSON，并保存到 {json_path}")

if __name__ == "__main__":
    # 举例：将 sample.docx 转换为 output.json
    docx_to_json("/Users/jny/Downloads/北京市.docx", "colleges_university.json")
