#!/usr/bin/env python

# Script to pull the latest 10 'past broadcasts' from a twitch.tv profile
# Uses livestreamer(badly, through subprocess)

# Intended to be run as cron

# Change these variables to suit you needs
# Or better yet, abstract them into a config file

video_count = 3
storage_directory = '/home/nibz/Videos/sc'

import os
import subprocess
import sys

import requests

try:
    channel = sys.argv[1]
except:
    print "Need channel name"
    print "{0} CHANNELNAME".format(sys.argv[0])
    sys.exit(1)


stream_url = "https://api.twitch.tv/kraken/channels/{0}/videos?limit={1}&offset=0&broadcasts=true&on_site=1".format(channel, video_count)

r = requests.get(stream_url)

for video in r.json()["videos"]:
    print video["title"]
    print video["created_at"]
    print video["url"]
    print

for video in r.json()["videos"]:
    print
    print "Pulling..."
    print video["title"]
    print video["created_at"]
    print video["url"]
    filename = "{0}-{1}.mp4".format(channel, video["created_at"])
    print "Saving to {0}".format(filename)
    if os.path.isfile(storage_directory + "/" + filename):
        print "Video already downloaded, skipping"
        continue
    ls = subprocess.Popen(["livestreamer",
                           "-o",
                           filename,
                           video["url"],
                           "source"],
                          cwd=storage_directory,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE)
    out, err = ls.communicate()
    print out, err
