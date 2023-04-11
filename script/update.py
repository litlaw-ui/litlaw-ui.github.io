import requests, feedparser
import datetime, os


header = '''+++
title = "ICYMI: $date"
date = "$date"
author = "Matthew Toms-Zuberec"
description = "Latest stories in cybersecurity for $date"
+++

---------------------------------------------------------------------------
## Latest Headlines
'''
footer = "**-- MTZ**"

# List of RSS feeds
site_list = ["https://threatpost.com/feed/", "https://feeds.feedburner.com/TheHackersNews?format=xml", "https://krebsonsecurity.com/feed/", "https://www.wired.com/feed/category/security/latest/rss", "http://feeds.feedburner.com/securityweek?format=xml", "https://cybersecuritynews.com/feed/", "https://www.bleepingcomputer.com/feed/"]
date_req = requests.get("https://worldtimeapi.org/api/timezone/America/Edmonton")

# Get yesterday and convert it to a time struct
today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
now = yesterday.timetuple()

# Replace date in header
header = header.replace("$date", str(yesterday))

posts = []

# Iterate list and write to file
for site in site_list:
    dgtw = feedparser.parse(site)
    for entry in dgtw["entries"]:
        # Check if it already exists
        if entry['title'] in [x['title'] for x in posts]:
            pass
        else:
            # Check if it's from the current time period
            if (entry.published_parsed[0],entry.published_parsed[1],entry.published_parsed[2]) == (now[0], now[1], now[2]):
                image = ""
                if ("media_thumbnail" in  entry):
                    image = entry["media_thumbnail"][0]["url"]
                elif ("media_content" in entry):
                    image = entry["media_content"][0]["url"]
                try:
                    posts.append({
                        "title": entry['title'],
                        "link": entry['link'],
                        "thumbnail": image
                    })
                except Exception as e:
                    print(e)

f = open("content/icymi/icymi-" + str(yesterday) + ".md", 'w+')
f.write(header)
for p in posts:
    # if(p["thumbnail"] != ""):
    #     f.write("![Placeholder](" + p["thumbnail"] + ") \n")
    f.write("- [" + p["title"] + "]" + "(" + p["link"] + ")\n\n")
f.write(footer)
f.close()
