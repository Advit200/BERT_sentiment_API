import transformers
from Model import SentimentModel
import torch


PRETRAINED_MODEL = "bert-base-cased"
MODEL_PATH = "./Model/Bert_model.bin"
TOKENIZER = transformers.BertTokenizer.from_pretrained(PRETRAINED_MODEL)
MAX_LEN = 128
N_CLASSES = 3

MODEL = SentimentModel()
MODEL.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))

REDIS_PORT = 6379
APP_PORT = 8080
HOST = "redis-server"