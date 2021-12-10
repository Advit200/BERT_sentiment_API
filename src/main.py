import pandas as pd
from IndeedScraping import IndeedScraper,IndeedPreprocessing
import datetime
from BERT_Sentiment import SentimentModel
from DataLoader import DataLoader
from Topic_Tagging import tag_Topic
import time
import Config
import os
from datetime import date
# from S3_upload import upload_file_to_s3
# from SES_triger import send_mail,send_developer_mail

indeed__scraping_result = {}

def indeedScraping(company,page_count,file_location):
    print(f"\n<<<<<<<<<<<     SCRAPING STARTED FOR {company}    >>>>>>>>>>>>>>>>>>>>>>>>\n")
    obj = IndeedScraper(company=company,page_count=page_count)
    final_df = obj.main()
    final_df.to_excel(f"../Output/indeed_{company}_review_raw.xlsx", index=False)
    PreProcesses_obj = IndeedPreprocessing()
    processed_df = PreProcesses_obj._preProcessDF(
        pd.read_excel(f"../Output/indeed_{company}_review_raw.xlsx")
    )
    processed_df.to_excel(file_location, index=False)

    print(f"\n\n<<<<<<<<<<<     SCRAPING COMPLETED FOR {company}    >>>>>>>>>>>>>>>>>>>>>>>>\n\n")
    return processed_df

def glassdoor_scraping_KOCH(date_difference, file_location, limit):
    execString = 'python ./glassdoor/glassdoorScrapper.py --file ' + \
        str(file_location)
    if limit != 0:
        execString = execString + " --limit " + str(limit)
    if date_difference == 0:
        os.system(execString)
    else:
        execString = execString + " --max_date " + str(date.today(
        ).year)+'-'+str(date.today().month)+'-'+str(date.today().day) + ' --min_date ' + str(date.today(
        ).year)+'-'+str(date.today().month)+'-'+str(date.today().day-date_difference)
        os.system(execString)


def glassdoor_scraping_differentCompanies(url, file_location, limit):
    execString = 'python ./glassdoor/glassdoorScrapper.py --file ' + \
        str(file_location)+' --url '+str(url)
    if limit != 0:
        execString = execString + " --limit " + str(limit)
    os.system(execString)


def google_scraping():
    os.system('python ./google/googleReviewScrapper.py')


def consolidate_data(FILE_INPUT_PATHS, FILE_OUTPUT):
    obj = DataLoader(FILE_INPUT_PATHS, FILE_OUTPUT)
    output = obj.consolidating_reviews()
    return output


def run_sentiment_analysis(SENTIMENT_RESULT_INPUT, SENTIMENT_RESULT_OUTPUT):
    sentiment = SentimentModel()
    df = pd.read_excel(SENTIMENT_RESULT_INPUT.get("input"))
    result_df = sentiment.run_sentiment_analysis(df, "Review")

    result_df.to_excel(SENTIMENT_RESULT_OUTPUT.get("output"), index=False)
    return result_df


def find_topic(INPUT_PATH, OUTPUT_PATH):
    df = pd.read_excel(INPUT_PATH.get("input"))
    df = tag_Topic(df, "Review")

    def _clean_df(df,col):
        df[col] = df[col].str.replace(r"'|\"|\"|'", "",regex=True)
        return df[col]

    cols = ["Title","Pros","Cons","Main_Review"]

    for col in cols:
        df[col] = _clean_df(df,col)    

    df.to_excel(OUTPUT_PATH.get("output"),index=False)

    return df


def df_stats(df):
    
    try:
        print(df.groupby(["Source","Company"])["Review_id"].count())
        print(f"\nTotal number of Reviews : {len(df['Review_id'].unique())}\n")

        today_date = datetime.datetime.today()
        one_week_past_date = today_date - datetime.timedelta(7)
        one_month_past_date = today_date - datetime.timedelta(30)

        df_week  = df.loc[df["Review_Posting_Date"].between(one_week_past_date,today_date) , :]
        week_review = df_week["Review_Posting_Date"].value_counts().sum()

        df_month  = df.loc[df["Review_Posting_Date"].between(one_month_past_date,today_date) , :]
        month_review = df_month["Review_Posting_Date"].value_counts().sum()  

        print(f"Total reviews in last week : {week_review}")
        print(f"\nTotal reviews in last month : {month_review}\n")

    except:
        print("Error while consolidating the data.")

