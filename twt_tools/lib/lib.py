import re
import subprocess
import json
from datetime import datetime as dt
from dateutil import parser

def link_parser(s):
    return re.sub(r'\?.+', '', re.sub(r'https://twitter.com/[a-zA-Z0-9_]*/[a-zA-Z0-9]*/', '', s))

def scrape_tweet(id):
    process = subprocess.Popen(f"snscrape --jsonl twitter-tweet {id}", stdout=subprocess.PIPE, shell=True)
    (output, err) = process.communicate()
    json_dict = json.loads(output.decode())
    return json_dict    

def format_date(s):
    return dt.strftime(parser.parse(s), "%D %H:%M")


def fetch_media(tweet, s_name):
    if tweet["media"]:
        print("fecthing media files")
        for media_index, i in enumerate(tweet["media"]):
            if i.get("fullUrl"):
                image_fetch = subprocess.Popen(f"wget -q -O {s_name}_{media_index}.jpeg {i['fullUrl']}", shell = True)
                image_fetch.wait()
                print("Image saved")

            elif i.get("variants"):
                video_fetch = subprocess.Popen(f"wget -q -O {s_name}_{media_index}.mp4 {i['variants'][0]['url']}", shell = True)
                video_fetch.wait()
                print("media saved!")

        print("Finished fecthing media files!")


def get_media(url, s_name):
    clean_url = link_parser(url)
    tweet = scrape_tweet(clean_url)
    fetch_media(tweet, s_name)
