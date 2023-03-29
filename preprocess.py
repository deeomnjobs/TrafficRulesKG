import json

label = ['B-ACT', 'I-ACT', 'B-LAW', 'I-LAW', 'B-SCORE', 'I-SCORE', 'B-PUNISH', 'I-PUNISH']


def preprocess_file():
    violation_list = []
    json_list = []
    with open("./resources/violation.json", "r", encoding='utf-8') as f:
        for line in f.readlines():
            violation_list.append(json.loads(line.replace("/n", "")))
