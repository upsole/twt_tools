import subprocess
import json
import os
import re
import time
from md2pdf.core import md2pdf

def link_parser(s):
    return re.sub(r'https://twitter.com/[a-zA-Z0-9_]*/[a-zA-Z0-9]*/', '', s)

def scrape_tweet(id):
    process = subprocess.Popen(f"snscrape --jsonl twitter-tweet {id}", stdout=subprocess.PIPE, shell=True)
    (output, err) = process.communicate()
    json_dict = json.loads(output.decode())
    return json_dict    

class Thread:
    # link String: Url from the last tweet of the twitter thread
    # thread_name: Name of folder 
    def __init__(self, link, thread_name, output_dir=""):
        self.id = link_parser(link)
        self.thread_name = thread_name
        self.thread = self.build_thread(self.id)
        self.output_dir = os.path.abspath(output_dir)
        self.src_folder = os.path.abspath(os.path.join(output_dir, "scraped_files"))
        self.css = os.path.abspath(f"{os.path.dirname(__file__)}/github.css")

    def build_thread(self, id):
        thread = []
        last_tweet = scrape_tweet(id)
        thread.append(last_tweet)
        while thread[-1]["inReplyToTweetId"]:
            tw = scrape_tweet(thread[-1]["inReplyToTweetId"])
            thread.append(tw)
            print("Indexed tweet")
        print("Scraping Finished")
        thread.reverse()
        return thread

    def get_images(self):
        thread = self.thread
        thread_name = self.thread_name
        os.makedirs(f"{self.src_folder}/{thread_name}/img", exist_ok=True)
        for tw_index, tw in enumerate(thread):
            if tw["media"]:
                for media_index, i in enumerate(tw["media"]):
                    if i["fullUrl"]:
                        # os.system(f"wget -q -O scraped_files/{thread_name}/img/{tw_index}_{media_index}.jpg {i['fullUrl']}")
                        subprocess.Popen(f"wget -q -O {self.src_folder}/{thread_name}/img/{tw_index}_{media_index}.jpg {i['fullUrl']}", shell = True)
                        print("image saved")

    def build_markdown(self):
        thread = self.thread
        thread_name = self.thread_name
        self.get_images()
        f = open(f"{self.src_folder}/{thread_name}/{thread_name}.md", "w")
        f.write(f"### Author: @{thread[0]['user']['username']}\n")
        f.write(f"#### URL: {thread[0]['url']}\n")
        for tw_index, tw in enumerate(thread):
            f.write("\n")
            f.write("---\n")
            f.write(f"# {str(tw_index + 1)}")
            f.write("\n")
            f.write(f"{re.sub(r'https://t.co/[a-zA-Z0-9_]*', '', tw['content'])}\n")
            if tw["quotedTweet"]:
                f.write(f">## Quoting {tw['quotedTweet']['url']}\n")
                f.write(f">{tw['quotedTweet']['content']}\n")
            if tw["media"]:
                f.write("<div style='display:flex; flex-direction: row; flex-wrap: wrap;'>")
                for media_index, i in enumerate(tw["media"]):
                    if i["fullUrl"]:
                        f.write(f"<img src='img/{tw_index}_{media_index}.jpg' style='height: 350px; object-fit: contain;'/>")
                f.write("</div>")
        f.close()
        print(f"Written thread as {thread_name}/{thread_name}.md")        

    def build_pdf(self):
        thread_name = self.thread_name
        base_folder = f"{self.src_folder}/{thread_name}/"
        md_file = os.path.join(base_folder, f"{thread_name}.md")
        base_url = os.path.abspath(base_folder)
        pdf_name = f"{self.output_dir}/{self.thread_name}.pdf" 
        time.sleep(1)
        md2pdf(pdf_name, md_file_path=md_file, css_file_path=os.path.abspath(self.css), base_url=base_url)
        print(f"Conversion finished")

    def cleanup(self):
        os.system(f"rm -r {self.src_folder}/{self.thread_name}")
        if not os.listdir(f"{self.src_folder}"):
            os.rmdir(self.src_folder)
        print("Cleanup finished")