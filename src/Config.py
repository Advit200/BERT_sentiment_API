
###########################################################################################
COMPANIES_LIST = ["Koch-Industries", "Molex", "Georgia--pacific",
                  "Guardian-Industries", "Flint-Hills-Resources", "Invista", "OnPoint", "Koch Glitsch", "Optimized Process Design", "DarkVision","John Zink Hamworthy","Genesis Robotics","Koch Knight","Sentient Energy","KBS","KTC","Koch Chemical Technology"]

# List of all companies for Indeed scraping.

indeed_companies_dict = {
    "Koch-Industries":  {"page_count": 37,
                         "file_location": "../Input/Indeed/Koch.xlsx"},
    "Molex": {"page_count": 34,
              "file_location": "../Input/Indeed/Molex.xlsx"},
    "Georgia--pacific": {"page_count": 167,
                         "file_location": "../Input/Indeed/GP.xlsx"},
    "Invista": {"page_count": 29,
                "file_location": "../Input/Indeed/Invista.xlsx"},
    "Flint-Hills-Resources": {"page_count": 15,
                              "file_location": "../Input/Indeed/FHR.xlsx"},
    "Guardian-Industries": {"page_count": 42,
                            "file_location": "../Input/Indeed/Guardian.xlsx"}

}

###########################################################################################

# Parameters for BERT Sentiment Analysis code input

SENTIMENT_RESULT_INPUT = {"input": "../Output/Consolidated_Koch_review.xlsx"}
SENTIMENT_RESULT_OUTPUT = {
    "output": "../Output/koch_review_sentiment_result.xlsx"}

##########################################################################################

# Parameters for Data Loader code input.

FILE_INPUT_PATHS = {
    "indeed_Koch-Industries": "../Input/Indeed/Koch.xlsx",
    "indeed_Molex": "../Input/Indeed/Molex.xlsx",
    "indeed_Georgia--pacific": "../Input/Indeed/GP.xlsx",
    "indeed_Guardian-Industries": "../Input/Indeed/Guardian.xlsx",
    "indeed_Flint-Hills-Resources": "../Input/Indeed/FHR.xlsx",
    "indeed_Invista": "../Input/Indeed/Invista.xlsx",

    "glassdoor_Flint-Hills-Resources": "../Input/Glassdoor/glassdoor_FHR.csv",
    "glassdoor_Georgia--pacific": "../Input/Glassdoor/glassdoor_GP.csv",
    "glassdoor_Molex": "../Input/Glassdoor/glassdoor_MOLEX.csv",
    "glassdoor_Invista": "../Input/Glassdoor/glassdoor_INVISTA.csv",
    "glassdoor_Guardian-Industries": "../Input/Glassdoor/glassdoor_GUARDIAN.csv",
    "glassdoor_Koch-Industries": "../Input/Glassdoor/glassdoor_KOCH.csv",
    "glassdoor_OnPoint": "../Input/Glassdoor/glassdoor_ONPOINT.csv",
    "glassdoor_Koch Glitsch": "../Input/Glassdoor/glassdoor_KOCHGLITSCH.csv",
    "glassdoor_Optimized Process Design": "../Input/Glassdoor/glassdoor_OPTIMIZED-PROCESS-DESIGNS.csv",
    "glassdoor_DarkVision": "../Input/Glassdoor/glassdoor_DARKVISION.csv",
    "glassdoor_John Zink Hamworthy": "../Input/Glassdoor/glassdoor_JOHN_ZINK.csv",
    "glassdoor_Genesis Robotics": "../Input/Glassdoor/glassdoor_GENESIS-ROBOTICS.csv",
    "glassdoor_Koch Knight": "../Input/Glassdoor/glassdoor_KOCHKNIGHT.csv",
    "glassdoor_Sentient Energy": "../Input/Glassdoor/glassdoor_SENTIENT_ENERGY.csv",

    "google": "../Input/Google/google.csv",

    # "ambitionbox_Koch-Industries": "../Input/AmbitionBox/ambitionbox_KOCH_INDUSTRIES.csv",
    "ambitionbox_KBS": "../Input/AmbitionBox/ambitionbox_KOCH-BUSINESS-SOLUTIONS.csv",
    "ambitionbox_Koch Chemical Technology": "../Input/AmbitionBox/ambitionbox_KOCH-CHEMICAL-TECHNOLOGY-GROUP-INDIA.csv",
    "ambitionbox_Koch Glitsch": "../Input/AmbitionBox/ambitionbox_KOCH-GLITSCH.csv",
    "ambitionbox_Invista": "../Input/AmbitionBox/ambitionbox_KOCH-INVISTA.csv",
    "ambitionbox_John Zink Hamworthy": "../Input/AmbitionBox/ambitionbox_KOCH-JOHN-ZINK.csv",
    "ambitionbox_Optimized Process Design": "../Input/AmbitionBox/ambitionbox_KOCH-OPTIMIZED-PROCESS-DESIGNS.csv",
    # "ambitionbox_KTC": "../Input/AmbitionBox/ambitionbox_KTC.csv",
    "ambitionbox_Molex": "../Input/AmbitionBox/ambitionbox_MOLEX.csv",
    "ambitionbox_Guardian-Industries": "../Input/AmbitionBox/ambitionbox_GUARDIAN.csv"

}

