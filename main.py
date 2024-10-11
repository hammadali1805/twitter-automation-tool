import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from utils import load_csv_file, find_tweets, create_report
from actions import *

import google.generativeai as genai
from gemini import paraphrase_content

from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

GOOGLE_API_KEY = "YOUR GEMINI API KEY HERE"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')



# Initialize WebDriver
def get_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


def perform_action(action, tweet_link, comment, paraphrase, language, delay, users, task_type, image_folder=None):
        
    if len(users)==0:
        messagebox.showerror('Error', 'No CSV selected or empty CSV selected.')
        return
    
    if (not comment) and (not image_folder) and (task_type=='post'):
        messagebox.showerror('Error', 'Give atleast one thing, message or image folder!')
        return

    # report cols = performedby, action, performedon, 

    driver = get_driver()
    report_content = [['PerformedBy', 'Action', 'PerfoedOn', 'Status', 'Comment']]


    if task_type=='link':

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if action == 'like':
                    if like_tweet(driver, tweet_link):
                        report_content.append([username, action, tweet_link, 'Success', ''])
                    else:
                        report_content.append([username, action, tweet_link, 'Failed', ''])

                elif action == 'retweet':                    
                    if retweet_tweet(driver, tweet_link):
                        report_content.append([username, action, tweet_link, 'Success', ''])
                    else:
                        report_content.append([username, action, tweet_link, 'Failed', ''])

                elif action == 'report':                    
                    if report_tweet(driver, tweet_link):
                        report_content.append([username, action, tweet_link, 'Success', ''])
                    else:
                        report_content.append([username, action, tweet_link, 'Failed', ''])

                elif action == 'comment':
                    if paraphrase:

                        new_comment = paraphrase_content(model, comment, language).strip('\n')
                        if new_comment:

                            if comment_tweet(driver, tweet_link, new_comment):
                                report_content.append([username, action, tweet_link, 'Success', new_comment])
                            else:
                                report_content.append([username, action, tweet_link, 'Failed', new_comment])
                        else:
                            report_content.append([username, action, tweet_link, 'Failed', new_comment])

                    else:
                        if comment_tweet(driver, tweet_link, comment):
                            report_content.append([username, action, tweet_link, 'Success', comment])
                        else:
                            report_content.append([username, action, tweet_link, 'Failed', comment])

                logout(driver)
                time.sleep(delay)
            else:
                report_content.append([username, action, tweet_link, 'Failed', ''])


    elif task_type=='keyword':

        if login(driver, users[0][0], users[0][1], users[0][2]):
            tweets = find_tweets(driver, tweet_link, len(users))
            logout(driver)

            if tweets:
                for tweet, (username, password, phone) in zip(tweets, users):

                    if login(driver, username, password, phone):

                        if action == 'like':
                            if like_tweet(driver, tweet):
                                report_content.append([username, action, tweet, 'Sucess', ''])
                            else:
                                report_content.append([username, action, tweet, 'Failed',  ''])


                        elif action == 'retweet':                    
                            if retweet_tweet(driver, tweet):
                                report_content.append([username, action, tweet, 'Success', ''])
                            else:
                                report_content.append([username, action, tweet, 'Failed', ''])



                        elif action == 'report':                    
                            if report_tweet(driver, tweet):
                                report_content.append([username, action, tweet, 'Success', ''])
                            else:
                                report_content.append([username, action, tweet, 'Failed', ''])


                        elif action == 'comment':
                            if paraphrase:

                                new_comment = paraphrase_content(model, comment, language).strip('\n')

                                if new_comment:

                                    if comment_tweet(driver, tweet, new_comment):
                                        report_content.append([username, action, tweet, 'Success', new_comment])
                                    else:
                                        report_content.append([username, action, tweet, 'Failed', new_comment])

                                else:
                                    report_content.append([username, action, tweet, 'Failed', new_comment])

                            else:

                                if comment_tweet(driver, tweet, comment):
                                    report_content.append([username, action, tweet, 'Success', comment])
                                else:
                                    report_content.append([username, action, tweet, 'Failed', comment])

                        logout(driver)
                        time.sleep(delay)
                    else:
                        report_content.append([username, action, tweet, 'Failed', ''])
            else:
                messagebox.showerror("Error", 'Unable to fetch tweets related to keyword. Please try again.')
        else:
            messagebox.showerror("Error", 'Unable to fetch tweets related to keyword. Please try again.')

    elif task_type=='account':

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if action == 'follow':
                    if follow_user(driver, tweet_link):
                        report_content.append([username, action, tweet_link, 'Success', ''])
                    else:
                        report_content.append([username, action, tweet_link, 'Failed', ''])


                elif action == 'report':                    
                    if report_user(driver, tweet_link):
                        report_content.append([username, action, tweet_link, 'Success', ''])
                    else:
                        report_content.append([username, action, tweet_link, 'Failed', ''])


                elif action == 'message':
                    if paraphrase:
                        new_comment = paraphrase_content(model, comment, language).strip('\n')

                        if new_comment:
                            
                            if message_user(driver, tweet_link, new_comment):
                                report_content.append([username, action, tweet_link, 'Success', new_comment])
                            else:
                                report_content.append([username, action, tweet_link, 'Failed', new_comment])

                        else:
                            report_content.append([username, action, tweet_link, 'Failed', new_comment])

                    else:
                        if message_user(driver, tweet_link, comment):
                            report_content.append([username, action, tweet_link, 'Success', comment])
                        else:
                            report_content.append([username, action, tweet_link, 'Failed', comment])

                logout(driver)
                time.sleep(delay)
            else:
                report_content.append([username, action, tweet_link, 'Failed', ''])



    elif task_type=='post':

        for username, password, phone in users:
            if login(driver, username, password, phone):

                if paraphrase:
                    new_comment = paraphrase_content(model, comment, language).strip('\n')

                    if new_comment:
                        
                        if post_tweet(driver, new_comment, image_folder):
                            report_content.append([username, action, str(image_folder), 'Success', new_comment])
                        else:
                            report_content.append([username, action, str(image_folder), 'Failed', new_comment])

                else:
                    if post_tweet(driver, comment, image_folder):
                        report_content.append([username, action, str(image_folder), 'Success', comment])
                    else:
                        report_content.append([username, action, str(image_folder), 'Failed', comment])

                logout(driver)
                time.sleep(delay)
            else:
                report_content.append([username, action, str(image_folder), 'Failed', comment])        

    create_report(report_content)
    driver.quit()
    messagebox.showinfo("SUCCESS", "Automation task has been completed.")


