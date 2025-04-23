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

os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citation_count)
}

with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

# ✅ 保存一份到项目根目录（GitHub Pages 可直接访问）
with open("../gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
