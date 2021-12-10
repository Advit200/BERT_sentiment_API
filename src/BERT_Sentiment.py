from transformers import pipeline
import pandas as pd
from DataProcessing import DataProcessor
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, classification_report,matthews_corrcoef

SENTIMENT_RESULT_INPUT = {"input": "../Output/Consolidated_Koch_review.xlsx"}
SENTIMENT_RESULT_OUTPUT = {
    "output": "../Output/koch_review_sentiment_result_trial.xlsx"}

# Sample is imbalanced . Ratio of positive reviews to neagtive is 3:1


class SentimentModel:
    row = 0

    def __init__(self):
        pass

    def __repr__(self):
        return "Main class for Sentiment Analysis"

    def _evaluate(self, df):
        # Evaluate the sentiment model based on the assumption that rating >= rating_threshold is positive.

        # actual = df["Rating"].apply(lambda x : 1 if x >= rating_threshold else 0).values
        # predicted = df["Sentiment"].apply(lambda x : 1 if x == "POSITIVE" else 0).values

        # confusion = confusion_matrix(actual,predicted)
        # accuracy = accuracy_score(actual,predicted)
        # precision = precision_score(actual,predicted)
        # recall = recall_score(actual,predicted)
        # f_score = f1_score(actual,predicted)

        # print(f"\n Accuracy of the model is : {accuracy:.2f}\n")
        # print(f"\n Precision of the model is : {precision:.2f}\n")
        # print(f"\n Recall of the model is : {recall:.2f}\n")
        # print(f"\n F1 score of the model is : {f_score:.2f}\n")
        # print(f"\n Confusion matrix  : {confusion}\n\n")

        actuals = df["Rating"].apply(
            lambda x: 0 if x <= 2 else 1 if x == 3 else 2).values

        predicted = df["Sentiment"].apply(
            lambda x: 0 if x == "NEGATIVE" else 1 if x == "NEUTRAL" else 2).values

        print(classification_report(actuals, predicted,
              target_names=["Negative", "Neutral", "Positive"]))

        print(f"\n\nMatthew's Correlation Coeff : {matthews_corrcoef(actuals,predicted):.2f}")

        return (actuals, predicted)

    def run_sentiment_analysis(self, df, col):
        
        MODEL = "cardiffnlp/twitter-roberta-base-sentiment"

        senti_pipeline = pipeline(
            "sentiment-analysis", model=MODEL)

        obj = DataProcessor(df, col)
        obj.PreProcessing()
        # obj.stopwords_removal()
        # obj.lemma()
        # obj.remove_common_words()
        # obj.stopwords_removal()

        def find_sentiment(text):
            try:
                sentiment = senti_pipeline(text)[0].get("label")
                print(
                    f"Sentiment assigned for row {self.row}/{len(df)} and sentiment is {sentiment}")
                self.row += 1
            except Exception as e:
                print(e)
                self.row += 1
                sentiment = "LABEL_1"

            return sentiment

        df = df.query('Review_len < 400')
        df.drop('Review_len',axis=1,inplace=True)

        df["Sentiment"] = df[col].apply(lambda text: find_sentiment(text))

        df["Sentiment"] = df["Sentiment"].map({"LABEL_0":"NEGATIVE" , "LABEL_1":"NEUTRAL" , "LABEL_2":"POSITIVE"})

        model_score = self._evaluate(df)

        print("\n\n<<<<<<<<<    SENTIMENT ANALYSIS SUCCESFULL     >>>>>>>>>>>>>>>>\n\n")
        return df


if __name__ == "__main__":
    sentiment = SentimentModel()
    df = pd.read_excel(SENTIMENT_RESULT_INPUT.get("input"), nrows=20)
    result_df = sentiment.run_sentiment_analysis(df, "Review")

    # result_df["Sentiment"] = result_df.apply(lambda df :["NEGATIVE" if df["Rating"]<=2 else df["Sentiment"]][0],axis=1)
    # result_df["Sentiment"] = result_df.apply(lambda df :["POSITIVE" if df["Rating"]==5 else df["Sentiment"]][0],axis=1)
    # result_df["Sentiment"] = result_df.apply(lambda df :["NEGATIVE" if ((df["Rating"]<=2) & (df["Sentiment"]=="")) else df["Sentiment"]][0],axis=1)
    # result_df["Sentiment"] = result_df.apply(lambda df :["POSITIVE" if ((df["Rating"]>=3) & (df["Sentiment"]=="")) else df["Sentiment"]][0],axis=1)

    result_df.to_excel(SENTIMENT_RESULT_OUTPUT.get("output"), index=False)


'''

0	negative
1	neutral
2	positive

'''
