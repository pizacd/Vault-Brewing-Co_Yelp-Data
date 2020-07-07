#!/usr/bin/env python
# coding: utf-8


#Importing libraries needed to complete web scraping
from bs4 import BeautifulSoup as soup
import requests
import re


#url for desired business. Yelp updated the tags so they need to be updated if it isn't finding the text.
url = 'https://www.yelp.com/biz/vault-brewing-yardley'
response = requests.get(url)
s = soup(response.text,'html.parser')



response.status_code #used to confirm whether data can be scraped. 200 indicats that scraping will be accepted.



num_reviews = int(s.find('p',attrs = {'class':"lemon--p__373c0__3Qnnj text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa- text-size--large__373c0__3t60B"}).text.strip(' reviews'))


print(str(num_reviews)+' reviews posted about this restaurant')
url_list = []
#creating list of all the urls to call in order to scrape reviews on different pages
for i in range(0, num_reviews,20):
    url_list.append(url+'?start='+str(i))



#part of webpage that highlights the entire review
reviews = s.find_all('div',attrs = {'class':"lemon--div__373c0__1mboc review__373c0__13kpL sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__2C9bH gutter-2__373c0__1DiLQ grid__373c0__1Pz7f layout-stack-small__373c0__27wVp border-color--default__373c0__3-ifU"})



review = reviews[2]
#To protect privacy, Yelp user names have not been included in the file. However, source code is below.
#username = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa"}).string
#print(username)



location = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO"}).get_text().strip()



print(location)



#getting the rating and doing string manipulation to change the data type to float
rating = float(review.select('[aria-label*=rating]')[0]['aria-label'].strip(' star rating'))


print(rating)


#Extracting the date the review was posted on Yelp
date = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-"}).get_text()
print(date)



#Extracting the text of the review
content = review.find('p',attrs = {'class':"lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"}).text



content


import csv
import time
import random

def scrape_single_page(reviews, csvwriter):
    for review in reviews:
        dic = {}
        #Code copied from previous steps
        #username = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2pB8f fs-block text-color--inherit__373c0__w_15m text-align--left__373c0__2pnx_ text-weight--bold__373c0__3HYJa"}).string
        try:
            location = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2Kxyz text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa- text-weight--bold__373c0__1elNz text-size--small__373c0__3NVWO"}).get_text().strip()  
        except:
            location = ''
        date = review.find('span',attrs = {'class':"lemon--span__373c0__3997G text__373c0__2Kxyz text-color--mid__373c0__jCeOG text-align--left__373c0__2XGa-"}).get_text()
        rating = float(review.select('[aria-label*=rating]')[0]['aria-label'].strip(' star rating'))
        content = review.find('p',attrs = {'class':"lemon--p__373c0__3Qnnj text__373c0__2Kxyz comment__373c0__3EKjH text-color--normal__373c0__3xep9 text-align--left__373c0__2XGa-"}).text
        #Assign Values to the dictionary
        #dic['username']=username Commented out to protect yelp user privacy
        dic['location']=location
        dic['date'] = date
        dic['rating'] = rating
        dic['content']=content
        review_writer.writerow(dic.values())
header = ['Location','Date','Rating','Content']
with open('vaultbrewing.csv','w',encoding = 'utf-8') as csvfile:
    review_writer = csv.writer(csvfile)
    review_writer.writerow(header)
    for index, url in enumerate(url_list):
        response = requests.get(url).text
        s = soup(response, 'html.parser')
        reviews = s.find_all('div',attrs = {'class':"lemon--div__373c0__1mboc review__373c0__13kpL sidebarActionsHoverTarget__373c0__2kfhE arrange__373c0__2C9bH gutter-2__373c0__1DiLQ grid__373c0__1Pz7f layout-stack-small__373c0__27wVp border-color--default__373c0__3-ifU"})        
        scrape_single_page(reviews, review_writer)
        #Random sleep to avoid getting banned from the server
        time.sleep(random.randint(1,5))
        #log the progress
        print('finished page '+str(index+1) + ' of '+ str(len(url_list)))

