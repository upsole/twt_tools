from lib import link_parser, scrape_tweet
import subprocess


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
