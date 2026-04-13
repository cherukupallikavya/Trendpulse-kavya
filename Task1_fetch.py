# Task 1 - TrendPulse (Guaranteed 100+ Stories Version)

import requests
import json
import time
import os
import random
from datetime import datetime

url1 = "https://hacker-news.firebaseio.com/v0/topstories.json"
url2 = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

cats = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm"],
    "worldnews": ["war","government","country","president","election","climate","attack","global"],
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship"],
    "science": ["research","study","space","physics","biology","discovery","nasa","genome"],
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming"]
}

# function to find category
def find_cat(title):
    t = title.lower()
    for c in cats:
        for k in cats[c]:
            if k in t:
                return c
    return None

# get ids
try:
    r = requests.get(url1, headers=headers)
    ids = r.json()
    random.shuffle(ids)
except:
    print("problem getting ids")
    exit()

final_data = []
count = {"technology":0,"worldnews":0,"sports":0,"science":0,"entertainment":0}

# IMPORTANT: keep looping until we reach at least 100
for c in cats:
    print("collecting:", c)

    for i in ids:

        if count[c] >= 25:
            break

        try:
            r2 = requests.get(url2.format(i), headers=headers)
            data = r2.json()
        except:
            continue

        if not data or "title" not in data:
            continue

        cat_found = find_cat(data["title"])

        if cat_found == c:
            d = {}
            d["post_id"] = data.get("id")
            d["title"] = data.get("title")
            d["category"] = cat_found
            d["score"] = data.get("score",0)
            d["num_comments"] = data.get("descendants",0)
            d["author"] = data.get("by","unknown")
            d["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            final_data.append(d)
            count[c] += 1

    time.sleep(2)

# if still less than 100, do one more pass
if len(final_data) < 100:
    print("Less data, running again...")

    for i in ids:
        if len(final_data) >= 110:
            break

        try:
            r2 = requests.get(url2.format(i), headers=headers)
            data = r2.json()
        except:
            continue

        if not data or "title" not in data:
            continue

        cat_found = find_cat(data["title"])

        if cat_found:
            d = {}
            d["post_id"] = data.get("id")
            d["title"] = data.get("title")
            d["category"] = cat_found
            d["score"] = data.get("score",0)
            d["num_comments"] = data.get("descendants",0)
            d["author"] = data.get("by","unknown")
            d["collected_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            final_data.append(d)

# save file
if not os.path.exists("data"):
    os.mkdir("data")

fname = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

with open(fname, "w") as f:
    json.dump(final_data, f, indent=4)

print("total collected:", len(final_data))
print("saved in:", fname)
