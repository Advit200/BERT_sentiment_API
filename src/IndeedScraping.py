from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import argparse
import requests


class IndeedPreprocessing:
    def __init__(self):
        pass

    def __repr__(self) -> str:
        return "Preprocessing class for indeed scraping data."

    def _remove_brackets(self, df, col):
        df[col] = df[col].str.replace(r"[", "").str.replace(r"]", "")
        df[col] = df[col].str.replace(r"\\r", "")

        return df[col]

    def _preProcessDF(self, df):
        for col in df.columns:
            df[col] = self._remove_brackets(df, col)

        df["Rating"] = (
            df["Rating"].str.replace(r"'", "").str.replace(r"'", "").astype(int)
        )
        df["Koch_Response_Date"] = pd.to_datetime(df["Koch_Response_Date"])
        df["User_Designation"] = df["author"].str.split("'", expand=True)[1]
        df["Employeer Status"] = (
            df["author"]
            .str.replace(r"(", "")
            .str.replace(r")", "")
            .str.split("'", expand=True)[5]
        )
        df["User_Location"] = df["author"].str.split("'", expand=True)[9]
        df["Review_Posting_Date"] = df["author"].str.split("'", expand=True)[13]
        df["Review_Posting_Date"] = pd.to_datetime(df["Review_Posting_Date"])

        df["helpful_yes"] = (
            df["likes"]
            .str.split(",", expand=True)[0]
            .str.replace(r"'", "")
            .str.replace(r"'", "")
        )
       
        df["helpful_no"] = df["likes"].apply(lambda x : x.split(",")[1].replace(r"'", "").replace(r"'", "") if len(x)>4 else "")

        df["Koch_Response_Delayed"] = (
            df["Koch_Response_Date"] - df["Review_Posting_Date"]
        )
        df["User_city"] = df["User_Location"].str.split(",", expand=True)[0]
        
        df["User_State"] = df["User_Location"].str.split(",", expand=True)[1]
        

        df.drop("author", axis=1, inplace=True)
        df.drop("likes", axis=1, inplace=True)
        df.drop("User_Location", axis=1, inplace=True)

        return df


class IndeedScraper:

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
            (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36",
        "Accept-Language": "en-US, en;q=0.5",
    }

    page = 1

    def __init__(self,company, page_count):
        self.company = company
        self.page_count = page_count

    def __repr__(self) -> str:
        return "Indeed.com scraping class for Koch Reviews"

    def _fetch(self, url):

        df = pd.DataFrame(
            {
                "Title": [],
                "author": [],
                "Rating": [],
                "Pros": [],
                "Cons": [],
                "Main_Review": [],
                "likes": [],
                "Koch_Response": [],
                "Koch_Response_Date": [],
            }
        )

        try:
            webpage = requests.get(url=url, headers=self.HEADERS)
            if webpage.status_code == 200:
                text = webpage.content
                soup = BeautifulSoup(text, "html.parser")
                dom = etree.HTML(str(soup))

                for review in dom.xpath(
                    "//div[@data-testid='reviewsList']//div[@itemprop='review']"
                ):

                    title = review.xpath(".//h2[@data-testid='title']//text()")
                    
                    if len(review.xpath(".//h2[@class='css-6pbru9 e1tiznh50']//text()")) > 0 :
                        pros = review.xpath(".//h2[@class='css-6pbru9 e1tiznh50']/following :: span[1]//text()")
                    else:
                        pros = None

                    if len(review.xpath(".//h2[@class='css-cvf89l e1tiznh50']//text()")) > 0 :
                        cons = review.xpath(".//h2[@class='css-cvf89l e1tiznh50']/following :: span[1]//text()")
                    else:
                        cons = None



                    rating = review.xpath(".//div[@itemprop='reviewRating']//@content")
                    koch_response = review.xpath(
                        ".//div[@class='css-1idfmdn-Text e1wnkr790']//text()"
                    )
                    koch_response_date = review.xpath(
                        ".//span[@class='css-zx9yt0-Text e1wnkr790']//text()"
                    )
                    author = review.xpath(".//span[@itemprop='author']//text()")
                    main_review = review.xpath(
                        ".//div[@data-tn-component='reviewDescription']//text()"
                    )
                    likes = review.xpath(
                        ".//span[@class='css-1l08sf4 eu4oa1w0']//text()"
                    )
                    

                    df = df.append(
                        {
                            "Title": title,
                            "author": author,
                            "Rating": rating,
                            "Pros": pros,
                            "Cons": cons,
                            "Main_Review": main_review,
                            "likes": likes,
                            "Koch_Response": koch_response,
                            "Koch_Response_Date": koch_response_date,
                        },
                        ignore_index=True,
                    )

                df["len"] = df["Title"].apply(lambda x: len(x))

                if all(df["len"]) == 0:
                    print(f"Re running for {self.page}...")
                    self._fetch(url)

                else:
                    print(f"Scrapping Completed for page {self.page}...")
                    df.drop("len", axis=1, inplace=True)
                    return df

            else:
                return "Error"

        except Exception as e:
            print(e)
            return e

    def main(self):

        df_final = pd.DataFrame()
        current_page = 0

        urls = [
            f"https://in.indeed.com/cmp/{self.company}/reviews?fcountry=ALL"
        ]
        urls.extend(
            [
                f"https://in.indeed.com/cmp/{self.company}/reviews?fcountry=ALL&start={i}"
                for i in range(20, 20 * self.page_count, 20)
            ]
        )

        while current_page < len(urls):
            df_local = self._fetch(urls[current_page])
            if isinstance(df_local, pd.DataFrame):
                current_page += 1
                self.page += 1
                df_final = pd.concat([df_final, df_local], axis=0, ignore_index=True)
            else:
                if df_local == "Error":
                    break
                else:
                    pass

        return df_final


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--page",
        default=1,
        type=int,
        help="Provide the no.of pages you want to scrape.",
    )
    parser.add_argument(
        "--location",
        default="../Input/FHR.xlsx",
        type=str,
        help="Provide the location where you want to save the scraped xlsx file.",
    )
    args = parser.parse_args()
    page_count = args.page
    file_location = args.location

    obj = IndeedScraper(company="Molex",page_count=page_count)
    final_df = obj.main()
    final_df.to_excel("../Output/FHR_review_raw.xlsx", index=False)
    PreProcesses_obj = IndeedPreprocessing()
    processed_df = PreProcesses_obj._preProcessDF(
        pd.read_excel("../Output/FHR_review_raw.xlsx")
    )
    processed_df.to_excel(file_location, index=False)
    print(f"\n\nSCRAPING COMPLETED. FILE HAS BEEN SAVED AT {file_location}")
