'''
Installation Requirements:

beautifulsoup4
selenium
webdriver_manager
regex
openpyxl
python-csv
pandas
requests

'''


from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import re
import csv
import pandas as pd
import time
import requests
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0' }


def scroll(driver, timeout):
    scroll_pause_time = timeout

    last_height = driver.execute_script("return document.body.scrollHeight") # Getting scroll height


    while True:
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolling down to bottom
        time.sleep(scroll_pause_time)# Waiting to load page
        new_height = driver.execute_script("return document.body.scrollHeight")# Calculate new scroll height and compare with last scroll height
        if new_height == last_height:
            break
        last_height = new_height


url = "https://www.bigbasket.com/ps/?q=toothpaste"
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(30)
driver.get(url)
scroll(driver, 5)


soup = bs(driver.page_source, 'lxml')
items = soup.findAll("div",{"class":"item prod-deck row ng-scope"})


filename = 'toothpastes.csv' # creating a new csv file
file = open(filename, "w")
writer = csv.writer(file)
writer.writerow(['Ranking', 'Link', 'Product Name', 'Manufacturer','Country of Origin', 'Item Weight', 'Price','Number of Customer Ratings', 'Number of Reviews', 'Average Rating (out of 5)'])

for i in range(len(items)):
    try:
        productlink = "https://www.bigbasket.com" + items[i].div.a['href'] # generating the link of the product
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(productlink)
        soup = bs(driver.page_source, 'lxml') # parsing through the product link
        
        try:
            ranking = str(i)
        except:
            ranking = 'Ranking not found'
        
        try:
            link = productlink
        except:
            link = 'Link not found'
        
        try:
            prod_name = soup.find("h1",{"class":"GrE04"}).text
        except:
            prod_name = 'Product name not found'
            
        try:
            prod_manuf = soup.find("a", {"class":"_2zLWN _3bj9B rippleEffect"}).text
        except:
            prod_manuf = 'Manufacturer not found'
            
        try:
            prod_origin_info = soup.find("div", {"class":"_3ezVU", "id":"about_4"}).text
            prod_origin = re.findall(".*?Country of origin:(.*?)Manufacturer", prod_origin_info)[0].strip()
        except:
            prod_origin = 'Origin not found'
        
        try:
            prod_weight = soup.find("div", {"class": "_3Yybm"}).text.strip()
        except:
            prod_weight = 'Item weight not found'
            
        try:
            prod_price = soup.find("td", {"class":"IyLvo"}).text
        except:
            prod_price = 'Price not found'
            
        try:
            ratings_reviews = soup.find("div", {"class":"gmwyk"}).text
            no_of_ratings_reviews = re.findall("\d*[^a-zA-Z\t]+", ratings_reviews)
            
            try:
                number_of_ratings = no_of_ratings_reviews[0].strip()
            except:
                number_of_ratings = 'Number of ratings not found'
                
            try:
                number_of_reviews = no_of_ratings_reviews[1].strip()
            except:
                number_of_reviews = 'Number of reviews not found'
        except:
            ratings_reviews = 'Ratings & Reviews not found'
            
        
        try:
            avg_rating = soup.find("div", {"class":"_2Ze34"}).text
        except:
            avg_rating = 'Average rating not found'
            
        print(ranking+ ' ' + link + ' ' +  prod_name + ' '+ prod_manuf+' '+ prod_origin + ' ' + prod_weight+ ' ' + prod_price + ' ' +  number_of_ratings + ' ' + number_of_reviews + ' ' + avg_rating)

        # writing the generated information to csv file
        writer.writerow([ranking,link, prod_name,prod_manuf,prod_origin,prod_weight,prod_price,number_of_ratings,number_of_reviews,avg_rating])
        
    except Exception as e:
        print(e)
file.close() # closing the csv file


DataFrame = pd.read_csv('toothpastes.csv')
DataFrame['Ranking'] = DataFrame['Ranking']+1
DataFrame.to_excel('toothpastes_final.xlsx',sheet_name='Product Mapping', index=False)


