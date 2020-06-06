# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Visit the Nasa site 
    news_url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(news_url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = bs(response.text, 'html.parser')


    # Extract the title of the news article
    title = soup.find('div', class_="content_title").text.strip()


    # Extract the teaser paragraph about the news article
    paragraph = soup.find('div', class_="image_and_description_container").text.strip()


    # visit the Nasa Images site
    nasa_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_images_url)


    # Extract the url of the featured image
    image_html = browser.html
    soup = bs(image_html, 'html.parser')

    article = soup.find('a', class_='button fancybox')
    href = article['data-fancybox-href']
    featured_image_url = "https://www.jpl.nasa.gov" + href


    # Visit the Mars Weather Twitter page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.get(weather_url)
    html = driver.page_source
    driver.close()


    # Extract the current weather on Mars
    weather_html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather = soup.find('div', class_="css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text.strip()


    # Visit the Space Facts page about Mars
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)


    # Extract the Mars Facts table as a Pandas dataframe
    table = pd.read_html(facts_url)
    profile = table[0]
    profile_df = profile.rename(columns={0: 'Description', 1: 'Value'})
    facts = []
    for index, row in profile_df.iterrows():
        desc = row['Description']
        value = row['Value']
        fact = {
            'description': desc,
            'value': value
        }
        facts.append(fact)


    # Visit the USGS Astrogeology site
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)


    # Extract the name of each of Mars's hemispheres and the url of the image of that hemisphere, then insert into MongoDB
    hemisphere_html = browser.html
    soup = bs(hemisphere_html, 'html.parser')

    results = soup.find_all('div', class_="item")

    hemisphere_image_urls = []

    for result in results: 
        heading = result.find('h3').text.replace('Enhanced', '')
        link = result.find('a')['href']
        url = "https://astrogeology.usgs.gov" + link
        browser.visit(url)
        image_html = browser.html
        soup = bs(image_html, 'html.parser')
        img_url = soup.find('div', class_="downloads").find('a')['href']
        print(heading)
        print(img_url)
        hemisphere = {
            'title': heading,
            'img_url': img_url
        }
        hemisphere_image_urls.append(hemisphere)
    
    mars_data = {
        "news_title": title,
        "news_paragraph": paragraph,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": facts,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    browser.quit()

    return mars_data