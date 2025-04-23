import os
import json
from scholarly import scholarly

def main():
    # 获取环境变量中的 Google Scholar ID
    scholar_id = os.environ.get("GOOGLE_SCHOLAR_ID")

    if not scholar_id:
        print("❌ ERROR: GOOGLE_SCHOLAR_ID not found in environment variables.")
        return

    print(f"📌 Scholar ID: {scholar_id}")

    try:
        # 查找作者信息并填充
        author = scholarly.search_author_id(scholar_id)
        results = scholarly.fill(author)

        # 打印完整原始数据（调试用）
        print("🔎 Raw results:")
        print(json.dumps(results, indent=2))

        # 尝试获取引用总数，如果不存在就设为 0
        total_citations = results.get("cited_by", {}).get("total", 0)
        print(f"📊 Total Citations: {total_citations}")

        # 构建简化版输出数据
        output = {
            "name": results.get("name", "N/A"),
            "affiliation": results.get("affiliation", "N/A"),
            "total_citations": total_citations,
            "h_index": results.get("cited_by", {}).get("h_index", {}).get("all", 0),
            "i10_index": results.get("cited_by", {}).get("i10_index", {}).get("all", 0)
        }

        # 保存为 JSON 文件
        output_path = "./results/citation_summary.json"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        print(f"✅ Citation summary saved to {output_path}")

    except Exception as e:
        print(f"❌ ERROR during data fetching or processing: {e}")

if __name__ == "__main__":
    main()
