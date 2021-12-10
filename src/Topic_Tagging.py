import pandas as pd
from DataProcessing import DataProcessor


def mapping_function(text):
    texts = text.lower().strip().split()
    topics = []
    for text in texts:
        if "management" in text:
            topics.append("Management")
        elif "manager" in text:
            topics.append("Managers")
        elif "supervisor" in text:
            topics.append("Supervisor")
        elif "mbm" in text or "principle" in text:
            topics.append("MBM")
        elif "leadership" in text or "leader" in text:
            topics.append("Leadership")
        elif (
            "culture" in text
            or "work" in text
            or "working" in text
            or "experience" in text
            or "people" in text
            or "life" in text
            or "hour" in text
            or "team" in text
            or "shift" in text
        ):
            topics.append("Work Culture")
        elif "internship" in text or "intern" in text:
            topics.append("Internship")
        elif "hiring" in text or "hire" in text or "interview" in text or "hr" in text:
            topics.append("Hiring")
        elif (
            "benefit" in text
            or "pay" in text
            or "salary" in text
            or "money" in text
            or "compensation" in text
        ):
            topics.append("Compensation/Benefit")

    topics = set(topics)

    if topics:
        return list(topics)
    else:
        return ["Others"]

def tag_Topic(df, col):
    
        df.dropna(subset=[col], inplace=True)

        df["Topics"] = df[col].map(mapping_function)
        df = df.explode("Topics")
        df.drop_duplicates(inplace=True)
        df.drop(["Review"], axis=1, inplace=True)
        df.dropna(subset=["Review_id"],inplace=True)
        # print(df["Topics"].value_counts())

        print(
            "\n\n<<<<<<<<<<<<<<<<<<<<<<<<   TOPIC ASSIGNMENT IS SUCCESFULL   >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n\n"
        )
        return df

if __name__ == "__main__":

    INPUT_PATH = {"input": "../Output/koch_review_sentiment_result.xlsx"}
    OUTPUT_PATH = {"output": "../Output/Final_PowerBI_input.xlsx"}

    df = pd.read_excel(INPUT_PATH.get("input"))
    tag_Topic(df, "Review")