FILE_OUTPUT = {"output": "../Output/Consolidated_Koch_review.xlsx"}

##########################################################################################

# Parameters for Topic Tagging code input

TOPIC_INPUT_PATH = {"input": "../Output/koch_review_sentiment_result.xlsx"}
TOPIC_OUTPUT_PATH = {"output": "../Output/Final_PowerBI_input.xlsx"}


###########################################################################################

# Glassdoor scraping code parameters.

GLASSDOOR_KOCH = {
    "Date_difference": 0,
    "Limit": 0,
    'fileLocation': "../Input/Glassdoor/glassdoor_KOCH.csv"
}
GLASSDOOR_FHR = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Flint-Hills-Resources-EI_IE15788.11,32.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_FHR.csv",
    "Limit": 0,
}
GLASSDOOR_GP = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Georgia-Pacific-EI_IE284.11,26.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_GP.csv",
    "Limit": 0,
}
GLASSDOOR_MOLEX = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Molex-EI_IE1666.11,16.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_MOLEX.csv",
    "Limit": 0,
}

GLASSDOOR_INVISTA = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-INVISTA-EI_IE19024.11,18.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_INVISTA.csv",
    "Limit": 0,
}

GLASSDOOR_GUARDIAN = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Guardian-Industries-EI_IE2809.11,30.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_GUARDIAN.csv",
    "Limit": 0,
}

GLASSDOOR_John_Zink_Hamworthy = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-John-Zink-Hamworthy-Combustion-EI_IE3008129.11,41.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_JOHN_ZINK.csv",
    "Limit": 0,
}
GLASSDOOR_Koch_Knight = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Koch-Knight-EI_IE3065269.11,22.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_KOCHKNIGHT.csv",
    "Limit": 0,
}
GLASSDOOR_OnPoint = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-OnPoint-EI_IE3216238.11,18.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_ONPOINT.csv",
    "Limit": 0,
}
GLASSDOOR_Optimized_Process_Designs = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Optimized-Process-Designs-EI_IE1627950.11,36.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_OPTIMIZED-PROCESS-DESIGNS.csv",
    "Limit": 0,
}
GLASSDOOR_Sentient_Energy = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Sentient-Energy-EI_IE453768.11,26.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_SENTIENT_ENERGY.csv",
    "Limit": 0,
}
GLASSDOOR_Genesis_Robotics = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Genesis-Robotics-EI_IE3685231.11,27.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_GENESIS-ROBOTICS.csv",
    "Limit": 0,
}
GLASSDOOR_Koch_Glitsch = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-Koch-Glitsch-EI_IE2600516.11,23.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_KOCHGLITSCH.csv",
    "Limit": 0,
}
GLASSDOOR_Koch_DarkVision = {
    "url": 'https://www.glassdoor.co.in/Overview/Working-at-DarkVision-EI_IE3579098.11,21.htm',
    "fileLocation": "../Input/Glassdoor/glassdoor_DARKVISION.csv",
    "Limit": 0,
}

###########################################################################################

# AWS configuration 

import os

aws_id = os.environ.get("aws_id")
aws_secret = os.environ.get("aws_secret")
s3_region_name = 'us-east-1'
s3_bucket_name = "bitter-sweet-proj"
s3_key="PowerBI_Input_File.csv"

###########################################################################################
# SES Email Configuration.

SOURCE = "aditya.gaurav@kochgs.com"
RECIPIENT_LIST = ["karthikeyan.chandrasekar@kochgs.com","aditya.gaurav@kochgs.com"]
FAILURE_RECIPIENT_LIST = ["aditya.gaurav@kochgs.com","karthikeyan.chandrasekar@kochgs.com"]
DEVELOPER_RECIPIENT_LIST = ["aditya.gaurav@kochgs.com","karthikeyan.chandrasekar@kochgs.com"]
