from torch import nn
import config
import re
import numpy as np


class BERTModel:

    def __init__(self, text):
        self.text = text
        self.main_text = text

    def __repr__(self):
        return "Main class for BERT Sentiment Analysis"

    def __len__(self):
        return len(self.text)

    @property
    def _preprocessing(self):
        self.text = str(self.text).lower().strip()
        self.text = re.sub(
            '[!"#$%&\'\\()*+,-./:;<=>?@[\]^_`{|}~]', '', self.text)
        
        return self.text

    @property
    def get_sentiment(self):

        try:

            if type(self.text) == str:

                self.text = self._preprocessing

                encoding = config.TOKENIZER.encode_plus(self.text, max_length=config.MAX_LEN, add_special_tokens=True, truncation=True,
                                                        padding='max_length', return_attention_mask=True, return_token_type_ids=False, return_tensors="pt")

                model_output = config.MODEL(
                    input_ids=encoding['input_ids'], attention_mask=encoding['attention_mask'])

                prob_ = nn.functional.softmax(model_output, dim=1)

                return {
                        "TEXT"    : self.main_text,
                        "POSITIVE": np.round(prob_[0][2].item(), 3),
                        "NEUTRAL" : np.round(prob_[0][1].item(), 3), 
                        "NEGATIVE": np.round(prob_[0][0].item(), 3)
                        }
            
            else:
                return {"ERROR":"Provide valid string input."}

        except Exception as e:

            print(e)
            return {"ERROR":"Model failed to run.Contact aditya.gaurav@kochgs.com for support"}




if __name__ == "__main__":

    # input_text = "Aditya is a nice GUY. Good from HeArt 4235235 &*&**(!#&())+><.HE has killed 10 people and murdered them"
    input_text = "Aditya is a nice GUY."
    # input_text = 123

    obj = BERTModel(input_text)
    result = obj.get_sentiment
    print(result)
