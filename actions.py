from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import random
import os

from utils import find_tweet

def login(driver, username, password, phone):
    """
    Logs into Twitter with provided credentials.

    Args:
    - driver: Selenium WebDriver instance.
    - username: Twitter username.
    - password: Twitter password.
    - phone: Phone Number added in Twitter.

    Returns:
    - True if login successful, False otherwise.
    """
    # try:
    #     driver.get("https://twitter.com/login")
    #     time.sleep(2)  # Let the page load

    #     # Use new find_element with By class
    #     driver.find_element(By.NAME, "text").send_keys(username)
    #     driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']").click()

    #     # Wait for password input to be available
    #     WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.NAME, "password"))
    #     ).send_keys(password)

    #     driver.find_element(By.CSS_SELECTOR, "div[data-testid='LoginForm_Login_Button']").click()
        
    #     # Wait for login to complete
    #     WebDriverWait(driver, 10).until(EC.url_contains("twitter.com/home"))
        
    #     return True
    # except Exception as e:
    #     print(f"Error during login: {str(e)}")
    #     return False

    try:

        # Open the Twitter (X) login page
        driver.get("https://x.com/i/flow/login")
        
        # Wait for the page to load
        time.sleep(10)
        
        # Locate the username input field and enter username
        username_input = driver.find_element(By.TAG_NAME, 'input')  # The only available input field
        username_input.send_keys(username)
        
        # Press 'Next' to go to the password field
        username_input.send_keys(Keys.ENTER)
        
        # Wait for the password field to load
        time.sleep(5)
        
        try:
            # Locate the password input field and enter password
            password_input = driver.find_element(By.NAME, 'password')
            password_input.send_keys(password)
            
            # Press 'Enter' to log in
            password_input.send_keys(Keys.ENTER)
            
            # Wait for login to complete
            time.sleep(5)
        except:
            # Locate the username input field and enter username
            phone_input = driver.find_element(By.TAG_NAME, 'input')  # The only available input field
            phone_input.send_keys(phone)
            
            # Press 'Next' to go to the password field
            phone_input.send_keys(Keys.ENTER)
            
            # Wait for the password field to load
            time.sleep(5)

            # Locate the password input field and enter password
            password_input = driver.find_element(By.NAME, 'password')
            password_input.send_keys(password)
            
            # Press 'Enter' to log in
            password_input.send_keys(Keys.ENTER)
            
            # Wait for login to complete
            time.sleep(5)

        return True

    except Exception as e:
        print(f"Error during login: {str(e)}")
        return False





def logout(driver):
    """
    Logs out from Twitter.

    Args:
    - driver: Selenium WebDriver instance.
    """
    try:
        # Logout
        driver.get('https://x.com/logout')
        time.sleep(2)
        
        # Click confirm logout button
        confirm_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="confirmationSheetConfirm"]')
        confirm_button.click()

        # Wait for logout to complete
        time.sleep(5)

    except Exception as e:
        print(f"Error during logout: {str(e)}")


def like_tweet(driver, tweet_url):
    """
    Likes a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - tweet_url: URL of the tweet to like.

    Returns:
    - True if like successful, False otherwise.
    """
    try:
        tweet = find_tweet(driver, tweet_url)
        like_button = tweet.find_element(By.CSS_SELECTOR, '[data-testid="like"]')
        like_button.click()
        time.sleep(2)
        return True
    except Exception as e:
        print(f"Error while liking tweet: {str(e)}")
        return False


def retweet_tweet(driver, tweet_url):
    """
    Retweets a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - tweet_url: URL of the tweet to retweet.

    Returns:
    - True if retweet successful, False otherwise.
    """
    try:        
        tweet = find_tweet(driver, tweet_url)

        repost_button = tweet.find_element(By.CSS_SELECTOR, '[data-testid="retweet"]')
        repost_button.click()
        time.sleep(1)

        confirm_repost = driver.find_element(By.CSS_SELECTOR, '[data-testid="retweetConfirm"]')
        confirm_repost.click()
        time.sleep(2)
        return True

    except Exception as e:
        print(f"Error while retweeting tweet: {str(e)}")
        return False

def comment_tweet(driver, tweet_url, comment_text):
    """
    Comments on a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - tweet_url: URL of the tweet to comment on.
    - comment_text: Text of the comment.

    Returns:
    - True if comment successful, False otherwise.
    """
    try:
        tweet = find_tweet(driver, tweet_url)

        # Wait for the comment (reply) button to be clickable
        comment_box = WebDriverWait(tweet, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="reply"]'))
        )
        comment_box.click()

        # Ensure that the page has time to load the input field
        time.sleep(3)

        # Scroll to the input element to make sure it's in view
        comment_input = driver.find_element(By.CSS_SELECTOR, '[aria-label="Post text"]')
        driver.execute_script("arguments[0].scrollIntoView();", comment_input)

        
        # Wait for the input field to be clickable and send the comment
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Post text"]'))
        )
        comment_input.send_keys(comment_text)

        time.sleep(1)

        # Click the reply button to post the comment
        reply_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="tweetButton"]'))
        )
        reply_button.click()

        # Give it some time for the comment to post
        time.sleep(2)
        return True

    except Exception as e:
        print(f"Error while commenting on tweet: {str(e)}")
        return False


