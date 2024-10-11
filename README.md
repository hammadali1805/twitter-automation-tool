# Twitter Automation Tool

## Project Overview

The **Twitter Automation Tool** is a GUI-based application built using `tkinter`, designed to automate various Twitter actions such as liking, retweeting, commenting, following accounts, and more. It allows users to perform these actions based on tweet links, keywords, and user accounts. Additionally, it provides features like paraphrasing content using Google's Gemini AI model and posting tweets with optional image attachments.

## Features
- Automate Twitter actions: Like, Retweet, Comment, Follow, Report, etc.
- Supports CSV file upload for batch processing of actions.
- Use Google's Gemini AI for paraphrasing comments or messages in multiple languages.
- Option to set delay time between automated actions.
- Supports posting tweets with messages and image attachments.

## Project Structure

- **main.py**: The main application file that initializes the GUI and handles all functionalities.
- **utils.py**: Contains utility functions such as loading CSV files, finding tweets, and creating reports.
- **actions.py**: Manages the execution of Twitter actions like posting tweets, liking, retweeting, and more.

## Prerequisites

Before running this application, ensure you have the following:
- Python version: **3.12.4**
- Google API key for using the Gemini AI model (replace `GOOGLE_API_KEY` in `main.py`).
- ChromeDriver for WebDriver automation (automatically installed using `webdriver-manager`).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hammadali1805/twitter-automation-tool.git
   cd twitter-automation-tool
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Make sure you have ChromeDriver installed. You can download it [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), or the script will install it for you using `webdriver-manager`.

4. Replace the placeholder Google API key in `main.py` with your own:
   ```python
   GOOGLE_API_KEY = "your_google_api_key"
   ```

## Usage

1. Run the `main.py` file to start the application:
   ```bash
   python main.py
   ```

2. **Main Tabs**:
   - **Tweet Link Actions**: Perform actions based on tweet links provided in a CSV or manually entered.
   - **Keyword Actions**: Perform actions based on keywords found in tweets.
   - **Account Actions**: Automate actions related to specific accounts (follow, message, report).
   - **Post Tweet**: Post tweets with or without images.

3. **Supported Actions**:
   - Like
   - Retweet
   - Comment (with multilingual paraphrasing option)
   - Follow accounts
   - Message accounts (with multilingual paraphrasing option)
   - Report tweets or accounts
   - Post tweets

## Dependencies

The required Python packages are listed in `requirements.txt`. Some notable dependencies include:
- `tkinter`: For GUI development.
- `google-generativeai`: For using Google's Gemini AI model to paraphrase content.
- `Pillow`: For handling images in the GUI.
- `webdriver-manager`: For managing ChromeDriver installation.

## How to Add API Keys

To use Gemini AI, you'll need a valid Google API key. Update the following line in `main.py` with your key:
```python
GOOGLE_API_KEY = "your_google_api_key"
```

## Customization

1. **Icons and Logos**:
   - Replace the Twitter favicon by updating the `self.iconbitmap('twitter.ico')` line in the `main.py`.
   - Replace the Twitter logo by providing your logo path in the line: `logo = Image.open("twitter.png")`.

2. **Actions**:
   You can customize the actions in the `perform_action()` function in the `main.py` file, which handles automating Twitter actions based on the selected parameters.

## Known Issues

- Ensure proper API rate limits when using the Google Generative AI or the Twitter API to avoid timeouts or temporary bans.
- If ChromeDriver is not properly installed, ensure the `webdriver-manager` installs the correct version compatible with your Chrome browser.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Feel free to contribute by creating pull requests or submitting issues to improve this project!
