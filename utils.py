from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import csv

from datetime import datetime
import pytz

def load_csv_file(file_path):
    users = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            # Assuming the CSV columns are in the order: username, password, phone
            username, password, phone = row
            users.append((username, password, phone))
    return users


def find_tweet(driver, tweet_url):
    """
    Finds a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - tweet_url: URL of the tweet to like.

    Returns:
    - Required tweet from the page if no error encountered else None.
    """
    try:
        driver.get(tweet_url)
        time.sleep(5)  # Let the page load
        # Find all the tweets (article elements) on the page
        tweets = driver.find_elements(By.CSS_SELECTOR, "article[data-testid='tweet']")
        for tweet in tweets:
            a_tags = tweet.find_elements(By.TAG_NAME, "a")
            for a_tag in a_tags:
                tweet_link = a_tag.get_attribute("href")
                if tweet_link == tweet_url:
                    return tweet
    except Exception as e:
        print(f"Error while finding tweet: {str(e)}")
        return None


def find_tweets(driver, keyword, n):
    """
    Finds a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - keyword: Keyword to search related tweets.
    - n: min no of tweets to return

    Returns:
    - List of links of tweets if no error encountered else None.
    """
    keyword = keyword.replace(' ', '%20').replace('#', '%23')
    url  = f'https://x.com/search?q={keyword}&src=typed_query&f=live'
    try:
        driver.get(url)
        time.sleep(5)  # Let the page load
        # Find all the tweets (article elements) on the page
        links = set()
        while len(links) <= n:
            tweets = driver.find_elements(By.CSS_SELECTOR, "a[href*='/status/']")
            for tweet in tweets:
                link = tweet.get_attribute("href")
                post_link = '/'.join(link.split('/')[:6])
                links.add(post_link)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for the page to load new tweets

        return list(links)[:n]
        
    except Exception as e:
        print(f"Error while finding tweet: {str(e)}")
        return None
    



def create_report(report_content):
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    # Get current time in IST
    ist_time = datetime.now(ist)
    # Format it as a string
    ist_time_str = ist_time.strftime('%Y_%m_%d_%H_%M_%S')

    report_name = ist_time_str
    with open(f'reports/{report_name}.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(report_content)


def get_timestamp():
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    # Get current time in IST
    ist_time = datetime.now(ist)
    # Format it as a string
    ist_time_str = ist_time.strftime('%Y/%m/%d %H:%M:%S')
    return ist_time_str