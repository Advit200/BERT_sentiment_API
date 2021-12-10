import pandas as pd
import numpy as np
import nltk
import gensim.corpora as corpora
# import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import PorterStemmer
import gensim
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

''' Comment the below 3 lines after first run of this file'''
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# stopwords = nltk.download("stopwords")


class DataProcessor:
    """
    Class containing all the methods for pre processing the text data before using as input for LDA Model.

    Input   : df  = DataFrame object
              col = Column name which needs to be preprocessed
    Output  : Processed Column Series

    """

    def __init__(self, df, col):
        self.df = df
        self.col = col

    def __repr__(self):
        return "PreProcessing class for model"

    def PreProcessing(self):

        self.df[self.col] = self.df[self.col].str.replace(r"'|\"|\"|'|!|\d+|\s+", " ",regex=True)
        self.df[self.col] = self.df[self.col].str.strip().str.lower()
        self.df.dropna(subset=[self.col], inplace=True)
        self.df.reset_index(drop=True,inplace=True)
        return self.df[self.col]

    '''
        NOTE : Using lemmatization provide better result than using stemming for LDA modelling but is computionally expensive and takes longer to run.
    # '''

    # def lemmatization(self,allowed_postags=["ADV", "NOUN", "ADJ", "VERB"]):
    #     def _lemma_function(texts):
    #         nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    #         doc = nlp(texts)
    #         lemma_text = " ".join(
    #             [token.lemma_ for token in doc if (token.pos_ in allowed_postags and len(token.lemma_) > 2)]
    #         )
    #         return lemma_text

    #     self.df[self.col] = self.df[self.col].apply(lambda texts: _lemma_function(texts))
    #     return self.df[self.col]


    def _pos_tagger(self):
        self.df[self.col] = self.df[self.col].apply(lambda texts: texts.split())
        self.df[self.col] = self.df[self.col].apply(lambda text_list : nltk.pos_tag(text_list))
        
        def wordnet_pos_tager(tag):
            if tag[1].startswith("J"):
                return wordnet.ADJ
            elif tag[1].startswith("V"):
                return wordnet.VERB
            elif tag[1].startswith("N"):
                return wordnet.NOUN
            elif tag[1].startswith("R"):
                return wordnet.ADV
            else:
                return None
        
        self.df[self.col] = self.df[self.col].apply(lambda tagged_text : [(word[0],wordnet_pos_tager(word)) for word in tagged_text])
        
        return self.df[self.col] 


    def lemma(self):
        self._pos_tagger()
        lemma = WordNetLemmatizer()
        self.df[self.col]  = self.df[self.col].apply(lambda texts_list :" ".join([lemma.lemmatize(word[0],pos=word[1]) for word in texts_list if (word[1]!=None and len(word[0]) >= 2)]))
       
        return self.df[self.col] 


    def stopwords_removal(self):
        stopwords_list = stopwords.words("english")
        stopwords_list.extend(
            [
                "make",
                "thing",
                "just",
                "area",
                "say",
                "new",
                "run",
                "lot",
                "day",
                "end",
                "got",
                "way",
                "let",
                "koch",
                "tax",
                "come"
                
            ]
        )
        self.df[self.col] = self.df[self.col].apply(lambda texts: texts.split())

        self.df[self.col] = self.df[self.col].apply(
            lambda texts: " ".join(
                [text.strip() for text in texts if text not in stopwords_list]
            )
        )

        return self.df[self.col]

    def stemming(self):
        porter = PorterStemmer()
        self.df[self.col] = self.df[self.col].apply(lambda texts: texts.split())
        self.df[self.col] = self.df[self.col].apply(
            lambda texts: " ".join(
                [porter.stem(text) for text in texts if len(porter.stem(text)) > 2]
            )
        )

        return self.df[self.col]

    def creating_bigrams(self):

        # data_words is a list of lists.Each inner list contains all text of that particular row
        data_words = []
        self.df[self.col] = self.df[self.col].apply(
            lambda texts: data_words.append(texts.split())
        )

        # min_count hyperparameter : Ignore all words and bigrams with total collected count lower than this value.
        bigram = gensim.models.Phrases(data_words, min_count=50)
        bigram_model = gensim.models.phrases.Phraser(bigram)

        for i in range(0, len(data_words)):
            self.df.loc[i, self.col] = " ".join(bigram_model[data_words[i]])
        self.df.dropna(subset=[self.col], inplace=True)

        return self.df[self.col]

    def remove_common_words(self):

        # min_df = 5 means "ignore terms that appear in less than 5 documents".
        tfidf = TfidfVectorizer(stop_words="english", min_df=10) # has a parameter to perform ngram here itself (ngram_range=(1,2))
        tfidf_matrix = tfidf.fit_transform(self.df[self.col]) # Use tfidf_matrix.A to view that sparse matrix.
        transformed_matrix = tfidf.inverse_transform(tfidf_matrix)
        for i in range(0, len(transformed_matrix)):
            self.df.loc[i, self.col] = " ".join(transformed_matrix[i])

        return self.df[self.col]

    def id2word_corpus_creator(self):

        # data_words is a list of lists.Each inner list contains all text of that particular row
        data_words = []
        self.df[self.col] = self.df[self.col].apply(
            lambda texts: data_words.append(texts.split())
        )
        # id2word maps words to integers.Its like Bag of words but returns gensim dictionary object.
        id2word = corpora.Dictionary(data_words)

        # doc2bow creates a tuple of word_id and occurance count.It is like CountVectorizer.
        # Corpus is a list of lists.Inner list contains the doc2bow returned tuple.
        corpus = [id2word.doc2bow(text) for text in data_words]

        return (id2word, corpus, data_words)


if __name__ == "__main__":

    INPUT_PATH = {"input": "../Output/Consolidated_Koch_review.xlsx"}
    OUTPUT_PATH = {"output": "../Output/Cleaned_consolidated_review.xlsx"}

    df = pd.read_excel(INPUT_PATH.get("input"))
    obj = DataProcessor(df, "Review")
    col_out1 = obj.PreProcessing()
    col_out2 = obj.stopwords_removal()
    col_out3 = obj.stemming()
    col_out4 = obj.creating_bigrams()
    col_out5 = obj.remove_common_words()
    col_out6 = obj.stopwords_removal()
    result = obj.id2word_corpus_creator()

    # print(result)
