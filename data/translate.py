import os
import json
from lht.api import AI

# ============== 配置 ==============
DATA_DIR = "./"
ai = AI(model="hunyuan-turbos-latest", max_workers=4)

def translate_summary_batch(texts):
    """批量翻译摘要
    输入: 英文摘要字符串列表
    输出: 中文翻译字符串列表（顺序对应）
    """
    try:
        return ai.batch_process(
            texts,
            system_prompt="请将以下英文论文摘要准确翻译成中文，不要引入额外说明。",
            max_workers=8
        )
    except Exception as e:
        print("翻译请求失败:", e)
        return None

def process_file(filepath):
    print(f"处理文件: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 收集需要翻译的摘要和对应索引
    to_translate = []
    translate_indices = []
    for i, paper in enumerate(data):
        if "summary_zh" not in paper and "summary" in paper:
            to_translate.append(paper["summary"])
            translate_indices.append(i)

    if not to_translate:
        print("无需要更新的内容")
        return

    # 批量翻译
    translated = translate_summary_batch(to_translate)
    if not translated:
        print("✗ 翻译失败")
        return

    # 更新数据
    updated = False
    for idx, zh in zip(translate_indices, translated):
        if zh:
            data[idx]["summary_zh"] = zh.strip()
            updated = True
            print(f"✓ 翻译成功: {data[idx]['title'][:40]}...")

    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✔ 文件已更新: {filepath}")

def main():
    for fname in os.listdir(DATA_DIR):
        if fname.endswith(".json"):
            process_file(os.path.join(DATA_DIR, fname))

if __name__ == "__main__":
    main()
