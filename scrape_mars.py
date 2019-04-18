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

mars_information = {}

def mars_scrape(): 
    #SCRAPING NEWS TITLE AND SUMMARY PARAGRAPH DEFINITION 
    #Initialize Browser
    browser=inint_browser()

    #Mission to mars dictionary to hold scraped information 
    #mars_information = {}

    #Scrape with URL
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    #BeautifulSoup and parse
    news_html = browser.html
    mars_news_soup = BeautifulSoup(news_html, 'html.parser')
        
    #Retrieve elements
    news_title=mars_news_soup.find('div', class_='content_title').text
    news_p=mars_news_soup.find('div', class_='article_teaser_body').text

    #Results and add to dictionary
    mars_information['news_title'] = news_title
    mars_information['news_paragraph'] = news_p
    
    #SCRAPING FEATURE MARS IMAGE DEFINITION
    mars_image_url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_image_url)

    #BeautifulSoup and parse
    image_html=browser.html
    image_soup=BeautifulSoup(image_html, 'html.parser')

    #Retrieve elements
    image_url=image_soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
        
    #Results and add to dictionary
    main_url='https://www.jpl.nasa.gov'
    feature_image_url=main_url+image_url

    mars_information['feature_image_url'] = feature_image_url
    
    #SCRAPING MARS WEATHER DEFINITION 
    weather_url='https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    #BeautifulSoup and parse
    weather_html = browser.html
    twitter_mars_soup = BeautifulSoup(weather_html, 'html.parser')

    #Retrieve elements
    twitter_mars=twitter_mars_soup.find_all('div', class_='js-tweet-text-container')

    #Results and add to dictionary
    for tweet in twitter_mars: 
        mars_weather=tweet.find('p').text
        if 'Sol' and 'gust' in mars_weather:
            mars_information['weather_tweet'] = mars_weather
    
    #SCRAPING MARS FACTS DEFINITION
    mars_facts_url = 'https://space-facts.com/mars/'

    #html read 
    mars_facts=pd.read_html(mars_facts_url)

    #Retrieve elements
    mars_facts_df=mars_facts[0]

    #Transforamtion 
    mars_facts_df.columns= ['Description','Value']
    mars_facts_df.set_index('Description')

    #Results and add to dictionary
    mars_facts_html=mars_facts_df.to_html()

    mars_information['mars_facts'] = mars_facts_html
    
    #SCRAPING MARS HEMISPHERE
    hem_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hem_url)

    #BeautifulSoup and parse
    hem_html = browser.html
    mars_hem_soup = BeautifulSoup(hem_html, 'html.parser')

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
    
    # Close the browser after scraping
    browser.quit()

    return mars_information