import os
import json
from datetime import datetime
from serpapi import GoogleSearch

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

# ========== 新增调试输出 ==========
api_key = os.environ.get("SERPAPI_KEY")
if not api_key:
    print("❌ SERPAPI_KEY not found in environment variables!")
    exit(1)
else:
    print("🔐 SERPAPI_KEY detected, length:", len(api_key))

# ========== 错误检查 ==========
if "error" in results:
    print(f"❌ SerpAPI error: {results['error']}")
    exit(1)
if "cited_by" not in results:
    print("❌ Missing 'cited_by' in response — likely incorrect author_id or not public.")
    exit(1)

# ========== 正常处理 ==========
results["updated"] = str(datetime.now())
os.makedirs("results", exist_ok=True)
with open("results/gs_data.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{results['cited_by']['total']}",
}
with open("results/gs_data_shieldsio.json", "w", encoding="utf-8") as f:
    json.dump(shieldio_data, f, ensure_ascii=False)

print("✅ [DONE] Citation data updated via SerpAPI.")
