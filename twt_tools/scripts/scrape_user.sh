#!/bin/bash
target_user=$1
snscrape --jsonl --max-results 50 twitter-user $target_user | sed '1s/^/[/;$!s/$/,/;$s/$/]/' > $target_user"_tweets.json"
echo "Formating data..."
prettier --write $target_user"_tweets.json"
