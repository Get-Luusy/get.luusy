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
from config import config

reddit = praw.Reddit(client_id=config["rd_client"], client_secret=config["rd_secret"],
                     username=config["rd_dev_name"], password=config["rd_dev_pass"], user_agent="tesh254")

def DLimage(url, filepath, filename):
    fullpath = filepath + filename + ".jpg"

    urllib.request.urlretrieve(url, fullpath)

def IsImageLink(url):
    LinkRegex = re.compile('((https:|http:)?\/\/.*\.(png|jpg|jpeg))')
    results = LinkRegex.findall(url)
    if results:
        return results[0][2]
    else:
        return False

