from scholarly import scholarly
import json
from datetime import datetime
import os
import signal
import sys

# ========== Timeout Setup ==========
class TimeoutException(Exception): pass
def timeout_handler(signum, frame):
    raise TimeoutException("Script timed out")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(60)  # 设置总运行时间上限为60秒（可根据需要修改）

# ========== Start Script ==========
try:
    print("Fetching author ID...")
    author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])

    print("Filling author profile...")
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

    name = author['name']
    author['updated'] = str(datetime.now())
    author['publications'] = {v['author_pub_id']:v for v in author['publications']}
    
    print("Saving results...")
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

except TimeoutException as e:
    print(f"❌ Timeout: {e}")
    sys.exit(1)

except Exception as e:
    print(f"❌ Failed to retrieve Google Scholar data: {e}")
    sys.exit(1)
