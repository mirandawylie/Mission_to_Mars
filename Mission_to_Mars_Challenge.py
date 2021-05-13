    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup
    from webdriver_manager.chrome import ChromeDriverManager
    import pandas as pd

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #Visit the mars nasa news site
    url = 'https://redplanetscience.com'\n
    browser.visit(url)\n

    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    #Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()

    #Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
   
   ### Featured Images
    #Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
   
    #Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
  
    #Find the relative image urlimg_soup.find('img', class_='fancybox-image').get('src')\n
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
 
    ### Mars Facts
    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    df
   
    df.to_html()

    ### Hempisheres
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/
    browser.visit(url)
  
    #Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
  
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
  
    3. Write code to retrieve the image urls and titles for each hemisphere.
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
  
    # 4. Print the list that holds the dictionary of each image url and title.
    "hemisphere_image_urls"
 
    #close automated browser
    browser.quit()
