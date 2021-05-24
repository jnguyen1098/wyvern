#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

opened = open("urls.tsv", "r")

urls = [line.split("\t")[1][:-1:] for line in opened]

if (len(urls) != 86):
    print("bad number of courses")
    exit()

for url in urls:
    html = requests.get(url)
    parsed = BeautifulSoup(html.content, "html.parser")
    for item in parsed.find_all("div", {"class": "courseblock"}):
        for thing in item.find_all(True):
            print(thing)
            print("lmao\n\n")
