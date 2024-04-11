import json
from collections import Counter
import time

from tqdm import tqdm

from chatgpt import chatgpt
from chatgpt4 import chatgpt4
from glm import glm4


def evaluate_llm_from_file(data_file, task_name, start):
    """
    Evaluate LLM's performance on event detection from a given JSON data file.
    """
    try:
        # Load data from the JSON file
        with open(data_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(f"Error loading data from {data_file}: {e}")
        return

    # Initialize counters
    true_positives = Counter()
    predicted_positives = Counter()
    actual_positives = Counter()
    # 初始化一个数组，用来存储预测的结果和实际的结果，以及编号
    result = []
    index = 0
    try:
        for item in tqdm(data):
            if index < start:
                index += 1
                continue
            instruction = item["instruction"]
            question = item["question"]
            actual_answer = item["answer"]

            # Simulate LLM call
            predicted_answer = chatgpt4(instruction, question, False)
            time.sleep(1)
            # if predicted_answer == 'resend':
            #     # 延时10秒
            #     time.sleep(10)
            #     predicted_answer = tongyi(instruction, question, True)

            if predicted_answer is None:
                print(f"Error evaluating LLM: No answer returned for question: {question}")
                print(index)
                continue
            # Update counters
            if predicted_answer == actual_answer:
                true_positives[predicted_answer] += 1
            predicted_positives[predicted_answer] += 1
            actual_positives[actual_answer] += 1
            result.append([question, actual_answer, predicted_answer])
            index += 1
    except Exception as e:
        print(f"Error evaluating LLM: {e}")



    # Calculate Precision, Recall, F1
    precision = sum(true_positives.values()) / sum(predicted_positives.values()) if sum(
        predicted_positives.values()) > 0 else 0
    recall = sum(true_positives.values()) / sum(actual_positives.values()) if sum(actual_positives.values()) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    # 打印result数组到文件
    with open(task_name + "_result.txt", "a", encoding="utf-8") as file:
        file.write(f"True Positives: {sum(true_positives.values())}, Predicted Positives: {sum(predicted_positives.values())}, Actual Positives: {sum(actual_positives.values())}\n")
        file.write(f"True Positives: {true_positives}\n")
        file.write(f"Predicted Positives: {predicted_positives}\n")
        file.write(f"Actual Positives: {actual_positives}\n")
        file.write(f"Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}\n")
        file.write(f"result:\n")
        # 一行一行打印result，打印成json格式
        for i in result:
            file.write(json.dumps(i, ensure_ascii=False) + "\n")

#main函数
if __name__ == "__main__":
    # evaluate_llm_from_file("./2_shot_dataset_2000.json", "gpt4_2_shot_2000", 123)
    # evaluate_llm_from_file("./5_shot_dataset_2000.json", "gpt4_5_shot_2000", 140)
    evaluate_llm_from_file("./10_shot_dataset_2000.json", "gpt4_10_shot_2000", 108)