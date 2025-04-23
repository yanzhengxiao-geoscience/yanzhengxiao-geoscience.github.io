from scholarly import scholarly
import json
from datetime import datetime
import os
from multiprocessing import Process
import sys

def run_crawler():
    try:
        print("📘 [START] Fetching author...")
        author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
        scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
        author['updated'] = str(datetime.now())
        author['publications'] = {v['author_pub_id']:v for v in author['publications']}

        print("📗 [INFO] Saving results...")
        os.makedirs('results', exist_ok=True)
        with open(f'results/gs_data.json', 'w') as outfile:
            json.dump(author, outfile, ensure_ascii=False, indent=2)

        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            "message": f"{author['citedby']}",
        }
        with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
            json.dump(shieldio_data, outfile, ensure_ascii=False)

        print("✅ Citation data successfully updated.")

    except Exception as e:
        print(f"❌ Error in scholarly script: {e}")
        sys.exit(1)


if __name__ == '__main__':
    p = Process(target=run_crawler)
    p.start()
    p.join(timeout=60)  # 最多运行 60 秒
    if p.is_alive():
        print("❌ Timeout: scholarly crawl took too long.")
        p.terminate()
        p.join()
        sys.exit(1)
