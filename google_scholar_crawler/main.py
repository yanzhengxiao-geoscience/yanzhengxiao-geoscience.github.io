import os
import json
from datetime import datetime
from serpapi import GoogleSearch

# 获取环境变量
AUTHOR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")
API_KEY = os.environ.get("SERPAPI_KEY")

print("📘 [START] Fetching data using SerpAPI...")

params = {
  "engine": "google_scholar_author",
  "author_id": AUTHOR_ID,
  "api_key": API_KEY
}

search = GoogleSearch(params)
results = search.get_dict()
print("🔍 Full cited_by block:\n", json.dumps(results.get("author", {}).get("cited_by", {}), indent=2))
print(json.dumps(results, indent=2))
# 添加时间戳
results["updated"] = str(datetime.now())

# 创建文件夹
os.makedirs("results", exist_ok=True)

# 保存完整数据
with open("results/gs_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

# 提取 citation 总数写入 shields.io
try:
    citations = results["author"]["cited_by"]["table"][0]["citations"]
except (KeyError, IndexError, TypeError):
    citations = "N/A"

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": str(citations),
}

with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
    json.dump(shieldio_data, f, ensure_ascii=False)

print("✅ [DONE] Citation data updated via SerpAPI.")
