import json
import os
import random

# 定义路径
original_data_folder = 'data'
new_data_folder = 'new_data_newnew'

# 确保新目录存在
if not os.path.exists(new_data_folder):
    os.makedirs(new_data_folder)

# 读取原始数据
all_data = []
for filename in ['train.jsonl', 'valid.jsonl']:
    with open(os.path.join(original_data_folder, filename), 'r', encoding='utf-8') as file:
        for line in file:
            all_data.append(json.loads(line))

# 打乱数据
random.shuffle(all_data)

# 分配数据
train_data = all_data[:4245]
valid_data = all_data[4245:5224]
test_data = all_data[5224:6531]

# 写入新文件
for data, filename in zip([train_data, valid_data, test_data],
                          ['train.jsonl', 'valid.jsonl', 'test.jsonl']):
    with open(os.path.join(new_data_folder, filename), 'w') as file:
        for item in data:
            json.dump(item, file)
            file.write('\n')

print("数据处理完成。")