def report_tweet(driver, tweet_url):
    """
    Reports a tweet specified by URL.

    Args:
    - driver: Selenium WebDriver instance.
    - tweet_url: URL of the tweet to report.
    """
    try:
        driver.get(tweet_url)
        time.sleep(2)  # Let the page load

        # Click more options button
        driver.find_element(By.CSS_SELECTOR, 'button[data-testid="caret"]').click()
        time.sleep(2)  # Wait for options to expand

        # Click report tweet
        driver.find_element(By.CSS_SELECTOR, 'div[data-testid="report"]').click()
        time.sleep(1)  # Wait for report modal to appear

        options = [
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
                   ]
        selected = random.choice(options)
        driver.find_element(By.XPATH, selected).click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
        time.sleep(1)

        next_options = [
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
        ]
        next_selected = random.choice(next_options)
        driver.find_element(By.XPATH, next_selected).click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
        time.sleep(1)
        
        return True
    except Exception as e:
        print(f"Error while reporting tweet: {str(e)}")
        return False


def follow_user(driver, user_profile_url):
    """
    Follows a user specified by profile URL.

    Args:
    - driver: Selenium WebDriver instance.
    - user_profile_url: URL of the user's profile to follow.

    Returns:
    - True if follow successful, False otherwise.
    """
    try:
        driver.get(user_profile_url)
        time.sleep(2)  # Let the page load

        user_id = user_profile_url.split('/')[-1]
        follow_button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Follow @{user_id}"]')
        follow_button.click()
        time.sleep(2)
        return True
    
    except Exception as e:
        print(f"Error while following user: {str(e)}")
        return False


def message_user(driver, user_profile_url, message_text):
    """
    Sends a direct message to a user specified by profile URL.

    Args:
    - driver: Selenium WebDriver instance.
    - user_profile_url: URL of the user's profile to message.
    - message_text: Text of the message.

    Returns:
    - True if message successful, False otherwise.
    """
    try:
        driver.get(user_profile_url)
        time.sleep(2)  # Let the page load

        # Click message button
        message_button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Message"]')
        message_button.click()
        time.sleep(2)

        # Enter message
        # message_box = driver.find_element(By.CSS_SELECTOR, 'textarea[data-testid="dmComposerTextInput"]')
        message_box = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="dmComposerTextInput"]')
        message_box.send_keys(message_text)
        time.sleep(2)

        # Send message
        send_button = driver.find_element(By.CSS_SELECTOR, f'button[aria-label="Send"]')
        send_button.click()
        time.sleep(2)
        return True
    
    except Exception as e:
        print(f"Error while messaging user: {str(e)}")
        return True


def report_user(driver, user_profile_url):
    """
    Reports a user specified by profile URL.

    Args:
    - driver: Selenium WebDriver instance.
    - user_profile_url: URL of the user's profile to report.
    """
    try:
        driver.get(user_profile_url)
        time.sleep(2)  # Let the page load

        # Click more options button
        driver.find_element(By.CSS_SELECTOR, 'button[data-testid="userActions"]').click()
        time.sleep(1)  # Wait for options to expand

        # Click report tweet
        driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div[1]/div/div/div[2]/div/div[3]/div/div/div/div[6]').click()
        time.sleep(2)  # Wait for report modal to appear

        options = [
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
                   ]
        selected = random.choice(options)
        driver.find_element(By.XPATH, selected).click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
        time.sleep(1)

        next_options = [
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[1]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[2]',
            '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/div/div/label[3]',
        ]
        next_selected = random.choice(next_options)
        driver.find_element(By.XPATH, next_selected).click()
        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, '[data-testid="ChoiceSelectionNextButton"]').click()
        time.sleep(1)
        
        return True
    except Exception as e:
        print(f"Error while reporting tweet: {str(e)}")
        return False






def post_tweet(driver, message, folder_path=None):
    try:
        # Open Twitter login page
        driver.get("https://twitter.com")
        time.sleep(2)

        # Click on the Tweet button to open the tweet modal
        tweet_box = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Post text"]')
        tweet_box.click()
        time.sleep(1)

        # Type the tweet message
        tweet_box.send_keys(message)

        # Check if folder_path is provided, and add a random image if it is
        if folder_path and os.path.exists(folder_path):
            images = [f for f in os.listdir(folder_path) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
            if images:
                random_image = os.path.join(folder_path, random.choice(images))
                
                # Find the file input element for image upload and send the file path
                file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
                file_input.send_keys(random_image)
                
                # Allow some time for the image to be processed by Twitter
                time.sleep(3)

        # Post the tweet
        tweet_button = driver.find_element(By.XPATH, '//button[@data-testid="tweetButtonInline"]')
        tweet_button.click()

        # Allow time for the tweet to post
        time.sleep(5)

        return True

    except Exception as e:
        print(f"Error while posting tweet: {str(e)}")
        return False