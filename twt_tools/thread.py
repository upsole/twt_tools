import subprocess
import os
import re
import time
import json
from twt_tools.lib.lib import link_parser, scrape_tweet, format_date
from md2pdf.core import md2pdf


class Thread:
    # link String: Url from the last tweet of the twitter thread
    # thread_name: Name of folder 
    def __init__(self, url, thread_name, output_dir=""):
        self.id = link_parser(url)
        self.thread_name = link_parser(thread_name)
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
            # print("Indexed tweet")
        # print("Scraping Finished")
        thread.reverse()
        return thread

    def thread_to_json(self):
        return json.dumps(self.thread)

    def get_images(self):
        thread = self.thread
        thread_name = self.thread_name
        os.makedirs(f"{self.src_folder}/{thread_name}/img", exist_ok=True)
        for tw_index, tw in enumerate(thread):
            if tw["media"]:
                print("Fetching media files...")
                for media_index, i in enumerate(tw["media"]):
                    if i.get("fullUrl"):
                        image_fetch = subprocess.Popen(f"wget -q -O {self.src_folder}/{thread_name}/img/{tw_index}_{media_index}.jpg {i['fullUrl']}", shell = True)
                        image_fetch.wait()
                        print("Image saved")

                    elif i.get("variants"):
                        video_fetch = subprocess.Popen(f"wget -q -O {self.src_folder}/{thread_name}/img/{tw_index}_{media_index}.mp4 {i['variants'][0]['url']}", shell = True)
                        video_fetch.wait()
                        thumb_fetch = subprocess.Popen(f"wget -q -O {self.src_folder}/{thread_name}/img/{tw_index}_{media_index}_thumb.jpg {i['thumbnailUrl']}", shell = True)
                        thumb_fetch.wait()
                        print("media saved!")

                print("Finished fecthing media files!")


    def build_markdown(self):
        thread = self.thread
        thread_name = self.thread_name
        self.get_images()
        f = open(f"{self.src_folder}/{thread_name}/{thread_name}.md", "w")
        f.write(f"### Author: @{thread[0]['user']['username']}\n")
        f.write(f"#### URL: {thread[0]['url']}\n")
        f.write(f"#### Date: {format_date(thread[0]['date'])}\n")
        for tw_index, tw in enumerate(thread):
            f.write("\n")
            f.write("---\n")
            f.write(f"# {str(tw_index + 1)}")
            f.write("\n")
            f.write(f"{re.sub(r'https://t.co/[a-zA-Z0-9_]*', '', tw['rawContent'])}\n")
            if tw["quotedTweet"]:
                f.write(f">## Quoting {tw['quotedTweet']['url']}\n")
                f.write(f">{tw['quotedTweet']['rawContent']}\n")
            if tw["media"]:
                f.write("<div style='display:flex; flex-direction: row; flex-wrap: wrap;'>")
                for media_index, i in enumerate(tw["media"]):
                    if i.get("fullUrl"):
                        f.write(f"<img src='img/{tw_index}_{media_index}.jpg' style='height: 350px; object-fit: contain;'/>")

                    if i.get("variants"):
                        f.write(f"<img src='img/{tw_index}_{media_index}_thumb.jpg' style='height: 350px; object-fit: contain;'/> \n")
                        f.write(f"Video URL: {i['variants'][0]['url']}")
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
        print("Cleanup finished. Build files are deleted")
