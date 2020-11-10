import twint
import json
import os
import datetime;

OUTPUT_FOLDER_NAME = "output"

with open('parameters.json') as f:
  parameters = json.load(f)

ts = (datetime.datetime.now()-datetime.timedelta(minutes=parameters['num_minutes'])).strftime("%Y-%m-%d %H:%M:%S")
# print(ts)
#configure output folder
if not os.path.exists(OUTPUT_FOLDER_NAME):
    os.makedirs(OUTPUT_FOLDER_NAME)

for keyword in parameters['keywords']:
    if os.path.exists(OUTPUT_FOLDER_NAME + "/" + keyword['word'] + ".output"):
      os.remove(OUTPUT_FOLDER_NAME + "/" + keyword['word'] + ".output")

    c = twint.Config()
    c.Search = keyword['word']
    c.Filter_retweets = True
    c.Store_json = True
    c.Hide_output = True
    c.Since = ts
    c.Output = OUTPUT_FOLDER_NAME + "/" + keyword['word'] + ".output"
    twint.run.Search(c)
    # C.Profile_full = True #views shadow banned tweets, but takes a long time to see
    # Should probably use a filter to enusre latest tweets are received, but with such a large volume, it's almost guaranteed