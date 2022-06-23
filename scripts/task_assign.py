"""
任务分配脚本
"""

import json
from collections import defaultdict
import requests 


# 为用户分配子任务，包括条目数量，具体的条目ID
def assign_process(item_ids):
    process_url = "http://localhost:8000/api/process/"
    res = requests.post(process_url, data={
        'task': 1,
        'user': 4,
        'assign_num': len(item_ids),
        'finished_num': 0
    })
    content = json.loads(res.content)

    process_assign_url = "http://localhost:8000/api/process_assign/"
    for item_id in item_ids:
        res = requests.post(process_assign_url, data={
            'process': content['id'],
            'item_id': item_id,
            'status': 0
        })

    return


if __name__ == "__main__":
    item_ids = list(range(11, 21))
    assign_process(item_ids)