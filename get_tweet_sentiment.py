import json
from sentiment import sentiment_score
import time
import datetime
OUTPUT_FOLDER_NAME = "output"

with open('parameters.json') as f:
  parameters = json.load(f)

featured_char_limit = parameters['featured_char_limit']
featured = []

sttime = ""
averages = []

#Read each output line in at a time as json
for keyword in parameters['keywords']:
    multiplier = keyword['weight']
    file1 = open(OUTPUT_FOLDER_NAME + '/' + keyword['word'] + '.output', 'r')
    lines = file1.readlines() 
    sttime =  json.loads(lines[0])['created_at']
    #print(keyword['word'])
    all_likes = 0
    all_retweets = 0
    score = 0
    num = 0
    for line in lines:
        data = json.loads(line)
        msg = data['tweet']
        likes = data['likes_count']
        retweets = data['retweets_count']
        like_score = likes * 0.5
        rewtweet_score = retweets * 1.0
        sentiment = sentiment_score(msg)
        if (sentiment < 0.3 or sentiment > 0.7):
            if multiplier == -1:
                sentiment = 1 - sentiment
            score += sentiment + like_score + rewtweet_score
            num += abs((1 + like_score + rewtweet_score))
        #Save featured tweets
        if len(msg) <= featured_char_limit and (not ("@" in msg)) and (not ("https://" in msg)):
            featured.append(data)
        all_likes += likes
        all_retweets += retweets
    score = score / num
    averages.append(score)
    # print("likes: ", all_likes, ", retweets", all_retweets)


total = 0
for a in averages:
    total += a
score = total / len(averages)
sentiment = round(score * 100, 1)
featured_out = []
#print("Sentiment: " + str(sentiment) + "%")
#print("Featured Tweets")
for tweet in featured:
    #print("@" + tweet['username'] + ": " + tweet['tweet'])
    featured_out.append({"username": tweet['username'] , "tweet": tweet['tweet']})



data = {
    "sentiment": sentiment,
    "featured": featured_out
}

with open(OUTPUT_FOLDER_NAME + "/" + 'data.json', 'w') as outfile:
    json.dump(data, outfile)

with open(OUTPUT_FOLDER_NAME + "/" + "results.log", "a") as file2:  # append mode 
    file2.write(sttime + ", " + str(sentiment) + "\n") 
    file2.close() 

print(sttime)