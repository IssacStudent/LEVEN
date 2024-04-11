import json

# Placeholder for the statistics
total_data_count = 0
total_tokens_count = 0
total_sentences_count = 0
event_types = set()
total_event_count = 0
event_type_counts = {}

# Load and process the JSONL file
with open('valid.jsonl', 'r', encoding='utf-8') as file:
    for line in file:
        data = json.loads(line)

        # Increment data count
        total_data_count += 1

        # Count tokens and sentences
        for content in data['content']:
            total_sentences_count += 1
            total_tokens_count += len(content['tokens'])

        # Count events and event types
        total_event_count += len(data['events'])
        for event in data['events']:
            event_type = (event['type_id'], event['type'])
            event_types.add(event_type)
            if event_type not in event_type_counts:
                event_type_counts[event_type] = 1
            else:
                event_type_counts[event_type] += 1

# Print the statistics
print(f"Total data count: {total_data_count}")
print(f"Total token count: {total_tokens_count}")
print(f"Total sentence count: {total_sentences_count}")
print(f"Total unique event types: {len(event_types)}")
print(f"Total event count: {total_event_count}")
for event_type, count in event_type_counts.items():
    print(f"Event type {event_type}: {count}")
