# coding=gbk
# 读取数据
import pandas as pd
import numpy as np
import json
import sys
import os

# data = pd.read_csv("jgj.csv",header=None)
# data = np.array(data)

# print(data[3])
# Open file
fileHandler = open("./resources/violation.json", "r", encoding="utf-8")

result = ""
# Get lines
while True:
    linestr = fileHandler.readline()
    if not linestr:
        break
    data = json.loads(linestr)

    segment = data['act'].replace('。','，') + "依据" + data['law'] + "，"
    if not data['score'].__contains__("0"):
        segment = segment + data["score"] + "，"
    segment = segment + "给予" + data["punish"] + "的处罚。"
    result = result + segment + "\n"

# Close file
fileHandler.close()
print(result)
fw = open("./resources/test.txt", 'w', encoding="utf-8")
fw.write(result)
