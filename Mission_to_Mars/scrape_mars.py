from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    # NASA Mars News #

    browser = init_browser()

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    news = soup.find_all('div', class_='list_text')

    news_title = []
    news_p = []

    for new in news:
        nt = new.find('div', class_='content_title').text
        np = new.find('div', class_='article_teaser_body').text

        news_title.append(nt)
        news_p.append(np)

    news_title = news_title[0]
    news_p = news_p[0]

    browser.quit()

    # JPL Mars Space Images - Featured Image

    browser = init_browser()

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    time.sleep(1)

    img_html = browser.html
    soup = bs(img_html, 'html.parser')

    img = soup.find('a', class_='showimg')

    featured_image_url = f'{img_url}{img["href"]}'

    browser.quit()

    # Facts table #

    facts_url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(facts_url)

    df_facts = tables[0]
    df_facts.columns = df_facts.iloc[0,:]
    df_facts.drop(index=0, inplace=True)
    df_facts.reset_index(drop=True, inplace=True)
    df_facts_html = df_facts.to_html(index=False)

    # Hemispheres images #

    browser = init_browser()

    hem_url = 'https://marshemispheres.com/'
    browser.visit(hem_url)
    time.sleep(1)

    hemisphere_image_url = []
    names = []
    hems_url = []

    hem_html = browser.html
    soup = bs(hem_html, 'html.parser')

    hems = soup.find_all('div', class_='description')

    for hem in hems:
        hemisphere = hem.find('a').find('h3').text
        names.append(hemisphere)

    for i in names:
        browser.links.find_by_partial_text(names[0]).click()
        hem_html = browser.html
        soup = bs(hem_html, 'html.parser')
        hems = soup.find('div', class_='wide-image-wrapper')
        hems = hems.find('img', class_='wide-image')['src']
        hems_url.append(f'{hem_url}{hems}')
        browser.back()

    for i,j in zip(names,hems_url):
        dictionary = {'title':'','img_url':''}
        dictionary['title'] = i
        dictionary['img_url'] = j
        hemisphere_image_url.append(dictionary)
    
    browser.quit()

    # Create dictionary for all this #
    mars_dict = {
        # Mars title
        'news_title':news_title,
        'news_p':news_p,

        # Featured Image
        'featured_image_url':featured_image_url,

        # Mars facts
        'mars_facts_html':df_facts_html,

        'hemisphere_image_url':hemisphere_image_url
    }

    return mars_dict