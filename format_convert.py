# coding:utf-8
import csv
import json
import os

remove_chars = len(os.linesep)


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
    with open('./nation.csv', 'w', encoding='utf-8', newline='') as csvfile:
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
#
# struct_list = []
# with open("./resources/struct_res.json","r",encoding='utf-8') as f:
#         struct_list = json.load(f)


def JSON2BIO(file1, file2, file3):
    with open(file1, 'r', encoding='utf-8') as f:
        json_list = json.load(f)
    sentence_list = []
    tag_list = []
    json_convert = []
    for record in json_list:
        sentence = list(filter(lambda x: x != ' ', record['sentence']))
        # 去除最后一个换行符
        sentence.pop()
        if sentence[0] == ' ':
            sentence[0] = '。'
        if sentence[-1] == ' ':
            sentence[-1] == '。'
        tag = []
        for i in range(len(sentence)):
            tag.append('O')
        for ner in record['ner']:
            begin = 0
            for index in ner['index']:
                if begin == 0:
                    tag[index] = 'B-' + ner['type']
                    begin = begin + 1
                else:
                    tag[index] = 'I-' + ner['type']
        json_convert.append({"text": sentence, "label": tag})
        for i in sentence:
            sentence_list.append(i)
        for i in tag:
            tag_list.append(i)
    with open(file2, 'a+', encoding='utf-8') as f:
        for i, j in zip(sentence_list, tag_list):
            f.write(i + '\t' + j + '\n')
            # f.truncate(f.tell() - 2)
    # with open(file3,'w',encoding='utf-8') as f:
    #     for data in json_convert:
    #         json.dump(data,f)
    #         f.write('\n')


# JSON2BIO('./resources/w2ner/labeled_val_weibo_w2ner.json','./resources/BIO/val_weibo.txt','./resources/LEBERT/dev.json')
# JSON2BIO('./resources/w2ner/labeled_train_weibo_w2ner.json','./resources/BIO/train_weibo.txt','./resources/LEBERT/train.json')
# JSON2BIO('./resources/w2ner/labeled_test_weibo_w2ner.json','./resources/BIO/test_weibo.txt','./resources/LEBERT/test.json')

JSON2BIO('./resources/resume-zh/dev.json', './resources/resume-zh/val_resume.txt')
JSON2BIO('./resources/resume-zh/train.json', './resources/resume-zh/train_resume.txt')
JSON2BIO('./resources/resume-zh/test.json', './resources/resume-zh/test_resume.txt')
