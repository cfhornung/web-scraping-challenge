# Dependencies & Setup
# splinter : https://pypi.org/project/splinter/
# beautiful soup : https://www.crummy.com/software/BeautifulSoup/
# Chromedriver : https://sites.google.com/a/chromium.org/chromedriver/downloads

# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
from time import sleep
import requests

# Function to open browser
def init_browser():
    
    # Set Executable Path & Initialize Chrome Browser (Mac)
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless = False)

# Scrape function
def scrape():

    # Call function to open browser
    browser = init_browser()

    # NASA Mars News Site
    nasa_mars_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_mars_url)
    sleep(5)
    bs = BeautifulSoup(browser.html, 'html.parser')

    # Retrieve latest title and paragraph
    news_title = bs.find("div", class_ = "list_text").find("div", class_ = "content_title").text
    news_paragraph = bs.find_all("div", class_= "article_teaser_body")[0].get_text()

    # JPL NASA Site
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Retrieve featured image
    browser.click_link_by_partial_text("FULL IMAGE")
    sleep(5)
    browser.click_link_by_partial_text("more info")
    browser.click_link_by_partial_text(".jpg")
    featured_image_url = browser.url

    # Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    twitter_page = requests.get(twitter_url)
    bs = BeautifulSoup(twitter_page.content, 'html.parser')

    # Retrieve first tweet
    first_tweet = first_tweet = bs.find("div", class_ = 'css-1dbjc4n').text
    #mars_weather_tweet = first_tweet.find("p").get_text().replace("\n", "").split("pic.twitter.com")[0]
    mars_weather_tweet = first_tweet

    # Mars Facts
    mars_facts_url = "https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    # Use Pandas to create a Dataframe to hold facts
    mars_facts_df = pd.read_html(mars_facts_url)[2]
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_df["Description"] = mars_facts_df["Description"].str.replace(":", "")
    mars_facts_df.set_index("Description", inplace = True)
    mars_facts_html = mars_facts_df.to_html()

    # Mars Hemispheres
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    sleep(25)

    # Loop through each hemisphere and scrape the data
    hemispheres = ["Cerberus", "Schiaparelli", "Syrtis", "Valles"]
    hemisphere_image_urls = []
    for hemi in hemispheres:

        hemisphere_dict = {}
        browser.click_link_by_partial_text(hemi)
        usgs_html = browser.html
        bs = BeautifulSoup(usgs_html, 'html.parser')
        hemisphere_dict["title"] = bs.find("h2").get_text().replace("Enhanced", "").strip()
        hemisphere_dict["img_url"] = bs.find_all("div", class_= "downloads")[0].find_all("a")[0]["href"]
        hemisphere_image_urls.append(hemisphere_dict)
        browser.back()

    # Close browser after scraping is complete
    browser.quit()

    # Store data in a dictionary and return
    mars_data = {
        "nasa_mars_title": news_title,
        "nasa_mars_paragraph": news_paragraph,
        "jpl_image": featured_image_url,
        "mars_latest_tweet": mars_weather_tweet,
        "mars_facts": mars_facts_html,
        "mars_hemisphere": hemisphere_image_urls
    }
    return mars_data

# Run
if __name__ == "__main__":
    print(scrape())