import json

def process_jsonl(file_path):
    total_tokens = 0
    total_trigger_words = 0

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line)

            # 累积tokens的数量
            for content in data['content']:
                total_tokens += len(content['tokens'])

            # 累积事件中触发词的数量
            for event in data['events']:
                for mention in event['mention']:
                    total_trigger_words += 1

            # 累积负样本中触发词的数量
            # total_trigger_words += len(data['negative_triggers'])

    # 计算触发词的比例
    trigger_word_ratio = total_trigger_words / total_tokens if total_tokens > 0 else 0
    return total_tokens, total_trigger_words, trigger_word_ratio

# 替换为您的jsonl文件路径
file_path = 'valid.jsonl'
total_tokens, total_trigger_words, trigger_word_ratio = process_jsonl(file_path)

print(f"总共的tokens数量：{total_tokens}")
print(f"总共的触发词数量：{total_trigger_words}")
print(f"触发词的比例：{trigger_word_ratio:.2%}")
