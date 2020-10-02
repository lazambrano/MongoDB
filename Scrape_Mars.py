# Import Dependecies 
from bs4 import BeautifulSoup 
from splinter import Browser
import pandas as pd 
import requests 

# Initialize browser
def init_browser(): 

    exec_path = {'executable_path': '/app/.chromedriver/bin/chromedriver'}
    return Browser('chrome', headless=True, **exec_path)

# Create Mission to Mars global dictionary 
mars_info = {}

# NASA MARS NEWS
def scrape_mars_news():
    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit NASA
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)

        # HTML Object
        html = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')


        # Retrieve the latest element 
        news_title = soup.find('div', class_='bottom_gradient').find('a').text
        news_p = soup.find('div', class_='rollover_description_inner').text

        # Dictionary entry 
        mars_info['news_title'] = news_title
        mars_info['news_paragraph'] = news_p

        return mars_info

    finally:

        browser.quit()

# FEATURED IMAGE
def scrape_mars_image():
    try:
        url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url)
        html = browser.html
        url_soup = BeautifulSoup(html, 'html.parser')
        current_featured_mars_image = browser.find_by_id('full_image')
        current_featured_mars_image.click()
        browser.is_element_present_by_text('more info')
        more_info_2 = browser.links.find_by_partial_text("more info")
        more_info_2.click()
        html = browser.html
        url_soup = BeautifulSoup(html, 'html.parser')
        img_url = url_soup.find('figure', class_="lede")
        image = img_url.find('a')["href"]
        
        # Concat URL
        img_url = f"https://www.jpl.nasa.gov{image}"
        img_url
        # Update Dictionary
        mars_info['featured_image_url'] = img_url
        return mars_info

    
    finally:

        browser.quit()


# Mars Facts
def mars_facts_scrape():    
    space_facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(space_facts_url)
    mars_df = tables[1]
    mars_df.set_index('Mars - Earth Comparison', inplace=True)
    mars_df.head()
    del mars_df['Earth']
    html_table = mars_df.to_html()
    mars_info['mars_facts'] = data
    return mars_info


# MARS HEMISPHERES


def scrape_mars_hemispheres():

    try: 

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website 
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)

        # HTML Object
        html_hemispheres = browser.html

        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html_hemispheres, 'html.parser')

        # Retreive all items 
        items = soup.find_all('div', class_='item')

        # Create empty list for hemisphere urls 
        hiu = []

        # Store the main_ul 
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        # Loop through the items 
        for i in items: 
            # Store title
            title = i.find('h3').text
            
            # Store link 
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit the link
            browser.visit(hemispheres_main_url + partial_img_url)
            
            # HTML Object of individual hemisphere 
            partial_img_html = browser.html
            
            # Parse HTML with Beautiful Soup 
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            
            # Retrieve full image 
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append 
            hiu.append({"title" : title, "img_url" : img_url})

        mars_info['hiu'] = hiu

        
        # Return mars_data dictionary 

        return mars_info
    finally:

        browser.quit()