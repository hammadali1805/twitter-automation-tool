import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils import load_csv_file, find_tweets
from actions import *

import google.generativeai as genai
from gemini import paraphrase_content

from datetime import datetime
import pytz

GOOGLE_API_KEY = "YOUR GEMINI API KEY HERE"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')


def create_report(report_content):
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    # Get current time in IST
    ist_time = datetime.now(ist)
    # Format it as a string
    ist_time_str = ist_time.strftime('%Y_%m_%d_%H_%M_%S')

    report_name = ist_time_str
    with open(f'reports/{report_name}.txt', 'w') as f:
        f.write(report_content)



# Initialize WebDriver
def get_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def perform_action(action, tweet_link, comment, paraphrase, language, delay, users, task_type):
        
    if len(users)==0:
        messagebox.showerror('Error', 'No CSV selected or empty CSV selected.')
        return
    
    driver = get_driver()
    report_content = ""
    # report_content += f"TARGET TWEET: {tweet_link}\nACTION: {action}\n\n\n"
    success = 0
    failed = 0

    if task_type=='link':

        report_head = f"TARGET TWEET: {tweet_link}\nACTION: {action}\n\n\n"

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if action == 'like':
                    if like_tweet(driver, tweet_link):
                        success += 1
                        report_content += f"Liked By: {username}\nStatus: Success\n\n"
                    else:
                        failed += 1
                        report_content += f"Liked By: {username}\nStatus: Failed\n\n"

                elif action == 'retweet':                    
                    if retweet_tweet(driver, tweet_link):
                        success += 1
                        report_content += f"Retweeted By: {username}\nStatus: Success\n\n"
                    else:
                        failed += 1
                        report_content += f"Retweeted By: {username}\nStatus: Failed\n\n"

                elif action == 'report':                    
                    if report_tweet(driver, tweet_link):
                        success += 1
                        report_content += f"Reported By: {username}\nStatus: Success\n\n"
                    else:
                        failed += 1
                        report_content += f"Reported By: {username}\nStatus: Failed\n\n"

                elif action == 'comment':
                    if paraphrase:

                        new_comment = paraphrase_content(model, comment, language).strip('\n')
                        if new_comment:

                            if comment_tweet(driver, tweet_link, new_comment):
                                success += 1
                                report_content += f"Commented By: {username}\nComment: {new_comment}\nStatus: Success\n\n"
                            else:
                                failed += 1
                                report_content += f"Commented By: {username}\nStatus: Failed\n\n"

                    else:
                        if comment_tweet(driver, tweet_link, comment):
                            success += 1
                            report_content += f"Commented By: {username}\nComment: {comment}\nStatus: Success\n\n"
                        else:
                            failed += 1
                            report_content += f"Commented By: {username}\nStatus: Failed\n\n"

                logout(driver)
                time.sleep(delay)
            else:
                report_content += f"Login failed for {username}\n\n"


    elif task_type=='keyword':
        report_head = f"TARGET KEYWORD: {tweet_link}\nACTION: {action}\n\n\n"

        if login(driver, users[0][0], users[0][1], users[0][2]):
            tweets = find_tweets(driver, tweet_link, len(users))
            logout(driver)

            if tweets:
                for tweet, (username, password, phone) in zip(tweets, users):

                    if login(driver, username, password, phone):

                        if action == 'like':
                            if like_tweet(driver, tweet):
                                success += 1
                                report_content += f"Liked By: {username}\nTweet: {tweet}\nStatus: Success\n\n"
                            else:
                                failed += 1
                                report_content += f"Liked By: {username}\nTweet: {tweet}\nStatus: Failed\n\n"


                        elif action == 'retweet':                    
                            if retweet_tweet(driver, tweet):
                                success += 1
                                report_content += f"Retweeted By: {username}\nTweet: {tweet}\nStatus: Success\n\n"
                            else:
                                failed += 1
                                report_content += f"Retweeted By: {username}\nTweet: {tweet}\nStatus: Failed\n\n"



                        elif action == 'report':                    
                            if report_tweet(driver, tweet):
                                success += 1
                                report_content += f"Reported By: {username}\nTweet: {tweet}\nStatus: Success\n\n"
                            else:
                                failed += 1
                                report_content += f"Reported By: {username}\nTweet: {tweet}\nStatus: Failed\n\n"


                        elif action == 'comment':
                            if paraphrase:

                                new_comment = paraphrase_content(model, comment, language).strip('\n')

                                if new_comment:

                                    if comment_tweet(driver, tweet, new_comment):
                                        success += 1
                                        report_content += f"Commented By: {username}\nTweet: {tweet}\nComment: {new_comment}\nStatus: Success\n\n"
                                    else:
                                        failed += 1
                                        report_content += f"Commented By: {username}\nTweet: {tweet}\nStatus: Failed\n\n"

                            else:

                                if comment_tweet(driver, tweet, comment):
                                    success += 1
                                    report_content += f"Commented By: {username}\nTweet: {tweet}\nComment: {comment}\nStatus: Success\n\n"
                                else:
                                    failed += 1
                                    report_content += f"Commented By: {username}\nTweet: {tweet}\nStatus: Failed\n\n"    

                        logout(driver)
                        time.sleep(delay)
                    else:
                        report_content += f"Login failed for {username}\n\n"
            else:
                report_content += 'Unable to find latest tweets matching the keyword.'
        else:
            report_content += 'Unable to find latest tweets matching the keyword.'
        

    elif task_type=='account':
        report_head = f'TARGET ACCOUNT: {tweet_link}\nACTION: {action}\n\n\n'

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if action == 'follow':
                    if follow_user(driver, tweet):
                        success += 1
                        report_content += f"Followed By: {username}\nStatus: Success\n\n"
                    else:
                        failed += 1
                        report_content += f"Followed By: {username}\nStatus: Failed\n\n"


                elif action == 'report':                    
                    if report_user(driver, tweet_link):
                        success += 1
                        report_content += f"Reported By: {username}\nStatus: Success\n\n"
                    else:
                        failed += 1
                        report_content += f"Reported By: {username}\nStatus: Failed\n\n"


                elif action == 'message':
                    if paraphrase:
                        new_comment = paraphrase_content(model, comment, language).strip('\n')

                        if new_comment:
                            
                            if message_user(driver, tweet_link, new_comment):
                                success += 1
                                report_content += f"Messeged By: {username}\nMessage: {new_comment}\nStatus: Success\n\n"
                            else:
                                failed += 1
                                report_content += f"Messeged By: {username}\nStatus: Failed\n\n"

                    else:
                        if message_user(driver, tweet_link, comment):
                            success += 1
                            report_content += f"Messaged By: {username}\nMessage: {comment}\nStatus: Success\n\n"
                        else:
                            failed += 1
                            report_content += f"Messaged By: {username}\nStatus: Failed\n\n"


                logout(driver)
                time.sleep(delay)
            else:
                report_content += f"Login failed for {username}\n\n"


    report_content = report_head + f'Success: {success}\nFailed: {failed}\nTotal Expected: {len(users)}\n\n\n' + report_content
    create_report(report_content)
    messagebox.showinfo("SUCCESS", "Automation task has been completed.")
    driver.quit()


