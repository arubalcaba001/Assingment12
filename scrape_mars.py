# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import requests
import numpy as np 


#INITIALIZE BROWSER DEFINITION
def inint_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

#Mission to mars dictionary to hold scraped information 
mars_information = {}

#SCRAPING NEWS TITLE AND SUMMARY PARAGRAPH DEFINITION
def scrape_mars_news(): 
    try: 
        #Initialize Browser
        browser=inint_browser()

        #Scrape with URL
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        #BeautifulSoup and parse
        html = browser.html
        mars_news_soup = BeautifulSoup(html, 'html.parser')
        
        #Retrieve elements
        news_title=mars_news_soup.find('div', class_='content_title').text
        news_p=mars_news_soup.find('div', class_='article_teaser_body').text

        #Results and add to dictionary
        mars_information['news_title'] = news_title
        mars_information['news_paragraph'] = news_p

        return mars_information
    finally:
        browser.quit()

#SCRAPING FEATURE MARS IMAGE DEFINITION
def scrape_feature_image(): 
    try: 
        #Initialize Browser
        browser=inint_browser()

        #Scrape with URL
        url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)

        #Click to the page
        browser.click_link_by_partial_text('FULL IMAGE')

        #BeautifulSoup and parse
        html=browser.html
        image_soup=BeautifulSoup(html, 'html.parser')

        #Retrieve elements
        image_url=image_soup.find('img', class_='fancybox-image')['src']
        
        #Results and add to dictionary
        main_url='https://www.jpl.nasa.gov'
        feature_image_url=main_url+image_url
        feature_image_url 

        mars_information['feature_image_url'] = feature_image_url 
        
        return mars_information
    finally:
        browser.quit()

#SCRAPING MARS WEATHER DEFINITION
def scrape_mars_weather(): 
    try: 
        #Initialize Browser
        browser=inint_browser()

        #Scrape URL
        weather_url='https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)

        #BeautifulSoup and parse
        html = browser.html
        twitter_mars_soup = BeautifulSoup(html, 'html.parser')

        #Retrieve elements
        twitter_mars=twitter_mars_soup.find_all('div', class_='js-tweet-text-container')

        #Results and add to dictionary
        for tweet in twitter_mars: 
            mars_weather=tweet.find('p').text
            if 'Sol' and 'gust' in mars_weather:
                print(mars_weather)
                break
            else: 
                pass

        mars_information['weather_tweet'] = mars_weather
        
        return mars_information
    finally:
        browser.quit()

#SCRAPING MARS FACTS DEFINITION
def scrape_mars_facts(): 
 
        #Scrape URL
        mars_facts_url = 'https://space-facts.com/mars/'

        #html read 
        mars_facts=pd.read_html(mars_facts_url)

        #Retrieve elements
        mars_facts_df=mars_facts[0]

        #Transforamtion 
        mars_facts_df.columns= ['Description','Value']
        mars_facts_df.set_index('Description')

        #Results and add to dictionary
        mars_data=mars_facts_df.to_html()

        mars_info['mars_facts'] = mars_data

        return mars_information

#SCRAPING MARS HEMISPHERE
def scrape_mars_hemisphere(): 
    try: 
        #Initialize Browser
        browser=inint_browser()

        #Scrape URL
        hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hem_url)

        #BeautifulSoup and parse
        html = browser.html
        mars_hem_soup = BeautifulSoup(html, 'html.parser')

        #Retrieve elements
        hem_mars = mars_hem_soup.find_all('div', class_='item')
        hem_main_url = 'https://astrogeology.usgs.gov'

        #Results and add to dictionary
        hem_img_urls=[]

        for p in hem_mars: 
        
            title= p.find('h3').text
            
            partial_img_url = p.find('a', class_='itemLink product-item')['href']
            browser.visit(hem_main_url + partial_img_url)
            
            partial_img_html = browser.html 
            hem_soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            img_url = hem_main_url + hem_soup.find('img', class_='wide-image')['src']
            hem_img_urls.append({"title" : title, "img_url" : img_url})
            
        mars_information['hemisphere_image_urls'] = hem_img_urls
        
        return mars_information
    finally:
        browser.quit()
