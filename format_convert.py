# coding:utf-8
import csv
import json


def w2ner2list(list_predict):
    act_set = set()
    nodes_list = []
    temp = {}
    # [(
    # 号牌为沪AAP8***的小型轿车在逸仙高架东侧近场中路下匝道路段，实施“机动车违反禁止标线指示的”违法行为，处罚：罚款200元，记1分。\n',
    # ('罚款200元', 'PUNISH', 74, 79),
    # ('记1分', 'SCORE', 81, 83),
    # ('机动车违反禁止标线指示的', 'ACT', 53, 64)
    # )
    # ,()
    # ]
    for predict in list_predict:
        for entity in predict[1:]:
            if entity[1] == 'ACT':
                if entity[0] not in act_set:
                    act_set.add(entity[0])
                    for e in predict[1:]:
                        temp[e[1]] = e[0]
                    nodes_list.append(temp)
                    temp = {}
    return nodes_list


def w2ner_write2csv(nodes_list):
    with open('ShangHai.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ACT', 'PUNISH', 'SCORE', 'BELONG'])
        for node in nodes_list:
            act = '####'
            punish = '####'
            score = '####'
            belong = '上海市地方法规'
            if 'ACT' in node:
                act = node['ACT']
            if 'PUNISH' in node:
                punish = node['PUNISH']
            if 'SCORE' in node:
                score = node['SCORE']
            writer.writerow([act, punish, score, belong])

def nation_writer2csv(struct_list):
    with open('./nation.csv','w',encoding='utf-8',newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ACT', 'PUNISH', 'SCORE', 'BELONG'])
        for node in struct_list:
            act = '####'
            punish = '####'
            score = '####'
            belong = '上海市地方法规'
            if 'ACT' in node:
                act = node['ACT']
            if 'PUNISH' in node:
                punish = node['PUNISH']
            if 'SCORE' in node:
                score = node['SCORE']
            writer.writerow([act, punish, score, belong])
# with open('./resources/output.txt', 'r', encoding='GBK') as f:
#     content = f.read()
# content = eval(content)
# unstruct_nodes_list = w2ner2list(content)
# write2csv(unstruct_nodes_list)

struct_list = []
with open("./resources/struct_res.json","r",encoding='utf-8') as f:
        struct_list = json.load(f)

