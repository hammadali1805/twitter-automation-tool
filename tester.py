from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from actions import login, logout, like_tweet, retweet_tweet, comment_tweet, follow_user, message_user
from utils import find_tweets

# Initialize WebDriver
def get_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver

def test_actions(driver):
    # Example usage:
    username = ""
    password = ""
    phone = ""

    # Login
    if login(driver, username, password, phone):
        try:
            # Example actions
            tweet_url = "https://x.com/TheEVuniverse/status/1839566467634729458"
            user_profile_url = "https://x.com/TheEVuniverse"
            keyword = "marvel fans"
            message_text = "Hello!"
            comment_text = "Hi!"

            tweets = find_tweets(driver, keyword, 50)
            print(len(tweets))
            # like_tweet(driver, tweet_url)
            # retweet_tweet(driver, tweet_url)
            # comment_tweet(driver, tweet_url, comment_text)
            # report_tweet(driver, tweet_url)
            # follow_user(driver, user_profile_url)
            # message_user(driver, user_profile_url, message_text)
            # report_user(driver, user_profile_url)
        finally:
            # Logout
            logout(driver)
    else:
        print("Login failed.")

# Example usage
driver = get_driver()
test_actions(driver)
