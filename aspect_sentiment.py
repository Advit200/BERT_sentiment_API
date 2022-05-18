import pandas as pd
from DataProcessing import DataProcessor
import aspect_based_sentiment_analysis as absa

SENTIMENT_RESULT_INPUT = {"input": "../Output/Consolidated_Koch_review.xlsx"}
SENTIMENT_RESULT_OUTPUT = {"output": "../Output/aspect_sentiment_result.xlsx"}


class AspectBasedSentimentModel:
    row = 0

    def __init__(self):
        self.nlp = absa.load()

    def __repr__(self):
        return "Main class for Sentiment Analysis"

    def _find_aspect_sentiment(self, text):

        final_sentiment_scores = {
            "Compensation": 0, "Hiring": 0, "MBM": 0, "Management": 0, "Work Culture": 0}

        sentiment_scores = {
            "people": -1,
            "work": -1,
            "management": -1,
            "mbm": -1,
            "salary": -1,
            "compensation": -1,
            "pay": -1,
            "benefit": -1,
            "culture": -1,
            "experience": -1,
            "hiring": -1,
            "interview": -1,
            "hr": -1
        }

        final_aspects = [
            topic for topic in sentiment_scores.keys() if topic in text]

        if final_aspects:

            completed_tasks = self.nlp(text, aspects=final_aspects)

            for key in completed_tasks.subtasks.keys():
                sentiment_scores[key] = completed_tasks.subtasks.get(
                    key).sentiment

            compensation_count = 0
            hiring_count = 0
            work_culture_count = 0
            mbm_count = 0
            management_count = 0

            for key in sentiment_scores.keys():
                if sentiment_scores[key] != -1:
                    if key in "pay,benefit,compensation,salary":
                        final_sentiment_scores["Compensation"] += sentiment_scores.get(
                            key)
                        compensation_count += 1
                    elif key in "hr,interview,hiring":
                        final_sentiment_scores["Hiring"] += sentiment_scores.get(
                            key)
                        hiring_count += 1
                    elif key in "people,work,experience,culture":
                        final_sentiment_scores["Work Culture"] += sentiment_scores.get(
                            key)
                        work_culture_count += 1
                    elif key in "mbm":
                        final_sentiment_scores["MBM"] += sentiment_scores.get(
                            key)
                        mbm_count += 1
                    elif key in "management":
                        final_sentiment_scores["Management"] += sentiment_scores.get(
                            key)
                        management_count += 1
                else:
                    pass

            final_sentiment_scores["Compensation"] = final_sentiment_scores["Compensation"] // compensation_count if (
                final_sentiment_scores["Compensation"] != 0 and compensation_count != 0) else 0 if (final_sentiment_scores["Compensation"] == 0 and compensation_count != 0) else -1

            final_sentiment_scores["Hiring"] = final_sentiment_scores["Hiring"] // hiring_count if (
                final_sentiment_scores["Hiring"] != 0 and hiring_count != 0) else 0 if (final_sentiment_scores["Hiring"] == 0 and hiring_count != 0) else -1

            final_sentiment_scores["Management"] = final_sentiment_scores["Management"] // management_count if (
                final_sentiment_scores["Management"] != 0 and management_count != 0) else 0 if (final_sentiment_scores["Management"] == 0 and management_count != 0) else -1

            final_sentiment_scores["MBM"] = final_sentiment_scores["MBM"] // mbm_count if (
                final_sentiment_scores["MBM"] != 0 and mbm_count != 0) else 0 if (final_sentiment_scores["MBM"] == 0 and mbm_count != 0) else -1
                
            final_sentiment_scores["Work Culture"] = final_sentiment_scores["Work Culture"] // work_culture_count if (
                final_sentiment_scores["Work Culture"] != 0 and work_culture_count != 0) else 0 if (final_sentiment_scores["Work Culture"] == 0 and work_culture_count != 0) else -1

            return final_sentiment_scores

        else:
            return {"Compensation": -1, "Hiring": -1, "MBM": -1, "Management": -1, "Work Culture": -1}

    def run_aspect_sentiment_analysis(self, df, col):
        obj = DataProcessor(df, col)
        obj.PreProcessing()
        obj.stopwords_removal()

        try:
            for i in range(len(df)):

                sentiment_result = self._find_aspect_sentiment(
                    df.loc[i, "Review"])

                df.loc[i, "Compensation_sentiment"] = sentiment_result["Compensation"]
                df.loc[i, "Hiring_sentiment"] = sentiment_result["Hiring"]
                df.loc[i, "MBM_sentiment"] = sentiment_result["MBM"]
                df.loc[i, "Management_sentiment"] = sentiment_result["Management"]
                df.loc[i, "Work Culture_sentiment"] = sentiment_result["Work Culture"]

                print(f"Running for row : {self.row}/{len(df)}")
                self.row += 1

            print(
                "\n\n<<<<<<<<<    SENTIMENT ANALYSIS SUCCESFULL     >>>>>>>>>>>>>>>>\n\n")
            return df

        except Exception as e:
            print(e)
            return "ERROR"


if __name__ == "__main__":

    sentiment = AspectBasedSentimentModel()
    df = pd.read_excel(SENTIMENT_RESULT_INPUT.get("input"))
    result_df = sentiment.run_aspect_sentiment_analysis(df, "Review")
    result_df.to_excel(SENTIMENT_RESULT_OUTPUT.get("output"), index=False)


'''

sentiment_mapping = {
                   -1:"NO SENTIMENT",
                    0:"NEUTRAL",
                    1:"NEGATIVE",
                    2:"POSITIVE" 
                    }

'''
