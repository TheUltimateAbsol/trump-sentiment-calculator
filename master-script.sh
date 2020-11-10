#!/bin/sh
while :
do
    echo "$(date): Process Started!"
    cd ~/trump-sentiment-calculator
    git pull
    echo "$(date): Updated Caculator Repo!"
    python3.7 get_tweets.py
    echo "$(date): Got tweets!"
    timestamp=$(python3.7 get_tweet_sentiment.py)
    echo "$(date): Calculated Tweets!"
    git add *
    git commit -m "Regular Data Push"
    git push
    echo "$(date): Published Fetched Tweets!"
    cd ~/trump-sentiment
    git pull
    git commit -m "$timestamp pulled latest site changes"
    cp ~/trump-sentiment-calculator/output/results.log src/results.log
    cp ~/trump-sentiment-calculator/output/trump.output src/trump.output
    cp ~/trump-sentiment-calculator/output/biden.output src/biden.output
    cp ~/trump-sentiment-calculator/output/data.json src/data.json
    git add src/results.log src/trump.output src/biden.output src/data.json
    git commit -m "$timestamp data update"
    git push
    echo "$(date): Published Data!"
    npm run deploy
    echo "$(date): Built Website!"
    #echo "$(date): Sleeping for 5 minutes!"
    #sleep 5m
done
