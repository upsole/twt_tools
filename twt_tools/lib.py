import re
import subprocess
import json

def link_parser(s):
    return re.sub(r'https://twitter.com/[a-zA-Z0-9_]*/[a-zA-Z0-9]*/', '', s)

def scrape_tweet(id):
    process = subprocess.Popen(f"snscrape --jsonl twitter-tweet {id}", stdout=subprocess.PIPE, shell=True)
    (output, err) = process.communicate()
    json_dict = json.loads(output.decode())
    return json_dict    
