#!/bin/bash
target_ID=$1
snscrape --jsonl twitter-tweet $target_ID > $target_ID"_tweets.json"
echo "Formating data..."
prettier --write $target_ID"_tweets.json"
