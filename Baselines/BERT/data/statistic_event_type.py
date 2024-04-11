import json
from collections import Counter

# 初始化计数器
event_counts = Counter()

# 读取jsonl文件并统计事件类型
with open("train.jsonl", "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)
        for event in data["events"]:
            event_type = event["type"]
            event_counts[event_type] += 1

sorted_event_counts = sorted(event_counts.items(), key=lambda x: x[1], reverse=True)
# 输出每种类型的事件数量
for event_type, count in sorted_event_counts:
    print(f"{event_type},")

