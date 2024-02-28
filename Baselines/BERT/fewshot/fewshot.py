import json
from collections import defaultdict
from random import shuffle
from tqdm import tqdm


def load_data_and_process(file_name):
    event_type_count = defaultdict(int)
    data = []

    with open(file_name, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc="Loading data"):
            json_line = json.loads(line.strip())
            # 删除negative_triggers字段
            if 'negative_triggers' in json_line:
                del json_line['negative_triggers']
            data.append(json_line)
            event_type = json_line['events'][0]['type']
            event_type_count[event_type] += 1

    return data, event_type_count


def create_few_shot_dataset(data, event_type_count, k):
    train_data = []
    valid_data = []
    event_type_to_data = defaultdict(list)

    # 分类数据
    for item in tqdm(data, desc="Classifying data"):
        event_type = item['events'][0]['type']
        event_type_to_data[event_type].append(item)

    # 对每种事件类型，随机选择K个数据为训练集，其余为验证集
    for event_type, items in tqdm(event_type_to_data.items(), desc="Creating few-shot dataset"):
        shuffle(items)  # 打乱数据
        train_data.extend(items[:k])
        valid_data.extend(items[k:])

    # 打乱训练集和验证集数据
    shuffle(train_data)
    shuffle(valid_data)

    # 保存训练集和验证集
    with open(str(k) + '_train.jsonl', 'w', encoding='utf-8') as file:
        for item in tqdm(train_data, desc="Writing train data"):
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')

    with open(str(k) + '_valid.jsonl', 'w', encoding='utf-8') as file:
        for item in tqdm(valid_data, desc="Writing valid data"):
            json.dump(item, file, ensure_ascii=False)
            file.write('\n')


# 加载数据并计数
data, event_type_count = load_data_and_process('merged_data.jsonl')

# 打印每种事件类型的数量
for event_type, count in event_type_count.items():
    print(f"事件类型 '{event_type}': {count}个")

# 假设K值，例如K=5
for K in [2, 5, 10]:
    create_few_shot_dataset(data, event_type_count, K)
