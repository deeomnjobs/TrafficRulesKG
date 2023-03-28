import json


def preprocess_file():
    violation_list = []
    json_list = []
    with open("./resources/violation.json", "r",encoding='utf-8') as f:
        for line in f.readlines():
            violation_list.append(json.loads(line.replace("/n", "")))
