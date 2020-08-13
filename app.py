import praw
import keyboard
import time
from PIL import Image
import math
from glob import glob
import random
import requests
import re
import pprint
import importlib
import datetime
import urllib.request
import string
import sys
import os
from config import config
from reddit import reddit, IsImageLink, DLimage
from bs4 import BeautifulSoup
from bot import bot, post_ids

filepath = "images"

subreddits = ['dankmemes', 'memes', 'wholesomememes', 'comedyheaven']

tags = "#meme #getluusy #dankmemes"

caption = "Follow @get.luusy for more"

waitTime = 2

numRounds = 100

postFrequency = 500

POST_CACHE = "cache.txt"

number_of_pics = 4

if not os.path.exists(POST_CACHE):
    with open(POST_CACHE, "w"):
        pass

if not os.path.exists(filepath):
    os.makedirs(filepath)


def already_uploaded(post_id):
    """Check if the reddit instagram bot has already post with image"""
    found = False

    with open(POST_CACHE, "r") as in_file:
        for line in in_file:
            if post_id in line:
                found = True
                break
    return found


def log_insta(post_ids):
    for post_id in post_ids:
        with open(POST_CACHE, "a") as out_file:
            out_file.write(str(post_id) + "\n")


def CropToInstagram(filename):
    img = Image.open(filename)

    x, y = img.size

    if x/y > 16/9:
        new_x = y * 16/9
        left_x = x/2 - new_x/2
        right_x = x/2 + new_x/2

        img = img.crop((left_x, 0, right_x, y))
    elif x/y < 4/5:  # vertical
        new_y = x*5/4
        top_y = y/2 - new_y/2

        bottom_y = top_y+new_y

        img = img.crop((0, top_y, x, bottom_y))

    try:

        new_name = filename[:-3]+'jpg'
        img = img.convert('RGB')
        os.unlink(filename)
        img.save(new_name)
        filename = new_name
    except Exception as e:
        print(e)

    return filename


counter = 0
for x in range(numRounds):
    red = random.choice(subreddits)
    print(red)
    subreddit = reddit.subreddit(red)
    new_memes = subreddit.hot(limit=number_of_pics)
    authors = []

    photoAlbum = []
    print("Round/post number:", x)
    for submission in new_memes:
        if submission.is_self == True:
            print("Post was text, skipping to next post.")
            continue
        else:
            pass
        url = submission.url
        time.sleep(waitTime)
        fileName = str(submission)

        time.sleep(waitTime)

        # try:
        #         DLimage(url, filePath, fileName)
        # except:
        #         print("scratch that, next post.")
        #         continue
        if IsImageLink(url) and not already_uploaded(submission.id):
            try:
                img = requests.get(submission.url)
                filename = str(counter)+'.'+IsImageLink(submission.url)
                print(filename)
                filename = os.path.join('images', filename)
                print(filename)

                imagefile = open(filename, 'wb')
                imagefile.write(img.content)
                imagefile.close()
                post_ids.append(submission.id)
                log_insta(post_ids)

                filename = CropToInstagram(filename)
                # dictionary format
                photoAlbum.append(
                    {'File': filename, 'Title': submission.title})

                counter += 1
            except Exception as e:
                print(e)

        elif str(submission.url).lower().startswith('https://imgur.com') or str(submission.url).lower().startswith('http://imgur.com') and counter < max_images:
            try:
                html_page = urllib.request.urlopen(submission.url)
                soup = BeautifulSoup(html_page, 'lxml')
                images = []
                for img in soup.findAll('img'):
                    images.append('https:'+img.get('src'))

                img = requests.get(images[0])
                filename = str(counter)+'.'+images[0][-3:]
                filename = os.path.join('images', filename)
                imagefile = open(filename, 'wb')
                imagefile.write(img.content)
                imagefile.close()

                filename = CropToInstagram(filename)

                # dictionary format
                photoAlbum.append(
                    {'File': filename, 'Title': submission.title})

                counter += 1
            except Exception as e:
                print(e)

    authors = ''.join(str(e + ', ') for e in authors)
    print(photoAlbum)
    for photo in photoAlbum:

        print(photo['File'])
        raju = photo['File']
        captionText = photo['Title']
        print("Temp Sleeping")
        time.sleep(30)

        bot.upload_photo(raju, caption=(captionText + '\n' + 'Pulled from ' + 'r/'+red + ' ' +
                                        'Reddit Authors:' + ' ' + authors[0:(len(authors)-2)] + '.' + '.' + '.' + '\n' + tags))
    for filename in glob(filepath + '/*'):
        os.remove(filename)

    print("Deleted Images")
    print("Sleeping")
    time.sleep(4000)
