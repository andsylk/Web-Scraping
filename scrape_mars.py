# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

# NASA Mars News
def mars_news_title():
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, "html.parser")
    first_news = soup.find('div', class_= "image_and_description_container")
    first_list = first_news.find('div', class_ ="list_text")
    news_title = first_list.find('div', class_ = 'content_title').text
    return news_title

def mars_news_p():
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, "html.parser")
    first_news = soup.find('div', class_= "image_and_description_container")
    first_list = first_news.find('div', class_ ="list_text")
    news_p = first_list.find('div',class_= 'article_teaser_body').text
    return news_p

# JPL Mars Space Images - Featured Image
def mars_featured_image():
    url2 = 'https://www.jpl.nasa.gov'
    images = '/spaceimages/?search=&category=Mars'
    browser.visit(url2+images)
    time.sleep(3)
    button = browser.find_by_id('full_image')
    button.click()
    html = browser.html
    time.sleep(3)
    soup2 = bs(html, 'html.parser')
    featured_image = soup2.find('a', class_= "button fancybox")['data-fancybox-href']
    featured_image_url = url2 + featured_image
    return featured_image_url

# Mars Weather
def mars_weather():
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(3)
    html = browser.html
    soup3 = bs(html, 'html.parser')
    weather = soup3.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    latest_weather = weather.text
    return latest_weather

# Mars Facts
def mars_facts():
    url4 = 'https://space-facts.com/mars/'
    browser.visit(url4)
    time.sleep(3)
    html = browser.html
    soup4 = bs(html, 'html.parser')
    table = soup4.find('table')
    mars_facts_table = pd.read_html(str(table))[0]
    mars_facts_table = mars_facts_table.rename(columns={0: 'Description', 1: 'Value'}).set_index('Description')
    mars_facts_html = mars_facts_table.to_html(index = True, header =True)
    return mars_facts_html

# Mars Hemisphere
def mars_hemisphere():
    url5 = 'https://astrogeology.usgs.gov'
    enhanced = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5+enhanced)
    time.sleep(3)
    html = browser.html
    soup5 = bs(html, 'html.parser')
    hemispheres = soup5.find_all('div', class_ = 'item')
    hemisphere_image_urls = [] 
    for hemisphere in hemispheres:
        hemisphere_title = hemisphere.find('h3').text
        title = hemisphere_title.replace('Enhanced','')
        hemisphere_thumb = hemisphere.find('a')['href']
        browser.visit(url5+hemisphere_thumb)
        time.sleep(2)
        new_html = browser.html
        soup = bs(new_html, 'html.parser')
        download = soup.find('div', class_='downloads')
        img_url = download.find('a')['href']
        hemisphere_image_urls.append({'title': title,
                                    'img_url': img_url})
    return hemisphere_image_urls

# Scrape Function
def scrape():
    mars_data={}
    mars_data["news_title"] = mars_news_title()
    mars_data["news_description"] = mars_news_p()
    mars_data["featured_image_url"] = mars_featured_image()
    mars_data["weather"] = mars_weather()
    mars_data["mars_facts"] = mars_facts()
    mars_data["mars_hemisphere_urls"] = mars_hemisphere()
    return mars_data


