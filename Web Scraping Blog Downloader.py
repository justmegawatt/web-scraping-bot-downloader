# By Megg Gawat 2016 - MegawattApps.com

from bs4 import BeautifulSoup
import tkinter
import requests
import os


class UI(object):

    def __init__(self, window):
        self.window = window
        self.window.title("Blog Downloader")
        self.mainframe = tkinter.Frame(window)
        self.mainframe.pack(padx=10, pady=10)

        self.author = tkinter.StringVar()
        self.posts = tkinter.IntVar()

        self.build_interface()

    def build_interface(self):
        self.frame = tkinter.Frame(self.mainframe)
        self.frame.grid(row=0, column=0)

        self.build_title()
        self.build_instructions()
        self.build_author_blog()
        self.build_posts_blog()
        self.build_download_button()

    def build_title(self):
        title = tkinter.Label(self.frame, text="Blog Downloader", font=("-weight bold", 17))
        title.grid(column=0, row=0, columnspan=2)

    def build_instructions(self):
        instructions_text = "Instructions: Copy and paste exact username as shown on URL bar. Example: \"Megawatt\" in https://www.example.com/profile/Megawatt/"
        instructions = tkinter.Label(self.frame, text=instructions_text, wrap=400)
        instructions.grid(column=0, row=1, columnspan=2)

    def build_author_blog(self):
        author_label = tkinter.Label(self.frame, text="Author:")
        author_label.grid(column=0, row=2)

        author_blog = tkinter.blog(self.frame, textvariable=self.author, width=40)
        author_blog.grid(column=1, row=2)

    def build_posts_blog(self):
        author_label = tkinter.Label(self.frame, text="Total Posts:")
        author_label.grid(column=0, row=3)

        author_blog = tkinter.blog(self.frame, textvariable=self.posts, width=40)
        author_blog.grid(column=1, row=3)

    def build_download_button(self):
        download_button = tkinter.Button(self.frame, text="Download All Blog Posts", command=self.download_button_action)
        download_button.grid(column=0, row=4, columnspan=2, pady=5)

    def download_button_action(self):
        begin_downloading = Downloader(self.author.get(), self.posts.get())


class Downloader(object):
    def __init__(self, author, posts):
        self.author = author
        self.current_post = posts
        self.author_post = "https://www.Example.com/profile/" + self.author
        os.makedirs(author, exist_ok=True)
        os.chdir(author)

        self.main_loop()

    def main_loop(self):
        while self.current_post:
            # print(self.current_post)
            self.author_post_object = requests.get(self.author_post + "/post/" + str(self.current_post))
            #print(self.author_post + str(self.current_post))
            self.soup = BeautifulSoup(self.author_post_object.text, "html.downloader")

            self.find_links()
            for self.link in self.links:
                self.open_link()
                self.grab_title()
                self.title_cleaner()
                self.create_new_txt()
                self.grab_contents()
                self.write_content()
                self.comment_separator()
                self.grab_comments()
                self.write_comments()

            self.file.close()
            self.current_post -= 1

    def find_links(self):
        anchor_tags = self.soup.select('h2 > a')
        self.links = []
        for anchor_tag in anchor_tags:
            link = anchor_tag.get('href')
            self.links.append(link)

    def open_link(self):
        link_post_object = requests.get(self.link)
        self.link_soup = BeautifulSoup(link_post_object.text, "html.downloader")

    def grab_title(self):
        title_list = self.link_soup.select('.blog-title')
        self.title = title_list[0].getText()

    def title_cleaner(self):
        #Creates a title appropriate for file names
        words = self.title.split(" ")
        new_words = []
        for word in words:
            new_word = ''
            for ch in word:
                if ch.isalnum():
                    new_word += ch
            new_words.append(new_word)
        self.clean_title = ' '.join(new_words)

    def create_new_txt(self):
        self.file = open(self.clean_title + '.txt', 'w')
        self.file.write(self.title)
        self.file.write("\n")
        self.file.write("\n")

    def grab_contents(self):
        self.contents = self.link_soup.select('.blog-content > p')

    def write_content(self):
        for content in self.contents:
            try:
                self.file.write(content.getText())
            except:
                continue
            self.file.write("\n")
            self.file.write("\n")

    def comment_separator(self):
        self.file.write("-- Comments --")
        self.file.write("\n")

    def grab_comments(self):
        self.authors = self.link_soup.select('.author > a')
        self.times = self.link_soup.select('.comment-info > a > time')
        self.comments = self.link_soup.select('.comment-body')

    def write_comments(self):
        for i, author in enumerate(self.authors):
            comment = self.comments[i].getText()
            time = self.times[i].getText()
            self.file.write("\n")
            try:
                self.file.write(author.getText())
            except:
                self.file.write("Unknown Name")
            self.file.write("\n")
            for char in time:
                if char.isalnum() or char == " " or char == ":" or char == ",":
                    self.file.write(char)
            for letter in comment:
                try:
                    self.file.write(letter)
                except:
                    continue
            self.file.write("\n")

main_window = tkinter.Tk()
UI(main_window)
main_window.mainloop()
