import requests
import json
import os
from datetime import datetime

# 从 GitHub Actions 的 secrets 获取
API_KEY = os.environ.get("SERPAPI_KEY")
SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")

if not API_KEY or not SCHOLAR_ID:
    raise ValueError("❌ SERPAPI_KEY or GOOGLE_SCHOLAR_ID is not set.")

# SerpAPI 请求参数
url = "https://serpapi.com/search"
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

# 请求数据
response = requests.get(url, params=params)
data = response.json()

# 提取引用数和作者名
citation_count = data.get("cited_by", {}).get("table", [{}])[0].get("citations", {}).get("all", 0)
name = data.get("author", {}).get("name", "unknown")

# 构建 Shields.io JSON 数据
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citation_count)
}

# 写入 results 文件夹 JSON（用于调试）
results_dir = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(results_dir, exist_ok=True)

with open(os.path.join(results_dir, "gs_data.json"), "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

with open(os.path.join(results_dir, "gs_data_shieldsio.json"), "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

# ✅ 写入仓库根目录，供 GitHub Pages 使用
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
with open(os.path.join(root_path, "gs_data_shieldsio.json"), "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
