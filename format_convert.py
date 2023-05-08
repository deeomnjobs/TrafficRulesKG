# coding:utf-8
set_act  = set()
removal_list = []
def extract(sentence,start):

    print()
def w2ner2(list_predict):
    # predict [0] sentence [1] ACT tuple [2] SCORE tuple [3] PUNISH tuple [4] LAW tuple
    for predict in list_predict:
        if predict[1][1] not in set_act:
            set_act.add(predict[1][1])
            temp = {}
            for data in predict[1:]:
                temp[data[1]] = data[0]
            removal_list.append(temp)
    return removal_list