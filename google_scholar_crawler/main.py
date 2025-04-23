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

# ✅ 正确提取引用数
citation_count = data.get("cited_by", {}).get("table", [{}])[0].get("citations", {}).get("all", 0)

# ✅ 正确提取作者名
name = data.get("author", {}).get("name", "unknown")

# ✅ 保存完整 JSON
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# ✅ 构建徽章 JSON
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citation_count)
}

# ✅ 保存徽章 JSON 到两个位置
with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

with open(os.path.join(os.path.dirname(__file__), "..", "gs_data_shieldsio.json"), "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
