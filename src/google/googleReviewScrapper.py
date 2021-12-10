
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import datetime as dt

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('log-level=3')
browser = webdriver.Chrome(options=chrome_options,
                           executable_path=r'.\google\chromedriver.exe')
webdriver = browser

webdriver.get(
    'https://www.google.com/search?q=koch+business+solutions#lrd=0x3bae151545665083:0xc996106e00eceebd,1,,,')

#Reviewer,ReviewDate,ReviewRating,ReviewDescription,TotalReviewsByUser,webdriver_obj,thisreview =([],) * 7
Reviewer = []
ReviewDate = []
ReviewRating = []
ReviewDescription = []
TotalReviewsByUser = []
webdriver_obj = []
thisreview = []
ReviewState = []
ReviewCountry = []
time.sleep(3)
last_len = 0


def get_reviews(thisreview):
    global last_len
    for webdriver_obj in thisreview.find_elements_by_class_name("WMbnJf"):
        Name = webdriver_obj.find_element_by_class_name("jxjCjc")
        Reviewer.append(Name.text)
        try:
            ReviewByuser = webdriver_obj.find_element_by_class_name("A503be")
            TotalReviewsByUser.append(ReviewByuser.text)
        except NoSuchElementException:
            TotalReviewsByUser.append("")
        star = webdriver_obj.find_element_by_class_name("Fam1ne")
        ReviewStar = star.get_attribute("aria-label")
        ReviewStar = ReviewStar.split('.')[0].split(' ')[1]
        ReviewRating.append(ReviewStar)
        ReviewState.append("Karnataka")
        ReviewCountry.append("India")
        Date = webdriver_obj.find_element_by_class_name("dehysf")
        if 'month' in Date.text.lower():
            if Date.text.split(' ')[0].isnumeric():
                monthBuffer = int(Date.text.split(' ')[0])
                finalDate = (pd.Period(dt.datetime.now(), 'M') -
                             monthBuffer).strftime('%B %Y')
            else:
                finalDate = (pd.Period(dt.datetime.now(), 'M') -
                             1).strftime('%B %Y')
        elif 'year' in Date.text.lower():
            if Date.text.split(' ')[0].isnumeric():
                yearBuffer = int(Date.text.split(' ')[0])*12
                finalDate = (pd.Period(dt.datetime.now(), 'M') -
                             yearBuffer).strftime('%B %Y')
            else:
                finalDate = (pd.Period(dt.datetime.now(), 'M') -
                             12).strftime('%B %Y')
        ReviewDate.append(finalDate)
        Body = webdriver_obj.find_element_by_class_name('Jtu6Td')
        try:
            webdriver_obj.find_element_by_class_name('review-snippet').click()
            s_32B = webdriver_obj.find_element_by_class_name(
                'review-full-text')
            ReviewDescription.append(s_32B.text)
        except NoSuchElementException:
            ReviewDescription.append(Body.text)
        print("Fetching review Data for -"+Name.text.split('\n')[0])
        element = webdriver_obj.find_element_by_class_name('PuaHbe')
        webdriver.execute_script("arguments[0].scrollIntoView();", element)
    print("Fetching Next page...")
    time.sleep(3)
    reviews = webdriver.find_elements_by_class_name(
        "gws-localreviews__general-reviews-block")
    r_len = len(reviews)
    if r_len > last_len:
        last_len = r_len
        get_reviews(reviews[r_len-1])


reviewsTypes = webdriver.find_elements_by_class_name(
    'EDblX')

list = ["MostRelevant", "Newest", "Highest", "Lowest"]
count = 0
for type in reviewsTypes:
    if count == 1:
        break
    type.find_element_by_class_name("AxAp9e").click()
    reviews = webdriver.find_elements_by_class_name(
        "gws-localreviews__general-reviews-block")
    last_len = len(reviews)
    get_reviews(reviews[last_len-1])
    fileName = "../Input/google.csv"
    data = pd.DataFrame({'Reviewer': Reviewer, 'TotalReviewsByUser': TotalReviewsByUser,
                         'ReviewRating': ReviewRating, 'ReviewDate': ReviewDate, "State": ReviewState, "Country": ReviewCountry,
                         'ReviewDescription': ReviewDescription})
    data.to_csv(fileName, index=False, encoding='utf-8')
    count = count+1

webdriver.close()
