from scholarly import scholarly
import json
import os

GOOGLE_SCHOLAR_ID = os.environ.get("GOOGLE_SCHOLAR_ID")
if not GOOGLE_SCHOLAR_ID:
    print("❌ GOOGLE_SCHOLAR_ID not set!")
    exit(1)

print("📘 [START] Fetching data using SerpAPI...")

author = scholarly.search_author_id(GOOGLE_SCHOLAR_ID)
results = scholarly.fill(author)

print(f"✅ Got results for {results['name']}")

with open("results/citation.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("📁 Citation data saved to results/citation.json")

# optional: output a summary
summary = {
    "message": f"{results['cited_by']['total']}",
    "h_index": results['cited_by']['h_index']['all'],
    "i10_index": results['cited_by']['i10_index']['all']
}

with open("results/citation_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)

print("📁 Summary saved to results/citation_summary.json")
