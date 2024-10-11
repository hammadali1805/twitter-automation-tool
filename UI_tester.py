import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import csv

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

def perform_action(action, tweet_link, comment, paraphrase, language, delay, users):
    # Placeholder for the actual automation action
    print(f"Action: {action}, Tweet: {tweet_link}, Comment: {comment}, Paraphrase: {paraphrase}, Language: {language}, Delay: {delay}, User: {users}")

def find_tweets(user, keyword, num_users):
    # Placeholder for finding tweets based on keywords
    return [f"Tweet_{i+1}" for i in range(num_users)]

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
        delay = int(self.delay_entry.get())
        users = self.csv_users
        if users:
            for user in users:
                perform_action(action, tweet_link=tweet_link, comment=comment, paraphrase=paraphrase, language=language, delay=delay, users=user)

    def start_keyword_actions(self):
        keyword = self.keyword_entry.get()
        action = self.keyword_action_var.get()
        comment = self.keyword_comment_entry.get() if action == "comment" else None
        paraphrase = bool(self.keyword_paraphrase_var.get())
        language = self.keyword_language_var.get()
        delay = int(self.keyword_delay_entry.get())
        users = self.csv_users
        if users:
            for user in users:
                found_tweets = find_tweets(user, keyword, len(users))
                for tweet in found_tweets:
                    perform_action(action, tweet_link=tweet, comment=comment, paraphrase=paraphrase, language=language, delay=delay, users=user)

    def start_account_actions(self):
        account_link = self.account_link.get()
        action = self.account_action_var.get()
        message = self.message_entry.get() if action == "message" else None
        paraphrase = bool(self.account_paraphrase_var.get())
        language = self.account_language_var.get()
        delay = int(self.account_delay_entry.get())
        users = self.csv_users
        if users:
            for user in users:
                perform_action(action, tweet_link=account_link, comment=message, paraphrase=paraphrase, language=language, delay=delay, users=user)


if __name__ == "__main__":
    app = XAutomationApp()
    app.mainloop()
