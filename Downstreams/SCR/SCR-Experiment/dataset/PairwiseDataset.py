import json
import os
from torch.utils.data import Dataset
import random


class PairwiseDataset(Dataset):
    def __init__(self, config, mode, encoding="utf8", *args, **params):
        self.config = config
        self.mode = mode

        self.query_path = config.get("data", "query_path")
        self.cand_path = config.get("data", "cand_path")
        self.labels = json.load(open(config.get("data", "label_path"), 'r'))
        self.data = []

        test_file = config.get("data", "test_file")
        querys = []
        for i in range(5):
            if mode == 'train':
                if test_file == str(i):
                    continue
                else:
                    querys += json.load(open(os.path.join(self.query_path, 'query_%d.json' % i), 'r', encoding='utf-8'))
            else:
                if test_file == str(i):
                    querys = json.load(open(os.path.join(self.query_path, 'query_%d.json' % i), 'r', encoding='utf-8'))
        pos_num = 0
        self.query2posneg = {}
        self.lenn = []
        for query in querys:
            que = query["q"]
            path = os.path.join(self.cand_path, str(query["ridx"]))
            self.query2posneg[str(query["ridx"])] = {"pos": [], "neg": []}
            tmp_num = 0
            for fn in os.listdir(path):
                tmp_num += 1
                cand = json.load(open(os.path.join(path, fn), "r", encoding="utf-8"))
                label = int(fn.split('.')[0]) in self.labels[str(query["ridx"])]
                if label:
                    self.query2posneg[str(query["ridx"])]["pos"].append(len(self.data))
                else:
                    self.query2posneg[str(query["ridx"])]["neg"].append(len(self.data))
                self.data.append({
                    "query": que,
                    "cand": cand["ajjbqk"],
                    "label": label,
                    "index": (query["ridx"], fn.split('.')[0]),
                    "query_inputs": query['inputs'],                # added event info
                    "cand_inputs": cand['inputs']                   # added event info
                })
                pos_num += int(label)
            self.lenn.append(tmp_num)

        print(mode, "positive num:", pos_num)

    def __getitem__(self, item):
        pair1 = self.data[item % len(self.data)]
        return (pair1, )

    def __len__(self):
        if self.mode == "train":
            return len(self.data)
        else:
            return len(self.data)
