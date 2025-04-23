import os
import json
import traceback
from scholarly import scholarly

def main():
    print("📘 Starting Google Scholar data fetcher...")

    # 获取 Scholar ID
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")
    if not scholar_id:
        print("❌ Environment variable GOOGLE_SCHOLAR_ID not found.")
        return

    print(f"🔍 Fetching data for Google Scholar ID: {scholar_id}")

    try:
        # 查找作者信息
        author = scholarly.search_author_id(scholar_id)
        results = scholarly.fill(author)

        # 提取引用信息
        cited_by = results.get("cited_by", {})
        total_citations = cited_by.get("total", 0)
        h_index = cited_by.get("h_index", {}).get("all", 0)
        i10_index = cited_by.get("i10_index", {}).get("all", 0)

        output = {
            "name": results.get("name"),
            "affiliation": results.get("affiliation"),
            "interests": results.get("interests", []),
            "email_domain": results.get("email_domain", ""),
            "url_picture": results.get("url_picture", ""),
            "total_citations": total_citations,
            "h_index": h_index,
            "i10_index": i10_index
        }

        # 保存结果
        os.makedirs("./results", exist_ok=True)
        with open("./results/citation_summary.json", "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print("✅ Citation summary saved to ./results/citation_summary.json")

    except Exception as e:
        print("❌ An error occurred during execution.")
        traceback.print_exc()

if __name__ == "__main__":
    main()
