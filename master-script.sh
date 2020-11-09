#!/bin/sh
do
    date + "%R: Process Started!"
    cd ~/trump-sentiment-calculator
    python3 get_tweets.py
    date + "%R: Got tweets!"
    timestamp=$(python3 get_tweet_sentiment.py)
    date + "%R: Calculated Tweets!"
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
    date + "%R: Published Data!"
    npm run deploy
    date + "%R: Built Website!"
    date + "%R: Sleeping for 5 minutes!"
    sleep 5m
done
