import transformers
from torch import nn
import config

class SentimentModel(nn.Module):
    
    def __init__(self):
        super().__init__()        
        self.bert_layer = transformers.BertModel.from_pretrained(config.PRETRAINED_MODEL)        
        self.dropout_layer = nn.Dropout(0.3)         
        self.linear_layer = nn.Linear(self.bert_layer.config.hidden_size,config.N_CLASSES)  
                  
    def forward(self,input_ids,attention_mask):        
        output = self.bert_layer(input_ids=input_ids,attention_mask=attention_mask)
        output =  self.dropout_layer(output['pooler_output'])
        output = self.linear_layer(output)
        return output