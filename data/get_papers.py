import arxiv  # pip install arxiv
import datetime
import json

def fetch_papers(keyword, date_from, date_to, max_results=100):
    """
    抓取 arXiv 上符合关键词与日期范围的论文，并返回列表字典。
    """
    # 构造查询，同时筛选摘要与标题中包含关键词
    query = f'all:{keyword}'
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )

    results = []
    for result in search.results():
        pub_date = result.published.date()
        if date_from <= pub_date <= date_to:
            results.append({
                "title": result.title,
                "summary": result.summary,
                "link": result.entry_id,
                "published": result.published.isoformat()
            })
    return results

def save_to_json(papers, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    keyword = input("请输入关键词: ").strip()
    d1 = input("请输入起始日期 (YYYY-MM-DD): ").strip()
    d2 = input("请输入结束日期 (YYYY-MM-DD): ").strip()
    date_from = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    date_to = datetime.datetime.strptime(d2, "%Y-%m-%d").date()

    papers = fetch_papers(keyword, date_from, date_to, max_results=200)
    print(f"共抓取到 {len(papers)} 篇论文")

    output = f"{keyword}_{d1}_{d2}.json"
    save_to_json(papers, output)
    print(f"已保存到文件：{output}")
