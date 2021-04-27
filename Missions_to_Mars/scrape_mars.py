from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# URLs
news_url = 'https://mars.nasa.gov/news/'
facts_url = 'https://space-facts.com/mars/'
jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

def scrape():

    mars_dict = {}

    # get latest news
    response = requests.get(news_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    top_result = soup.find('div', class_="slide")
    title_html = top_result.find('div', class_='content_title')
    mars_dict['news_title'] = title_html.a.text
    desc_html = top_result.find('div', class_="rollover_description_inner")
    mars_dict['news_desc'] = desc_html.text

    # get table of facts about mars
    tables = pd.read_html(facts_url)
    mars_facts = tables[0]
    mars_dict["facts_table_html"] = mars_facts.to_html(index=False, header=False)


    # get latest mars image
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    browser.visit(jpl_url)
    mars_dict["featured_img_url"] = browser.links.find_by_partial_text('FULL IMAGE')['href']

    # get images of each hemisphere
    hemispheres = []
    browser.visit(hemispheres_url)
    for i in range(4):
        images = browser.links.find_by_partial_text('Hemisphere')
        images[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_url_suffix = soup.find('img', class_='wide-image')['src']
        img_url = 'https://astrogeology.usgs.gov/' + img_url_suffix
        title = (soup.find('h2', class_='title').text).split(" Enhanced", 1)[0]
        img_dict = {"title": title, "img_url":img_url}
        hemispheres.append(img_dict)
        browser.back()
    browser.quit()


    mars_dict["hemisphere_imgs"] = hemispheres

    return mars_dict


print(scrape())