# Main Application Class
class XAutomationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Twitter Automation Tool")
        self.geometry("800x500")
        self.configure(bg="#1DA1F2")  # Twitter blue background

        # Set the Twitter logo as favicon
        self.iconbitmap('twitter.ico')  # Change to your actual Twitter logo path

        # Twitter Logo
        logo = Image.open("twitter.png")  # Change to your actual Twitter logo path
        logo = logo.resize((50, 50), Image.Resampling.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(logo)
        logo_label = ttk.Label(self, image=self.logo_image, background="#1DA1F2")
        logo_label.pack(pady=10)

        # Title Label
        title_label = ttk.Label(self, text="Twitter Automation Tool", font=("Helvetica", 24, "bold"), background="#1DA1F2", foreground="white")
        title_label.pack(pady=10)

        # Notebook (Tab View)
        style = ttk.Style()
        # style.configure("TNotebook", background="#1DA1F2", foreground="white")
        # style.configure("TNotebook.Tab", background="white", foreground="black", padding=[5, 5])
        # style.map("TNotebook.Tab", background=[("selected", "black")], foreground=[("selected", "#1DA1F2")])

        style.theme_use("clam")
        style.configure("TButton", background="#4CAF50", foreground="white", font=('Arial', 10, 'bold'), padding=10)
        style.configure("TLabel", font=('Arial', 10), foreground="#333")
        style.configure("TEntry", font=('Arial', 10), padding=5)

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(padx=10, pady=10, expand=True)

        # Tabs
        self.tweet_tab = ttk.Frame(self.notebook)
        self.keyword_tab = ttk.Frame(self.notebook)
        self.account_tab = ttk.Frame(self.notebook)
        self.post_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.tweet_tab, text="Tweet Link Actions")
        self.notebook.add(self.keyword_tab, text="Keyword Actions")
        self.notebook.add(self.account_tab, text="Account Actions")
        self.notebook.add(self.post_tab, text="Post Tweet")

        # --- Tweet Link Tab UI ---
        self.create_tweet_tab()

        # --- Keyword Tab UI ---
        self.create_keyword_tab()

        # --- Account Tab UI ---
        self.create_account_tab()

        # --- Post Tweet Tab UI--
        self.create_post_tab()

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
        self.language_dropdown = ttk.OptionMenu(self.tweet_tab, self.language_var, "English", "English", "Urdu", "Hindi", "Bengali")

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
        self.keyword_language_dropdown = ttk.OptionMenu(self.keyword_tab, self.keyword_language_var, "English", "English", "Urdu", "Hindi", "Bengali")

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
        self.account_language_dropdown = ttk.OptionMenu(self.account_tab, self.account_language_var, "English", "English", "Urdu", "Hindi", "Bengali")

        ttk.Label(self.account_tab, text="Delay (seconds):").grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
        self.account_delay_entry = ttk.Entry(self.account_tab, width=10)
        self.account_delay_entry.grid(row=4, column=1, padx=10, pady=10)
        self.account_delay_entry.insert(0, "1")

        ttk.Button(self.account_tab, text="Start", command=self.start_account_actions).grid(row=5, column=1, padx=10, pady=10)

    def create_post_tab(self):
        # Upload CSV button
        ttk.Button(self.post_tab, text="Upload CSV", command=self.load_csv).grid(row=0, column=0, padx=10, pady=10)
        self.csv_label_post = ttk.Label(self.post_tab, text="No file selected")
        self.csv_label_post.grid(row=0, column=1, padx=10, pady=10)
        self.csv_users = []

        # ttk.Label(self.account_tab, text="Account Link:").grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        # self.account_link = ttk.Entry(self.account_tab, width=40)
        # self.account_link.grid(row=1, column=1, padx=10, pady=10)

        # self.account_action_var = tk.StringVar(value="follow")
        # account_actions = ["follow", "follow", "report", "message"]
        # self.account_action_dropdown = ttk.OptionMenu(self.account_tab, self.account_action_var, *account_actions, command=self.toggle_message)
        # self.account_action_dropdown.grid(row=2, column=1, padx=10, pady=10)

        self.post_message_label = ttk.Label(self.post_tab, text="Message:")
        self.post_message_entry = ttk.Entry(self.post_tab, width=40)
        self.post_paraphrase_var = tk.IntVar()
        self.post_paraphrase_checkbox = ttk.Checkbutton(self.post_tab, text="Paraphrase", variable=self.post_paraphrase_var)
        self.post_language_var = tk.StringVar(value="English")
        self.post_language_dropdown = ttk.OptionMenu(self.post_tab, self.post_language_var, "English", "English", "Urdu", "Hindi", "Bengali")
        self.post_message_label.grid(row=1, column=0, padx=10, pady=10)
        self.post_message_entry.grid(row=1, column=1, padx=10, pady=10)
        self.post_paraphrase_checkbox.grid(row=1, column=2, padx=10, pady=10)
        self.post_language_dropdown.grid(row=1, column=3, padx=10, pady=10)

        # Upload Images button
        ttk.Button(self.post_tab, text="Select Images Folder", command=self.load_image_folder).grid(row=2, column=0, padx=10, pady=10)
        self.image_label_post = ttk.Label(self.post_tab, text="No folder selected")
        self.image_label_post.grid(row=2, column=1, padx=10, pady=10)
        self.image_folder = ''
        tk.Button(self.post_tab, text="X", command=self.remove_image_folder).grid(row=2, column=2, padx=10, pady=10)


        ttk.Label(self.post_tab, text="Delay (seconds):").grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
        self.post_delay_entry = ttk.Entry(self.post_tab, width=10)
        self.post_delay_entry.grid(row=3, column=1, padx=10, pady=10)
        self.post_delay_entry.insert(0, "1")

        ttk.Button(self.post_tab, text="Start", command=self.start_post_actions).grid(row=5, column=1, padx=10, pady=10)

    def toggle_comment(self, *args):
        if self.action_var.get() == "comment":
            self.comment_label.grid(row=3, column=0, padx=10, pady=10)
            self.comment_entry.grid(row=3, column=1, padx=10, pady=10)
            self.paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.comment_label.grid_forget()
            self.comment_entry.grid_forget()
            self.paraphrase_checkbox.grid_forget()
            self.language_dropdown.grid_forget()

    def toggle_keyword_comment(self, *args):
        if self.keyword_action_var.get() == "comment":
            self.keyword_comment_label.grid(row=3, column=0, padx=10, pady=10)
            self.keyword_comment_entry.grid(row=3, column=1, padx=10, pady=10)
            self.keyword_paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.keyword_language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.keyword_comment_label.grid_forget()
            self.keyword_comment_entry.grid_forget()
            self.keyword_paraphrase_checkbox.grid_forget()
            self.keyword_language_dropdown.grid_forget()

    def toggle_message(self, *args):
        if self.account_action_var.get() == "message":
            self.message_label.grid(row=3, column=0, padx=10, pady=10)
            self.message_entry.grid(row=3, column=1, padx=10, pady=10)
            self.account_paraphrase_checkbox.grid(row=3, column=2, padx=10, pady=10)
            self.account_language_dropdown.grid(row=3, column=3, padx=10, pady=10)
        else:
            self.message_label.grid_forget()
            self.message_entry.grid_forget()
            self.account_paraphrase_checkbox.grid_forget()
            self.account_language_dropdown.grid_forget()

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            self.csv_users = load_csv_file(file_path)  # You can update this to actually load the CSV content.
            self.csv_label_tweet.config(text=file_path)  # Update label with the file path
            self.csv_label_keyword.config(text=file_path)  # Update label with the file path
            self.csv_label_account.config(text=file_path)  # Update label with the file path
            self.csv_label_post.config(text=file_path)  # Update label with the file path
        else:
            self.csv_label_tweet.config(text="No file selected")

    def load_image_folder(self):
        folder_path = filedialog.askdirectory()  # Ask the user to select a directory
        if folder_path:
            self.image_folder = folder_path
            self.image_label_post.config(text=folder_path)  # Update label with the file path
        else:
            self.image_label_post.config(text="No folder selected")

    def remove_image_folder(self):
        self.image_folder = ''
        self.image_label_post.config(text="No folder selected")

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

    def start_post_actions(self):
        message = self.post_message_entry.get()
        paraphrase = bool(self.post_paraphrase_var.get())
        language = self.post_language_var.get()
        image_folder = self.image_folder

        try:
            delay = int(self.delay_entry.get())
        except:
            messagebox.showerror('Error', 'Choose an integer for delay.')
            return
        users = self.csv_users
        perform_action('post', tweet_link=None, comment=message, paraphrase=paraphrase, language=language, delay=delay, users=users, task_type='post', image_folder=image_folder)


if __name__ == "__main__":
    app = XAutomationApp()
    app.mainloop()