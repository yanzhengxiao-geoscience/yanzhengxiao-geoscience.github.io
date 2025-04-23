import os
import json
import time
from datetime import datetime
from serpapi import GoogleSearch

# --- 获取变量 ---
AUTHOR_ID = os.getenv("GOOGLE_SCHOLAR_ID")
API_KEY = os.getenv("SERPAPI_KEY")

params = {
    "engine": "google_scholar_author",
    "author_id": AUTHOR_ID,
    "api_key": API_KEY
}

def fetch_author_data(max_retries=3):
    for attempt in range(max_retries):
        print(f"🔄 Attempt {attempt + 1}: Fetching data from SerpAPI...")
        try:
            search = GoogleSearch(params)
            results = search.get_dict()

            # 检查 cited_by 字段是否存在
            cited_by = results.get("author", {}).get("cited_by", {})
            if cited_by:
                print("✅ Successfully fetched cited_by block:")
                print(json.dumps(cited_by, indent=2))
                return results, cited_by
            else:
                print("⚠️ 'cited_by' block empty, retrying...")
        except Exception as e:
            print(f"❌ Error during SerpAPI request: {e}")
        time.sleep(5)
    return None, {}

# --- 主运行逻辑 ---
results, cited_by = fetch_author_data()

# --- 提取引用数 ---
try:
    citations = cited_by["table"][0]["citations"]
except (KeyError, IndexError, TypeError):
    citations = "N/A"
    print("❗ Failed to extract citation count from 'table[0][citations]'")

# --- 写入文件 ---
os.makedirs("results", exist_ok=True)

# 1. 保存完整结果
with open("results/gs_data.json", "w", encoding="utf-8") as f:
    if results:
        results["fetched_at"] = str(datetime.now())
    json.dump(results or {"error": "No data fetched"}, f, ensure_ascii=False, indent=2)

# 2. 保存 shields.io 格式数据
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citations)
}
with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
    json.dump(shieldio_data, f, ensure_ascii=False)

print(f"📊 Final citation count: {citations}")
print("✅ All data written to /results")
