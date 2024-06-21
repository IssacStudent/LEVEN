import logging

import numpy as np
import torch
from flask import Flask, request, jsonify
from flask_cors import CORS
from torch.utils.data import DataLoader, SequentialSampler, TensorDataset
from transformers import BertConfig, BertForTokenClassification, BertTokenizer

from constants import get_labels
from input_processor import process_input_examples, split_chinese_sentences, construct_examples, \
    convert_examples_to_features

app = Flask(__name__)
CORS(app)
logger = logging.getLogger(__name__)
logger.info("Start to initialize the app")
labels = get_labels()
num_labels = len(labels)
device = torch.device("cpu")

config_class, model_class, tokenizer_class = BertConfig, BertForTokenClassification, BertTokenizer
config = config_class.from_pretrained('./led-roberta',
                                      num_labels=num_labels)
tokenizer = tokenizer_class.from_pretrained('hfl/chinese-roberta-wwm-ext',
                                            do_lower_case=True, )
model = model_class.from_pretrained('./saved_20240228/checkpoint-2200')
model.to(device)
logger.info("Finish to initialize the app")


@app.route('/op', methods=['POST'])
def op():
    data = request.json
    service = data.get('service', 'dataInterface')
    command = data.get('command', 'eventDetection')
    if service == 'dataInterface' and command == 'eventDetection':
        event_detection_data = data.get('data', {})
        event_detection_res_data = event_detection(event_detection_data)
        return jsonify({
            'code': 200,
            'data': event_detection_res_data,
            'msg': 'success',
            'total': len(event_detection_res_data)
        })
    else:
        return jsonify({
            'msg': 'Invalid service or command',
            'code': 500,
            'data': {},
            'total': 0
        })


def event_detection(data):
    text = data.get('text', '')
    sentences = split_chinese_sentences(text)
    examples = construct_examples(sentences)
    features = convert_examples_to_features(
        examples,
        labels,
        512, tokenizer,
        cls_token_at_end=False,  # xlnet has a cls token at the end
        cls_token=tokenizer.cls_token,
        cls_token_segment_id=0,
        sep_token=tokenizer.sep_token,
        sep_token_extra=False,  # roberta uses an extra separator b/w pairs of sentences
        pad_on_left=False,  # pad on the left for xlnet
        pad_token=tokenizer.convert_tokens_to_ids([tokenizer.pad_token])[0],
        pad_token_segment_id=0,
        pad_token_label_id=-100
    )

    all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
    all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
    all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
    all_label_ids = torch.tensor([f.label_ids for f in features], dtype=torch.long)

    dataset = TensorDataset(all_input_ids, all_input_mask, all_segment_ids, all_label_ids)

    sampler = SequentialSampler(dataset)
    dataloader = DataLoader(dataset, sampler=sampler, batch_size=8)

    preds = None
    out_label_ids = None
    model.eval()
    for batch in dataloader:
        batch = tuple(t.to(device) for t in batch)
        with torch.no_grad():
            inputs = {"input_ids": batch[0],
                      "attention_mask": batch[1],
                      "token_type_ids": batch[2],
                      "labels": batch[3]}

            outputs = model(**inputs)
            logits = outputs[1]
            best_path = torch.argmax(logits, dim=2)
        if preds is None:
            preds = best_path.detach().cpu().numpy()
            out_label_ids = inputs['labels'].detach().cpu().numpy()
        else:
            preds = np.append(preds, best_path.detach().cpu().numpy(), axis=0)
            out_label_ids = np.append(out_label_ids, inputs["labels"].detach().cpu().numpy(), axis=0)

    label_map = {i: label for i, label in enumerate(labels)}
    out_label_list = [[] for _ in range(out_label_ids.shape[0])]
    preds_list = [[] for _ in range(out_label_ids.shape[0])]

    for i in range(out_label_ids.shape[0]):
        for j in range(out_label_ids.shape[1]):
            if out_label_ids[i, j] != -100:
                out_label_list[i].append(label_map[out_label_ids[i][j]])
                preds_list[i].append(label_map[preds[i][j]])

    for i in range(len(preds_list)):
        examples[i].labels = preds_list[i]

    results = process_input_examples(examples)
    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
