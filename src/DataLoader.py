import pandas as pd
import numpy as np
from City_country_mapping import cities_country_mapping
from fuzzywuzzy import fuzz
from datetime import datetime
import Config


class DataLoader:

    def __init__(self, FILE_INPUT_PATHS, FILE_OUTPUT):
        """
        This class has consolidating_reviews method that takes the documents present
        under input path mentioned under FILE_INPUT_PATHS dict and consolidate them
        into one simgle excel file and save it under path mentioned under FILE_OUTPUT dict.

        Input  : FILE_INPUT_PATHS dict having file name as key and path as value
        Output : FILE_OUTPUT dict having "output" as key and path as value

        """
        self.FILE_INPUT_PATHS = FILE_INPUT_PATHS
        self.FILE_OUTPUT = FILE_OUTPUT
        self.indeed_all_df = pd.DataFrame()
        self.glassdoor_all_df = pd.DataFrame()
        self.ambitionbox_all_df = pd.DataFrame()

    def __repr__(self):
        return "Data laoder for sentiment analysis model"

    def _designation_assignment(self, text):

        designations_list = [
            "Anonymous",
            "Assistant Manager",
            "Financial Analyst",
            "Accountant",
            "Analyst",
            "Software Developer",
            "Human Resource",
            "Welder",
            "Mechanical",
            "Project Engineer",
            "Manager",
            "Designer",
            "Intern",
            "Talent Acquisition",
            "Supervisor",
            "Admnistrator",
            "Service Desk",
            "Data Architect",
            "Test Engineer",
            "Electronics Engineer",
            "Project Coordinator",
            "Plant Manager",
            "Plant Operator",
            "Audit Senior",
            "Boilermaker",
            "Safety Coordinator",
            "Director",
        ]

        for designation in designations_list:
            score = fuzz.token_sort_ratio(text, designation)
            if score > 50:
                return designation

    def consolidating_reviews(self):

        try:
            ######################    INDEED DATAFRAMES     #################################################

            def indeed_dataframe_function(company):
                if self.FILE_INPUT_PATHS.get(f'indeed_{company}'):
                    try:
                        df_indeed = pd.read_excel(
                            self.FILE_INPUT_PATHS.get(f'indeed_{company}'),
                            usecols=[
                                "Title",
                                "Rating",
                                "Main_Review",
                                "User_Designation",
                                "Employeer Status",
                                "Review_Posting_Date",
                                "User_city",
                                "User_State",
                                "Pros",
                                "Cons",
                                "Koch_Response",
                                "Koch_Response_Date",
                                "helpful_yes",
                                "helpful_no",
                            ]
                        )
                        df_indeed[
                            [
                                "Country",
                                "Advice_to_Mgmt",
                                "recommends",
                                "positive_outlook",
                                "approves_of_CEO",
                            ]
                        ] = None

                        df_indeed["Source"] = "Indeed"
                        df_indeed["Company"] = company

                        self.indeed_all_df = pd.concat(
                            [self.indeed_all_df, df_indeed], axis=0, ignore_index=True)

                        return df_indeed

                    except Exception as e:
                        print(e)
                        print(f"error in indeed in company : {company}")
                else:
                    pass
                

            ######################    GLASSDOOR DATAFRAMES     #################################################

            def glassdoor_dataframe_function(company):
                if self.FILE_INPUT_PATHS.get(f"glassdoor_{company}"):
                    try:
                        df_glassdoor = pd.read_csv(
                            self.FILE_INPUT_PATHS.get(f"glassdoor_{company}"),
                            usecols=[
                                "employee_title",
                                "City",
                                "Country",
                                "employee_status",
                                "review_title",
                                "rating_overall",
                                "date",
                                "pros",
                                "cons",
                                "advice_to_mgmt",
                                "helpful",
                                "recommends",
                                "positive_outlook",
                                "approves_of_CEO",
                                "response"
                            ]
                        )
                        df_glassdoor.rename(
                            columns={
                                "employee_title": "User_Designation",
                                "City": "User_city",
                                "employee_status": "Employeer Status",
                                "review_title": "Title",
                                "rating_overall": "Rating",
                                "date": "Review_Posting_Date",
                                "pros": "Pros",
                                "cons": "Cons",
                                "advice_to_mgmt": "Advice_to_Mgmt",
                                "helpful": "helpful_yes",
                                "response":"Koch_Response"
                            },
                            inplace=True,
                        )
                        df_glassdoor[
                            [
                                "Main_Review",
                                "User_State",
                                "Koch_Response_Date",
                                "helpful_no",
                            ]
                        ] = None

                        df_glassdoor["Source"] = "Glassdoor"
                        df_glassdoor["Company"] = company

                        self.glassdoor_all_df = pd.concat(
                            [self.glassdoor_all_df, df_glassdoor], axis=0, ignore_index=True)

                        return df_glassdoor
                    
                    except Exception as e:
                        print(e)
                        print(f"error in glassdoor in company : {company}")
                else:
                    pass


            ######################    GOOGLE DATAFRAMES     #################################################
            try:
                df_google = pd.read_csv(
                    self.FILE_INPUT_PATHS.get("google"),
                    usecols=[
                        "ReviewRating",
                        "ReviewDate",
                        "State",
                        "Country",
                        "ReviewDescription",
                    ]
                )
                df_google.rename(
                    columns={
                        "State": "User_State",
                        "ReviewRating": "Rating",
                        "ReviewDate": "Review_Posting_Date",
                        "ReviewDescription": "Main_Review",
                    },
                    inplace=True,
                )
                df_google[
                    [
                        "User_city",
                        "User_Designation",
                        "Employeer Status",
                        "Title",
                        "Pros",
                        "Cons",
                        "Advice_to_Mgmt",
                        "Koch_Response",
                        "Koch_Response_Date",
                        "helpful_yes",
                        "helpful_no",
                        "recommends",
                        "positive_outlook",
                        "approves_of_CEO",
                    ]
                ] = None
                df_google["Source"] = "Google"
                df_google["Company"] = "Koch-Industries"
            
            except Exception as e:
                print(e)
                print("error in google.")

            ######################    AMBITIONBOX DATAFRAMES     #################################################

            def ambitionbox_dataframe_function(company):
                if self.FILE_INPUT_PATHS.get(f"ambitionbox_{company}"):
                    try:
                        df_ambitionbox = pd.read_csv(
                            self.FILE_INPUT_PATHS.get(f"ambitionbox_{company}"),
                            usecols=[
                                "ReviewDate",
                                "WorkLocation",
                                "EmploymentStatus",
                                "ReviewerPost",
                                "EmployeeOverallRating",
                                "EmployeePros",
                                "EmployeeCons",
                                "ReviewLikes",
                                "ReviewDislikes",
                                "EmployeeWork"
                            ]
                        )
                        df_ambitionbox.rename(
                            columns={
                                "ReviewerPost": "User_Designation",
                                "WorkLocation": "User_city",
                                "EmploymentStatus": "Employeer Status",                            
                                "EmployeeOverallRating": "Rating",
                                "ReviewDate": "Review_Posting_Date",
                                "EmployeePros": "Pros",
                                "EmployeeCons": "Cons",
                                "ReviewLikes": "helpful_yes",
                                "ReviewDislikes":"helpful_no",
                                "EmployeeWork":"Main_Review"
                                
                            },
                            inplace=True,
                        )
                        df_ambitionbox[
                            [
                                "User_State",                            
                                "Title",                
                                "Advice_to_Mgmt",
                                "Koch_Response",
                                "Koch_Response_Date",
                                "helpful_no",
                                "recommends",
                                "positive_outlook",
                                "approves_of_CEO"
                            ]
                        ] = None

                        df_ambitionbox["Source"] = "Ambitionbox"
                        df_ambitionbox["Company"] = company

                        self.ambitionbox_all_df = pd.concat(
                            [self.ambitionbox_all_df, df_ambitionbox], axis=0, ignore_index=True)
                        
                        return df_ambitionbox
                    
                    except Exception as e:
                        print(e)
                        print(f"error in ambitionbox in company : {company}")
                
                else:
                    pass

            ######################    DATA CONSOLIDATION AND CLEANING    #####################################################

            for company in Config.COMPANIES_LIST:
                indeed_dataframe_function(company)
                glassdoor_dataframe_function(company)
                ambitionbox_dataframe_function(company)

            df_consolidated = pd.concat(
                [self.indeed_all_df, self.glassdoor_all_df, self.ambitionbox_all_df], axis=0, ignore_index=True)

            df_consolidated["Review_Posting_Date"] = pd.to_datetime(
                df_consolidated["Review_Posting_Date"])

            df_consolidated.drop_duplicates(inplace=True) # This is done before combining google df because there are lot of reviews in google that has only rating and this will drop lot of them as duplictaes.

            df_consolidated = pd.concat(
                [df_consolidated,df_google], axis=0, ignore_index=True)
            
            df_consolidated["Review_Posting_Date"] = pd.to_datetime(
                df_consolidated["Review_Posting_Date"])

            df_consolidated.fillna("", inplace=True)
            df_consolidated["Review"] = (
                df_consolidated["Title"]
                + df_consolidated["Main_Review"]
                + df_consolidated["Pros"]
                + df_consolidated["Cons"])

            temp_df = df_consolidated.loc[(df_consolidated["Review"] == "") & (df_consolidated["Rating"] != ""), :]
           
            temp_df.loc[:, "Review"] = temp_df.apply(
                lambda x: ["Good" if x["Rating"] >= 3 else "Bad"], axis=1
            )
            
            temp_df.loc[:, "Review"] = temp_df["Review"].apply(
                lambda x: " ".join(x))

            df_consolidated = pd.concat([df_consolidated, temp_df], axis=0)

            df_consolidated = df_consolidated.loc[df_consolidated["Review"] != "", :]

            #  Unique ID assigned to all the reviews
            df_consolidated["Review_id"] = np.arange(
                1, len(df_consolidated) + 1)

            df_consolidated["Employeer Status"] = (
                df_consolidated["Employeer Status"]
                .str.replace("less than", "<")
                .str.replace("more than", ">")
                .str.replace("years", "yrs")
                .str.replace("year", "yrs")
                .str.replace(" Employee", ""))

            df_consolidated["User_city"] = df_consolidated.apply(
                lambda df: "Bangalore"
                if df["User_State"] == "Karnataka"
                else df["User_city"],
                axis=1,)

            df_consolidated["User_city"] = df_consolidated["User_city"].str.lower()
            df_consolidated["User_city"] = df_consolidated["User_city"].str.capitalize(
            )

            df_consolidated["User_city"] = df_consolidated["User_city"].apply(
                lambda x: x if len(x) > 0 else "Others")

            df_consolidated.loc[:, "User_city"] = df_consolidated.loc[:, "User_city"].str.replace("Bengaluru", "Bangalore")\
                .str.replace("India", "Bangalore")\
                .str.replace("Canada", "Others")\
                .str.replace("Usa", "Others")\
                .str.replace("Bangalore rural", "Bangalore")\
                .str.replace("Bangalorena", "Bangalore")\
                .str.replace("Wichita ks", "Wichita")\
                .str.replace("Tulsa ok", "Tulsa")\
                .str.replace("Houston tx", "Houston")\
                .str.replace("850 main st wilmington", "wilmington")\
                .str.replace("805 main street wilmington", "wilmington")\
                .str.replace("Baytown texas", "Baytown")\
                .str.replace("North atlanta", "Atlanta")\
                .str.replace("Bangalorepolis", "Bangalore")\
                .str.replace("Bangalore city", "Bangalore")\
                .str.replace("Bangalore urban", "Bangalore")\
                .str.replace("Downtown atlanta", "Atlanta")\
                .str.replace("Atlanta ga", "Atlanta")\
                .str.replace("Corporate - atlanta", "Atlanta")\
                .str.replace("Cedar springs/atlanta", "Atlanta")\
                .str.replace("Hq - atlanta", "Atlanta")\
                .str.replace("Atlanta downtown post office", "Atlanta")\
                .str.replace("East tulsa", "Tulsa")\
                .str.replace("Wichit", "Wichita")\
                .str.replace("Pennington ala", "Pennington")\
                .str.replace("Green bay wi", "Green bay")\
                .str.replace("Green bay wisconsin", "Green bay")\
                .str.replace("Bowling green ky", "Bowling green")\
                .str.replace("Pineland / camden", "Camden")\
                .str.replace("Camas wa", "Camas")\
                .str.replace("Camden wyoming", "Camden")\
                .str.replace("Camden south carolina", "Camden")\
                .str.replace("Bengalore kr puram", "Bangalore")\
                .str.replace("Wichitaa", "Wichita")\
                .str.replace("Lugoff sc", "Lugoff")\
                .str.replace("Lugoff south carolina", "Lugoff")\
                .str.replace("Lugoff", "Camden")\
                .str.replace("Navi mumbai", "Mumbai")\
                .str.replace("Bangalore ", "Bangalore")


            df_consolidated["User_city"] = df_consolidated["User_city"].str.lower()

            df_consolidated["Country"] = df_consolidated["User_city"].apply(
                lambda city: cities_country_mapping[city]
                if city in cities_country_mapping
                else None)

            df_consolidated["User_city"] = df_consolidated["User_city"].str.capitalize(
            )

            df_consolidated["Employeer Status"] = df_consolidated["Employeer Status"].apply(
                lambda x: x if len(x) > 0 else "Others")

            df_consolidated["Country"].fillna("Others", inplace=True)

            df_consolidated["User_Designation"] = df_consolidated[
                "User_Designation"
            ].map(self._designation_assignment)

            df_consolidated["User_Designation"].fillna("Others", inplace=True)

            df_consolidated["Last_Pull"] = datetime.today().strftime(
                "%d-%m-%Y")
            
            df_consolidated["Review_len"] = df_consolidated["Review"].apply(lambda x : len(x.split()))
           
            df_consolidated.loc[:, "Company"] = df_consolidated.loc[:, "Company"].str.replace("Koch Knight", "KES").str.replace("Genesis Robotics", "KES").str.replace(
                "John Zink Hamworthy", "KES").str.replace("DarkVision", "KES").str.replace("Optimized Process Design", "KES").str.replace("Koch Glitsch", "KES").str.replace("OnPoint", "KES").str.replace("Sentient Energy", "KES").str.replace("Koch Chemical Technology", "KES")

            df_consolidated.to_excel(self.FILE_OUTPUT.get(
                "output"), index=False, engine="xlsxwriter")

            print(
                "\n\n<<<<<<<<<<<<<      CONSOLIDATION OF FILE IS SUCCESSFULL     >>>>>>>>>>>>>>>>>>>>>\n\n")
            # print(df_consolidated)
            return df_consolidated

        except Exception as e:
            print(e)
            return "\n\n<<<<<<<<<<<<<      CONSOLIDATION OF FILE IS UNSUCCESSFULL     >>>>>>>>>>>>>>>>>>>>>\n\n"


if __name__ == "__main__":

    FILE_INPUT_PATHS = {
        "indeed_koch": "../Input/Indeed/Koch.xlsx",
        "indeed_molex": "../Input/Indeed/Molex.xlsx",
        "indeed_GP": "../Input/Indeed/GP.xlsx",
        "indeed_guardian": "../Input/Indeed/Guardian.xlsx",
        "indeed_fhr": "../Input/Indeed/FHR.xlsx",
        "indeed_invista": "../Input/Indeed/Invista.xlsx",
        "glassdoor": "../Input/Glassdoor/glassdoor.csv",
        "google": "../Input/Google/google.csv",
        "ambitionbox": "../Input/AmbitionBox/ambitionbox.xlsx"

    }
    FILE_OUTPUT = {"output": "../Output/Consolidated_Koch_review.xlsx"}

    obj = DataLoader(FILE_INPUT_PATHS, FILE_OUTPUT)
    output = obj.consolidating_reviews()
