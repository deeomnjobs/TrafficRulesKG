set_act  = set()
set_score = set()
set_punish = set()
set_law = set()
def extract(sentence,start):

    print()
def w2ner2(list_predict):
    for predict in list_predict:
        for data in range(1, len(predict)):
            if data[1] == 'ACT':
                set_act.add(data[1])
            if data[1] == 'SCORE':
                set_score.add(data[1])
            if data[1] == 'PUNISH':
                set_punish.add(data[1])
            if data[1] == 'LAW':
                set_law.add(data[1])
    print()