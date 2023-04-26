import torch

from models import Bert_BiLSTM_CRF
from main import tag2idx
# model = Bert_BiLSTM_CRF(tag2idx).cuda()
# model.load_state_dict(torch.load('best_model.pth'))
model = torch.load('best_model.pth')
print(model)