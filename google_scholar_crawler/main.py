import requests
import json
import os
from datetime import datetime

API_KEY = os.environ.get("SERPAPI_KEY")
SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")

if not API_KEY or not SCHOLAR_ID:
    raise ValueError("SERPAPI_KEY or GOOGLE_SCHOLAR_ID is not set")

url = "https://serpapi.com/search"
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

citation_count = data.get("cited_by", {}).get("table", [{}])[0].get("citations", {}).get("all", 0)
name = data.get("author", {}).get("name", "unknown")

# 写入 result 目录（保留）
os.makedirs("results", exist_ok=True)
with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump({
        "schemaVersion": 1,
        "label": "citations",
        "message": str(citation_count)
    }, f, indent=2, ensure_ascii=False)

# ✅ 写入仓库根目录
with open("../gs_data_shieldsio.json", "w") as f:
    json.dump({
        "schemaVersion": 1,
        "label": "citations",
        "message": str(citation_count)
    }, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
