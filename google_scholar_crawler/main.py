import requests
import json
import os
from datetime import datetime

# 读取环境变量
API_KEY = os.environ.get("SERPAPI_KEY")
SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")

# 校验
if not API_KEY or not SCHOLAR_ID:
    raise ValueError("SERPAPI_KEY or GOOGLE_SCHOLAR_ID is not set")

# 请求 SerpAPI
url = "https://serpapi.com/search"
params = {
    "engine": "google_scholar_author",
    "author_id": SCHOLAR_ID,
    "api_key": API_KEY
}

response = requests.get(url, params=params)
data = response.json()

# 提取引用数
citation_count = data.get("cited_by", {}).get("table", [{}])[0].get("citations", {}).get("all", 0)
name = data.get("author", {}).get("name", "unknown")

# 准备输出目录
os.makedirs("results", exist_ok=True)

# 保存原始数据
with open("results/gs_data.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 构造 shields.io 显示格式
shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": str(citation_count)
}

# 保存到 /results/ 中
with open("results/gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

# ✅ 保存一份到项目根目录（main 分支）
with open("../gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

# ✅ 保存一份到 scholar_branch/ 用于推送到 google-scholar-stats 分支
os.makedirs("../scholar_branch", exist_ok=True)
with open("../scholar_branch/gs_data_shieldsio.json", "w") as f:
    json.dump(shieldio_data, f, indent=2, ensure_ascii=False)

print(f"✅ {name} 的引用数是 {citation_count}")