def run_all():
        start = time.time()

        for company,metadata in Config.indeed_companies_dict.items():
            output = indeedScraping(company=company,page_count=metadata["page_count"],file_location=metadata["file_location"])
            indeed__scraping_result[company] = len(output)

        # glassdoor_scraping_KOCH(
        #     date_difference=Config.GLASSDOOR_KOCH['Date_difference'], file_location=Config.GLASSDOOR_KOCH['fileLocation'], limit=Config.GLASSDOOR_KOCH['Limit'])
        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_FHR['url'], file_location=Config.GLASSDOOR_FHR['fileLocation'], limit=Config.GLASSDOOR_FHR['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_GP['url'], file_location=Config.GLASSDOOR_GP['fileLocation'], limit=Config.GLASSDOOR_GP['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_MOLEX['url'], file_location=Config.GLASSDOOR_MOLEX['fileLocation'], limit=Config.GLASSDOOR_MOLEX['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_INVISTA['url'], file_location=Config.GLASSDOOR_INVISTA['fileLocation'], limit=Config.GLASSDOOR_INVISTA['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_GUARDIAN['url'], file_location=Config.GLASSDOOR_GUARDIAN['fileLocation'], limit=Config.GLASSDOOR_GUARDIAN['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_John_Zink_Hamworthy['url'], file_location=Config.GLASSDOOR_John_Zink_Hamworthy['fileLocation'], limit=Config.GLASSDOOR_John_Zink_Hamworthy['Limit'])

        # glassdoor_scraping_differentCompanies(
        #     url=Config.GLASSDOOR_Koch_Knight['url'], file_location=Config.GLASSDOOR_Koch_Knight['fileLocation'], limit=Config.GLASSDOOR_Koch_Knight['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_OnPoint['url'], file_location=Config.GLASSDOOR_OnPoint['fileLocation'], limit=Config.GLASSDOOR_OnPoint['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_Optimized_Process_Designs['url'], file_location=Config.GLASSDOOR_Optimized_Process_Designs['fileLocation'], limit=Config.GLASSDOOR_Optimized_Process_Designs['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_Sentient_Energy['url'], file_location=Config.GLASSDOOR_Sentient_Energy['fileLocation'], limit=Config.GLASSDOOR_Sentient_Energy['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_Genesis_Robotics['url'], file_location=Config.GLASSDOOR_Genesis_Robotics['fileLocation'], limit=Config.GLASSDOOR_Genesis_Robotics['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_Koch_Glitsch['url'], file_location=Config.GLASSDOOR_Koch_Glitsch['fileLocation'], limit=Config.GLASSDOOR_Koch_Glitsch['Limit'])

        # glassdoor_scraping_differentCompanies(url=Config.GLASSDOOR_Koch_DarkVision['url'], file_location=Config.GLASSDOOR_Koch_DarkVision['fileLocation'], limit=Config.GLASSDOOR_Koch_DarkVision['Limit'])

        print("\n\n<<<<<<<<<    ALL SCRAPING COMPLETED   >>>>>>>>>>>>>>>>>>>\n\n")

        consolidated_df = consolidate_data(FILE_INPUT_PATHS=Config.FILE_INPUT_PATHS,
                         FILE_OUTPUT=Config.FILE_OUTPUT)
        
        df_stats(consolidated_df)

        run_sentiment_analysis(SENTIMENT_RESULT_INPUT=Config.SENTIMENT_RESULT_INPUT,
                               SENTIMENT_RESULT_OUTPUT=Config.SENTIMENT_RESULT_OUTPUT)

        final_df = find_topic(INPUT_PATH=Config.TOPIC_INPUT_PATH,
                   OUTPUT_PATH=Config.TOPIC_OUTPUT_PATH)

        print(f"\nTotal number of unique rows : {len(final_df['Review_id'].unique())}\n")

        # df_size = len(final_df["Review_id"].unique())

        # upload_status =  upload_file_to_s3(file_name=Config.TOPIC_OUTPUT_PATH["output"],bucket_name=Config.s3_bucket_name,key=Config.s3_key)

        # if upload_status["uploaded"]:
        #     time.sleep(2) 
        #     send_developer_mail(recipient_list=Config.DEVELOPER_RECIPIENT_LIST,source=Config.SOURCE,dataset_details=indeed__scraping_result,df_size=df_size)
        #     send_mail(recipient_list=Config.RECIPIENT_LIST,source=Config.SOURCE,template_name="Bitter-Sweet-Success")
        # else:
        #     send_mail(recipient_list=Config.FAILURE_RECIPIENT_LIST,source=Config.SOURCE,template_name="Bitter-Sweet-Failure")


        end = time.time()

        print(
            f"\n\n <<<<<<<<   TIME TAKEN TO RUN: {(end-start)/60:.2f} mins   >>>>>>>>>>>>>>>>>\n")


if __name__ == "__main__":

    run_all()
