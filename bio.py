file_input = './resources/test.txt'
file_output = './resources/data_labeled.txt'

# file_input = './resources/temp.txt'
# file_output = './resources/temp_result.txt'



features_list = ['实施', '的违法行为', '，记', '分，给予', '给予', '的处罚', '依据', '']
label_list = ['B-ACT', 'I-ACT', 'B-SCORE', 'I-SCORE', 'B-PUNISH', 'I-PUNISH', 'B-LAW', 'I-LAW']

fileHandler_1 = open(file_input, "r", encoding="utf-8")
fileHandler_2 = open(file_output, "w", encoding="utf-8")

with open(file_input, 'r', encoding='utf-8') as f:
    while True:
        line = fileHandler_1.readline()
        if not line:
            break
        print(line)
        word_list = list(line.strip())
        print(word_list)
        tag_list = ["O" for i in range(len(word_list))]

        #ACT
        index_1 = line.find(features_list[0])
        index_2 = line.find(features_list[1])
        len_1 = len(features_list[0])
        start_index = index_1 + len_1
        end_index = index_2
        tag_list[start_index] = label_list[0]
        for j in range(start_index + 1, end_index):
            tag_list[j] = label_list[1]

        #SCORE
        index_3 = line.find(features_list[2])
        index_4 = line.find(features_list[3])
        if (index_3 != -1 and index_4 != -1):
            len_1 = len(features_list[2])
            start_index = index_3 + len_1
            end_index = index_4
            print(start_index,end_index)
            tag_list[start_index] = label_list[2]
            for j in range(start_index + 1, end_index):
                tag_list[j] = label_list[3]

        #PUNISH
        index_5 = line.find(features_list[4])
        index_6 = line.find(features_list[5])
        len_1 = len(features_list[4])
        start_index = index_5 + len_1
        end_index = index_6
        tag_list[start_index] = label_list[4]
        for j in range(start_index + 1, end_index):
            tag_list[j] = label_list[5]

        #LAW
        index_7 = line.find(features_list[6])
        len_1 = len(features_list[6])
        start_index = index_7 + len_1
        end_index = -1
        if(index_3!=-1):
            end_index = index_3 - 1
        else:
            end_index = index_5 - 1
        tag_list[start_index] = label_list[6]
        for j in range(start_index + 1, end_index):
            tag_list[j] = label_list[7]

        #输出
        for w, t in zip(word_list, tag_list):
            print(w + " " + t)
            if w != '	' and w != ' ':
                fileHandler_2.write(w + " " + t + '\n')
                # output_f.write(w + " "+t)
        fileHandler_2.write('\n')
        # break

fileHandler_1.close()
fileHandler_2.close()
