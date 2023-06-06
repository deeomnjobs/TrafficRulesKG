import argparse

import numpy as np
import prettytable as pt
import torch
import torch.autograd
import torch.nn as nn
import transformers
from sklearn.metrics import precision_recall_fscore_support, f1_score
from torch.utils.data import DataLoader

import config
import data_loader
import utils
from model import Model

class Trainer(object):
    def __init__(self, mode, device):
        self.model = model
        self.model = self.model.to(device)
        self.device = device

    def predict(self, predict_loader):
        self.model.eval()
        predict_result = []
        with torch.no_grad():
            for i, data_batch in enumerate(predict_loader):
                texts = data_batch[-1]
                data_batch = [data.to(self.device) for data in data_batch[:-1]]
                bert_inputs, grid_mask2d, pieces2word, dist_inputs, sent_length = data_batch
                outputs = model(bert_inputs, grid_mask2d, dist_inputs, pieces2word, sent_length)
                outputs = torch.argmax(outputs, -1)
                predict_decode(outputs.cpu().numpy(), sent_length.cpu().numpy(), texts)

    def save(self, path):
        torch.save(self.model.state_dict(), path)

    def load(self, path):
        self.model.load_state_dict(torch.load(path))

def predict_decode(outputs, length, texts):
    entities = []
    for index, (instance, l, text) in enumerate(zip(outputs, length, texts)):
        forward_dict = {}
        head_dict = {}
        ht_type_dict = {}
        for i in range(l):
            for j in range(i + 1, l):
                if instance[i, j] == 1:
                    if i not in forward_dict:
                        forward_dict[i] = [j]
                    else:
                        forward_dict[i].append(j)
        for i in range(l):
            for j in range(i, l):
                if instance[j, i] > 1:
                    ht_type_dict[(i, j)] = instance[j, i]
                    if i not in head_dict:
                        head_dict[i] = {j}
                    else:
                        head_dict[i].add(j)

        predicts = []

        def find_entity(key, entity, tails):
            entity.append(key)
            if key not in forward_dict:
                if key in tails:
                    predicts.append(entity.copy())
                entity.pop()
                return
            else:
                if key in tails:
                    predicts.append(entity.copy())
            for k in forward_dict[key]:
                find_entity(k, entity, tails)
            entity.pop()

        def convert_index_to_text(index, type):
            text = "-".join([str(i) for i in index])
            text = text + "-#-{}".format(type)
            return text

        for head in head_dict:
            find_entity(head, [], head_dict[head])
        predicts = set([convert_index_to_text(x, ht_type_dict[(x[0], x[-1])]) for x in predicts])
        tmp = (text,)
        for pre in predicts:
            pre = pre.split('-#-')
            ind = pre[0].split('-')
            entity = text[int(ind[0]):int(ind[-1]) + 1]
            entity_type = config.vocab.id2label[int(pre[1])]
            tmp += ((entity, entity_type, int(ind[0]), int(ind[-1])),)
        entities.append(tmp)
    print(entities)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='./config/conll03.json')
    parser.add_argument('--device', type=int, default=0)

    parser.add_argument('--dist_emb_size', type=int)
    parser.add_argument('--type_emb_size', type=int)
    parser.add_argument('--lstm_hid_size', type=int)
    parser.add_argument('--conv_hid_size', type=int)
    parser.add_argument('--bert_hid_size', type=int)
    parser.add_argument('--ffnn_hid_size', type=int)
    parser.add_argument('--biaffine_size', type=int)

    parser.add_argument('--dilation', type=str, help="e.g. 1,2,3")

    parser.add_argument('--emb_dropout', type=float)
    parser.add_argument('--conv_dropout', type=float)
    parser.add_argument('--out_dropout', type=float)

    parser.add_argument('--epochs', type=int)
    parser.add_argument('--batch_size', type=int)

    parser.add_argument('--clip_grad_norm', type=float)
    parser.add_argument('--learning_rate', type=float)
    parser.add_argument('--weight_decay', type=float)

    parser.add_argument('--bert_name', type=str)
    parser.add_argument('--bert_learning_rate', type=float)
    parser.add_argument('--warm_factor', type=float)

    parser.add_argument('--use_bert_last_4_layers', type=int, help="1: true, 0: false")

    parser.add_argument('--seed', type=int)

    args = parser.parse_args()

    config = config.Config(args)

    logger = utils.get_logger(config.dataset)
    logger.info(config)
    config.logger = logger

    if torch.cuda.is_available():
        torch.cuda.set_device(args.device)
    logger.info("Loading Data")
    texts = [
        '2022年12月31日12时51分，号牌为沪AAX8 ** * 的轻型封闭式货车在博园路近联西路路段，实施“驾驶机动车不按机动车信号灯表示通行的”违法行为，处罚：罚款200元，记6分。'
    ]
    # 这一步要在model之前创建，因为还有给config添加属性
    predict_dataset = data_loader.load_data_bert_predict(texts, config)
    predict_loader = DataLoader(dataset=predict_dataset,
                                batch_size=config.batch_size,
                                collate_fn=data_loader.collate_fn_predict,
                                shuffle=False,
                                num_workers=4,
                                drop_last=False)
    # updates_total这个参数直接设置为0即可
    updates_total = 0
    logger.info("Building Model")
    model = Model(config)
    device = torch.device("cpu")
    trainer = Trainer(model, device)
    trainer.load("model.pt")
    trainer.predict(predict_loader)