# Main Application Class
class XAutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Twitter Automation Tool")
        self.geometry("800x500")

        # Notebook (Tab View)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True)

        # Tabs
        self.tweet_tab = ttk.Frame(self.notebook)
        self.keyword_tab = ttk.Frame(self.notebook)
        self.account_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.tweet_tab, text="Tweet Link Actions")
        self.notebook.add(self.keyword_tab, text="Keyword Actions")
        self.notebook.add(self.account_tab, text="Account Actions")

        # --- Tweet Link Tab UI ---
        self.create_tweet_tab()

        # --- Keyword Tab UI ---
        self.create_keyword_tab()

        # --- Account Tab UI ---
        self.create_account_tab()

    def create_tweet_tab(self):
        # Upload CSV button
        ttk.Button(self.tweet_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_tweet = ttk.Label(self.tweet_tab, text="No file selected")
        self.csv_label_tweet.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.tweet_tab, text="Tweet Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.tweet_link = ttk.Entry(self.tweet_tab, width=40)
        self.tweet_link.grid(row=1, column=1, padx=10, pady=10)

        self.action_var = tk.StringVar(value="like")
        actions = ["like", "like", "retweet", "report", "comment"]
        self.action_dropdown = ttk.OptionMenu(self.tweet_tab, self.action_var, *actions, command=self.toggle_comment)
        self.action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.comment_label = ttk.Label(self.tweet_tab, text="Comment:")
        self.comment_entry = ttk.Entry(self.tweet_tab, width=40)
        self.paraphrase_var = tk.IntVar()
        self.paraphrase_checkbox = ttk.Checkbutton(self.tweet_tab, text="Paraphrase", variable=self.paraphrase_var)
        self.language_var = tk.StringVar(value="English")
        self.language_dropdown = ttk.OptionMenu(self.tweet_tab, self.language_var, "English", "English", "Spanish", "Hindi", "French")

        ttk.Label(self.tweet_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.delay_entry = ttk.Entry(self.tweet_tab, width=10)
        self.delay_entry.grid(row=4, column=1, padx=10, pady=10)
        self.delay_entry.insert(0, "1")

        ttk.Button(self.tweet_tab, text="Start", command=self.start_tweet_actions).grid(row=5, column=1, padx=10, pady=10)

    def create_keyword_tab(self):
        # Upload CSV button
        ttk.Button(self.keyword_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_keyword = ttk.Label(self.keyword_tab, text="No file selected")
        self.csv_label_keyword.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.keyword_tab, text="Keyword:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.keyword_entry = ttk.Entry(self.keyword_tab, width=40)
        self.keyword_entry.grid(row=1, column=1, padx=10, pady=10)

        self.keyword_action_var = tk.StringVar(value="like")
        keyword_actions = ["like", "like", "retweet", "report", "comment"]
        self.keyword_action_dropdown = ttk.OptionMenu(self.keyword_tab, self.keyword_action_var, *keyword_actions, command=self.toggle_keyword_comment)
        self.keyword_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        # Comment feature in Keyword tab
        self.keyword_comment_label = ttk.Label(self.keyword_tab, text="Comment:")
        self.keyword_comment_entry = ttk.Entry(self.keyword_tab, width=40)
        self.keyword_paraphrase_var = tk.IntVar()
        self.keyword_paraphrase_checkbox = ttk.Checkbutton(self.keyword_tab, text="Paraphrase", variable=self.keyword_paraphrase_var)
        self.keyword_language_var = tk.StringVar(value="English")
        self.keyword_language_dropdown = ttk.OptionMenu(self.keyword_tab, self.keyword_language_var, "English", "English", "Spanish", "Hindi", "French")

        ttk.Label(self.keyword_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.keyword_delay_entry = ttk.Entry(self.keyword_tab, width=10)
        self.keyword_delay_entry.grid(row=4, column=1, padx=10, pady=10)
        self.keyword_delay_entry.insert(0, "1")

        ttk.Button(self.keyword_tab, text="Start", command=self.start_keyword_actions).grid(row=5, column=1, padx=10, pady=10)

    def create_account_tab(self):
        # Upload CSV button
        ttk.Button(self.account_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_account = ttk.Label(self.account_tab, text="No file selected")
        self.csv_label_account.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        ttk.Label(self.account_tab, text="Account Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.account_link = ttk.Entry(self.account_tab, width=40)
        self.account_link.grid(row=1, column=1, padx=10, pady=10)

        self.account_action_var = tk.StringVar(value="follow")
        account_actions = ["follow", "follow", "report", "message"]
        self.account_action_dropdown = ttk.OptionMenu(self.account_tab, self.account_action_var, *account_actions, command=self.toggle_message)
        self.account_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.message_label = ttk.Label(self.account_tab, text="Message:")
        self.message_entry = ttk.Entry(self.account_tab, width=40)
        self.account_paraphrase_var = tk.IntVar()
        self.account_paraphrase_checkbox = ttk.Checkbutton(self.account_tab, text="Paraphrase", variable=self.account_paraphrase_var)
        self.account_language_var = tk.StringVar(value="English")
        self.account_language_dropdown = ttk.OptionMenu(self.account_tab, self.account_language_var, "English", "English", "Spanish", "Hindi", "French")

        ttk.Label(self.account_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.account_delay_entry = ttk.Entry(self.account_tab, width=10)
        self.account_delay_entry.grid(row=4, column=1, padx=10, pady=10)
        self.account_delay_entry.insert(0, "1")

        ttk.Button(self.account_tab, text="Start", command=self.start_account_actions).grid(row=5, column=1, padx=10, pady=10)

    def toggle_comment(self, *args):
        if self.action_var.get() == "comment":
            self.comment_label.grid(row=3, column=0, padx=10, pady=10)
            self.comment_entry.grid(row=3, column=1, padx=10, pady=10)
            self.paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.comment_label.grid_remove()
            self.comment_entry.grid_remove()
            self.paraphrase_checkbox.grid_remove()
            self.language_dropdown.grid_remove()

    def toggle_keyword_comment(self, *args):
        if self.keyword_action_var.get() == "comment":
            self.keyword_comment_label.grid(row=2, column=0, padx=10, pady=10)
            self.keyword_comment_entry.grid(row=2, column=1, padx=10, pady=10)
            self.keyword_paraphrase_checkbox.grid(row=2, column=2, padx=10, pady=10)
            self.keyword_language_dropdown.grid(row=2, column=3, padx=10, pady=10)
        else:
            self.keyword_comment_label.grid_remove()
            self.keyword_comment_entry.grid_remove()
            self.keyword_paraphrase_checkbox.grid_remove()
            self.keyword_language_dropdown.grid_remove()

    def toggle_message(self, *args):
        if self.account_action_var.get() == "message":
            self.message_label.grid(row=2, column=0, padx=10, pady=10)
            self.message_entry.grid(row=2, column=1, padx=10, pady=10)
            self.account_paraphrase_checkbox.grid(row=2, column=2, padx=10, pady=10)
            self.account_language_dropdown.grid(row=2, column=3, padx=10, pady=10)
        else:
            self.message_label.grid_remove()
            self.message_entry.grid_remove()
            self.account_paraphrase_checkbox.grid_remove()
            self.account_language_dropdown.grid_remove()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_users = load_csv_file(file_path)  # You can update this to actually load the CSV content.
            self.csv_label_tweet.config(text=file_path)  # Update label with the file path
            self.csv_label_keyword.config(text=file_path)  # Update label with the file path
            self.csv_label_account.config(text=file_path)  # Update label with the file path
        else:
            self.csv_label_tweet.config(text="No file selected")

    def start_tweet_actions(self):
        tweet_link = self.tweet_link.get()
        action = self.action_var.get()
        comment = self.comment_entry.get() if action == "comment" else None
        paraphrase = bool(self.paraphrase_var.get())
        language = self.language_var.get()
        try:
            delay = int(self.delay_entry.get())
        except:
            messagebox.showerror('Error', 'Choose an integer for delay.')
            return
        users = self.csv_users
        perform_action(action, tweet_link=tweet_link, comment=comment, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='link')

    def start_keyword_actions(self):
        keyword = self.keyword_entry.get()
        action = self.keyword_action_var.get()
        comment = self.keyword_comment_entry.get() if action == "comment" else None
        paraphrase = bool(self.keyword_paraphrase_var.get())
        language = self.keyword_language_var.get()
        try:
            delay = int(self.delay_entry.get())
        except:
            messagebox.showerror('Error', 'Choose an integer for delay.')
            return
        users = self.csv_users
        perform_action(action, tweet_link=keyword, comment=comment, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='keyword')

    def start_account_actions(self):
        account_link = self.account_link.get()
        action = self.account_action_var.get()
        message = self.message_entry.get() if action == "message" else None
        paraphrase = bool(self.account_paraphrase_var.get())
        language = self.account_language_var.get()
        try:
            delay = int(self.delay_entry.get())
        except:
            messagebox.showerror('Error', 'Choose an integer for delay.')
            return
        users = self.csv_users
        perform_action(action, tweet_link=account_link, comment=message, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='account')


if __name__ == "__main__":
    app = XAutomationApp()
    app.mainloop()
