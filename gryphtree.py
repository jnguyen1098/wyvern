# Gryphtree
# Analyzes course descriptions

import pygraphviz
import pydot

import re
import pandas

import requests
import time

from bs4 import BeautifulSoup

rx_dict = {
    'title': re.compile(r'.*\(\d\-\d\) \[\d\.\d\d\]'),
    'restrictions': re.compile(r'Restriction\(s\):.*AAAAA'),
    'prerequisites': re.compile(r'Prerequisite\(s\):.*AAAAA')
}

def parse_line(number, line):
    """
        It's regex time 
    """
    for key, rx in rx_dict.items():
        match = rx.match(line)
        if match:
            print("line {}: [{}]".format(number, line))

gryph_url = "https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/"

print("Accessing", gryph_url)
page = requests.get(gryph_url)

print("Parsing result into BeautifulSoup")
homepage = BeautifulSoup(page.content, 'html.parser')

faculties = {}

print("Scraping course codes")
sidebar_links = homepage.find_all("a")
for link in sidebar_links:
    try:
        match = re.match(r'\.\/c12(.+)\.shtml', link['href'])
        if match:
            faculties[match.group(1)] = gryph_url + match.group(0)[2:]
    except:
        pass

for faculty, link in faculties.items():
    print(link)

deathgex = re.compile(r"^([A-Z]{2,4})\*([0-9]{4}) ([A-Za-z0-9 \?–\&'\(\)\:\/,\.\-]+) ([SFWU,]{1,7}|P1|P2|P3|P4) \(([0-9V\.]{1,3})\-([0-9V\.]{1,3})\) \[([0-9]\.[0-9][0-9])\]$")
match = deathgex.match("ACCT*1220 Introductory Financial Accounting F,W (3-0) [0.50]")
if match:
    print("{},{},'{}',[{}],({}-{}),{}".format(match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), match.group(6), match.group(7)))

total = 0
for key, value in faculties.items():
    #print("Scraping", value)
    page = requests.get(value)
    faculty = BeautifulSoup(page.content, 'html.parser')
    courses = faculty.find_all("div", class_="course")
    cnt = 0
    for course in courses:
        candidates = course.find_all("a", {'name': re.compile(r'[A-Z]{2,4}[0-9]{4}')})
        for candidate in candidates:
            print(candidate.text)
            cnt += 1
    print("There are", cnt, "courses in", key)
    total += cnt

print("there are", total, "courses at uog")

exit()

G = pygraphviz.AGraph('testgraph.dot')
G.layout(prog='dot')
G.add_node('b')
G.write('output.gv')

graphs = pydot.graph_from_dot_file('output.gv')
graphs[0].write_svg('output.svg')
