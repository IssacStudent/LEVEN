import json
from tqdm import tqdm


# 合并文件
def merge_files(file1, file2, output_file):
    merged_data = []
    for file in [file1, file2]:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                data = json.loads(line.strip())
                merged_data.append(data)

    print(f"合并后的数据条数：{len(merged_data)}")

    # 拆分每条数据，确保每条新数据只有一个events对象
    split_data = []
    for item in tqdm(merged_data, desc="Processing"):
        for event in item['events']:
            # 创建一个新的字典，除了events是单个对象外，其余数据与原数据相同
            new_item = item.copy()
            new_item['events'] = [event]
            split_data.append(new_item)

    # 保存处理后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in split_data:
            json.dump(item, f, ensure_ascii=False)
            f.write('\n')

    print(f"处理后的数据条数：{len(split_data)}")
    return split_data


# 调用函数，合并并处理文件
merge_files('train.jsonl', 'valid.jsonl', 'merged_data.jsonl')
