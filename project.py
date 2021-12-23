from bs4 import BeautifulSoup
import requests
import time
import datetime
import smtplib


def check_price():
    # connect to website
    URL = 'https://www.amazon.com/dp/B00XD06PMG/ref=sspa_dk_detail_4?psc=1&pd_rd_i=B00XD06PMG&pd_rd_w=D3cIG&pf_rd_p=9fd3ea7c-b77c-42ac-b43b-c872d3f37c38&pd_rd_wg=pUcId&pf_rd_r=4505MHP98ZF80XJNTQTC&pd_rd_r=eb3310dd-8f31-45e6-8ffc-f60240615e7e&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyNFYyUFRSMFdMQ09TJmVuY3J5cHRlZElkPUExMDEwOTQzM1BYQjJGQ1E1UENJSSZlbmNyeXB0ZWRBZElkPUEwODE5Mzc1RDM4S0tRSTNVQjBCJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ=='

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")

    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    title = soup2.find(id='productTitle').get_text()

    price = soup2.find(id='priceblock_ourprice').get_text()

    ratings = soup2.find(id='acrCustomerReviewText').get_text()

    # print(title)
    # print(price)
    # print(ratings)

    # Clean up the data a little bit

    price = price.strip()[1:]
    title = title.strip()
    ratings = ratings.strip()

    # Create a Timestamp for your output to track when data was collected

    import datetime

    today = datetime.date.today()

    print(today)

    # Create CSV and write headers and data into the file

    import csv

    header = ['Title', 'Price', 'Date']
    data = [title, price, today]  # converting everything into a list

    # creating csv
    with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        # data initially inserted into the csv
        writer.writerow(header)
        writer.writerow(data)

    # df = pd.read_csv(r'C:\Users\KIIT\Desktop\amazon_project\AmazonWebScraperDataset.csv')
    #
    # print(df)

    # appending data to the csv

    with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        # 'a+' is for appending the data
        writer = csv.writer(f)
        writer.writerow(data)

    if (price < 15):
        send_mail()


# Runs check_price after a set time and inputs data into your CSV

while (True):
    check_price()
    time.sleep(86400)  # seconds in a day

import pandas as pd

df = pd.read_csv(r'C:\Users\KIIT\Desktop\amazon_project\AmazonWebScraperDataset.csv')

print(df)

# sends a mail if the price decreases bellow 15
def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    # server.starttls()
    server.ehlo()
    server.login('shubham@gmail.com', 'xxxxxxx')

    subject = "The Shirt you want is below $15! Now is your chance to buy!"
    body = "Shubham, This is the moment we have been waiting for. Now is your chance " \
           "to pick up the shirt of your dreams. Don't mess it up! " \
           "Link here: https://www.amazon.com/dp/B00XD06PMG/ref=sspa_dk_detail_4?pd_rd_i=B00XD06PMG&pd_rd_w=D3cIG&pf_rd_p=9fd3ea7c-b77c-42ac-b43b-c872d3f37c38&pd_rd_wg=pUcId&pf_rd_r=4505MHP98ZF80XJNTQTC&pd_rd_r=eb3310dd-8f31-45e6-8ffc-f60240615e7e&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyNFYyUFRSMFdMQ09TJmVuY3J5cHRlZElkPUExMDEwOTQzM1BYQjJGQ1E1UENJSSZlbmNyeXB0ZWRBZElkPUEwODE5Mzc1RDM4S0tRSTNVQjBCJndpZGdldE5hbWU9c3BfZGV0YWlsJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1&psc=1"

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail(
        'shubham.kr2202@gmail.com',
        msg

    )
