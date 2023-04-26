import json
import logging
import os

file_json = './resources/violation.json'
file_violation_data = './resources/violation_data.txt'
file_train_BIO = './resources/labeled_train.txt'
file_val_BIO = './resources/labeled_val.txt'
file_test_BIO = './resources/labeled_test.txt'
file_violation_data_W2NER_json = './resources/violation_W2NER_json.json'
file_train_w2ner = './resources/labeled_train_w2ner.json'
file_val_w2ner = './resources/labeled_val_w2ner.json'
file_test_w2ner = './resources/labeled_test_w2ner.json'

features_list = ['实施', '的违法行为', '，记', '分，给予', '给予', '的处罚', '依据', '']
label_list = ['B-ACT', 'I-ACT',  'B-SCORE', 'I-SCORE', 'B-PUNISH', 'I-PUNISH','B-LAW', 'I-LAW']
remove_chars = len(os.linesep)
logging.getLogger().setLevel(logging.INFO)


def data_concat():
    logging.info("data_concat is running.")
    result_list = []
    with open(file_json, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            violation_data = json.loads(line)
            segment = violation_data['act'].replace('。', '，') + '依据' + violation_data['law'] + '' + '，'
            if not violation_data['score'].__contains__('0'):
                segment = segment + violation_data['score'] + '，'
            segment = segment + '给予' + violation_data['punish'] + '的处罚。'
            result_list.append(segment)
    with open(file_violation_data, 'w+', encoding='utf-8') as f:
        for result in result_list:
            f.write(result + '\n')
        f.truncate(f.tell() - remove_chars)
    logging.info("data_concat is over.")


def auto_label_BIO():
    logging.info("auto_label is running.")
    # readlines()只读入内存一次，需要提前存储
    with open(file_violation_data, 'r', encoding='utf-8') as f1:
        lines_f1 = len(f1.readlines())

    with open(file_violation_data, 'r', encoding='utf-8') as f1, open(file_train_BIO, 'w+', encoding='utf-8') as f2, open(file_val_BIO, 'w+', encoding='utf-8') as f3, open(file_test_BIO, 'w+', encoding='utf-8') as f4:
        # train : val : test = 8 : 1 : 1
        bound_train = lines_f1 * 0.8
        bound_val = lines_f1 * 0.9
        count = 0
        for line in f1.readlines():
            count = count + 1
            word_list = list(line.strip())
            tag_list = ["O" for i in range(len(word_list))]

            # ACT
            index_1 = line.find(features_list[0])
            index_2 = line.find(features_list[1])
            len_1 = len(features_list[0])
            start_index = index_1 + len_1
            end_index = index_2
            tag_list[start_index] = label_list[0]
            for j in range(start_index + 1, end_index):
                tag_list[j] = label_list[1]

            # SCORE
            index_3 = line.find(features_list[2])
            index_4 = line.find(features_list[3])
            if (index_3 != -1 and index_4 != -1):
                len_1 = len(features_list[2])
                start_index = index_3 + len_1
                end_index = index_4
                tag_list[start_index] = label_list[2]
                for j in range(start_index + 1, end_index):
                    tag_list[j] = label_list[3]

            # PUNISH
            index_5 = line.find(features_list[4])
            index_6 = line.find(features_list[5])
            len_1 = len(features_list[4])
            start_index = index_5 + len_1
            end_index = index_6
            tag_list[start_index] = label_list[4]
            for j in range(start_index + 1, end_index):
                tag_list[j] = label_list[5]

            # LAW
            index_7 = line.find(features_list[6])
            len_1 = len(features_list[6])
            start_index = index_7 + len_1
            end_index = -1
            if (index_3 != -1):
                end_index = index_3 - 1
            else:
                end_index = index_5 - 1
            tag_list[start_index] = label_list[6]
            for j in range(start_index + 1, end_index):
                tag_list[j] = label_list[7]

            # write
            for w, t in zip(word_list, tag_list):
                if w != '	' and w != ' ':
                    if count < bound_train :
                        f2.write(w + '\t' + t + '\n')
                    elif count < bound_val :
                        f3.write(w + '\t' + t + '\n')
                    else:
                        f4.write(w + '\t' + t + '\n')
        f2.truncate(f2.tell() - remove_chars)
        f3.truncate(f3.tell() - remove_chars)
        f4.truncate(f4.tell() - remove_chars)
    logging.info("auto_label is over.")

def auto_label_w2ner():
    res_list = []
    ner_list = []
    with open(file_violation_data,'r',encoding='utf-8') as f:
        for line in f.readlines():
            # ACT
            index_1 = line.find(features_list[0])
            index_2 = line.find(features_list[1])
            if(index_1 != -1 and index_2 != -1):
                len_1 = len(features_list[0])
                start_index = index_1 + len_1
                end_index = index_2
                ner_list.append({"index":list(range(start_index,end_index)),"type":"ACT"})

            # SCORE
            index_3 = line.find(features_list[2])
            index_4 = line.find(features_list[3])
            if (index_3 != -1 and index_4 != -1):
                len_1 = len(features_list[2])
                start_index = index_3 + len_1
                end_index = index_4
                ner_list.append({"index": list(range(start_index, end_index)), "type": "SCORE"})

            # PUNISH
            index_5 = line.find(features_list[4])
            index_6 = line.find(features_list[5])
            if (index_5 != -1 and index_6 != -1):
                len_1 = len(features_list[4])
                start_index = index_5 + len_1
                end_index = index_6
                ner_list.append({"index": list(range(start_index, end_index)), "type": "PUNISH"})

            # LAW
            index_7 = line.find(features_list[6])
            if (index_7 != -1):
                len_1 = len(features_list[6])
                start_index = index_7 + len_1
                end_index = -1
                if (index_3 != -1):
                    end_index = index_3 - 1
                else:
                    end_index = index_5 - 1
                ner_list.append({"index": list(range(start_index, end_index)), "type": "LAW"})
            sentence = [one for one in line]
            res = {'sentence':sentence,'ner':ner_list}
            ner_list = []
            res_list.append(res)
    print(res_list)
    with open(file_violation_data_W2NER_json,'w',encoding='utf-8') as f:
        json.dump(res_list,f)

def data_partion():
    with open(file_violation_data_W2NER_json,'r',encoding='utf-8') as f:
        violation_data = json.load(f)
    size = len(violation_data)
    bound_train = size * 0.8
    bound_val = size * 0.9
    labeled_train_w2ner = []
    labeled_test_w2ner = []
    labeled_val_w2ner = []
    for i in range(size):
        if i < bound_train:
            labeled_train_w2ner.append(violation_data[i])
        elif i < bound_val:
            labeled_val_w2ner.append(violation_data[i])
        else:
            labeled_test_w2ner.append((violation_data[i]))
    with open(file_train_w2ner,'w',encoding='utf-8') as f:
        json.dump(labeled_train_w2ner,f)
    with open(file_val_w2ner,'w',encoding='utf-8') as f:
        json.dump(labeled_val_w2ner,f)
    with open(file_test_w2ner,'w',encoding='utf-8') as f:
        json.dump(labeled_test_w2ner,f)




# 按需取用
# data_concat()
# auto_label_BIO()
# auto_label_w2ner()
data_partion()