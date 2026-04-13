# Task 1 - TrendPulse (Human Written Beginner Code with Simple Comments)

import requests   # to call API
import json       # to save data in json format
import time       # for delay
import os         # for folder creation
from datetime import datetime   # to get current date time

# urls (given in question)
url1 = "https://hacker-news.firebaseio.com/v0/topstories.json"
url2 = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# header (important, otherwise sometimes request fails)
headers = {"User-Agent": "TrendPulse/1.0"}

# categories with keywords (all small letters so easy matching)
cats = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

# function to find category using title
def find_cat(title):
    t = title.lower()   # convert to lowercase
    for c in cats:      # loop each category
        for k in cats[c]:   # loop each keyword
            if k in t:      # if keyword found in title
                return c
    return None   # if nothing matches


# main code starts here

# getting top story ids
try:
    r = requests.get(url1, headers=headers)
    ids = r.json()[:500]   # only first 500
except:
    print("problem getting ids")
    exit()   # stop if failed

final_data = []   # list to store all stories

# to track each category count (max 25)
count = {"technology":0,"worldnews":0,"sports":0,"science":0,"entertainment":0}

# loop each category one by one
for c in cats:
    print("collecting:", c)

    # loop through all ids
    for i in ids:

        # stop if already 25 collected
        if count[c] == 25:
            break

        # get each story data
        try:
            r2 = requests.get(url2.format(i), headers=headers)
            data = r2.json()
        except:
            print("error id", i)
            continue   # skip if error

        # skip if empty
        if data is None:
            continue

        # skip if no title
        if "title" not in data:
            continue

        # find category from title
        cat_found = find_cat(data["title"])

        # check if matches current category
        if cat_found == c:

            # create dictionary (manual way)
            d = {}
            d["post_id"] = data.get("id")
            d["title"] = data.get("title")
            d["category"] = cat_found
            d["score"] = data.get("score",0)
            d["num_comments"] = data.get("descendants",0)
            d["author"] = data.get("by","unknown")
            d["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            final_data.append(d)   # add to list
            count[c] += 1          # increase count

    time.sleep(2)   # wait after each category (important as per question)


# create folder if not exists
if not os.path.exists("data"):
    os.mkdir("data")

# file name with date
fname = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

# saving file
try:
    f = open(fname, "w")
    json.dump(final_data, f, indent=4)   # save nicely formatted
    f.close()
except:
    print("error saving file")

# final output
print("total collected:", len(final_data))
print("saved in:", fname)
