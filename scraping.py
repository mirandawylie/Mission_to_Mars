# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

#initalize browser, create data dictonary, end WebDriver, return scraped data
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres(browser)
    }

   # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert browser to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Use try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None

#return function
    return news_title, news_p

# ## JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL Space Images
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #Use try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    #return function
    return img_url

# ## Mars Facts

def mars_facts():

    #Use try/except for error handling
    try:
        #use 'read_html" to scrape facts into tables dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

#Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

# Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-hover table-condensed")

def hemispheres(browser):
# Initiate headless driver for deployment
    url = 'https://marshemispheres.com/'
    browser.visit(url + 'index.html')
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item img')[i].click()
  
        #Find image anchor tag
        sample_element = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_element['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
  
    return hemisphere_image_urls

if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())