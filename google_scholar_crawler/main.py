import requests
import json
import os
from datetime import datetime

API_KEY = os.environ.get("SERPAPI_KEY")  # 在 GitHub Action 设置环境变量
SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")  # 填入 Scholar 的 ID，如 'xJaxiEEAAAAJ'

if not API_KEY or not SCHOLAR_ID:
    raise ValueError("请设置环境变量 SERPAPI_KEY 和 GOOGLE_SCHOLAR_ID")

url = "https://serpapi.com/search"
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# 取出引用数（cited by）
citation_count = data["cited_by"]["value"] if "cited_by" in data else 0
name = data.get("name", "unknown")

# 输出完整数据
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 输出 Shields.io 用的 citation 标签
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{citation_count}",
}
with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
