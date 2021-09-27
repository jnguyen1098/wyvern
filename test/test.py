#!/usr/bin/env python3

import requests
import sys
import time

from bs4 import BeautifulSoup

HEADERS = {
    "Content-Type": "application/json, charset=UTF-8",
    "Cookie": "__RequestVerificationToken_L1N0dWRlbnQ1=7wcHRu4kId0vHsK5AVX-QPXg\
        K1k9MOr-YhjsAfwnI909uGdGg4IiYpbeSx3VZAwNuRfDlmBhv-tFUSvm6EhBo-9Vj_IShNK\
        TxVQTVOtWjto1",
    "__RequestVerificationToken": "usYD9CwPoPKaoX777i1AXd77m1RjN290BQLVR7WfVzir\
        PpFxdgi4kUbV4YPHJ31X2SKfwfTZnNhS5XfUc1Wicec1sIg_9THnbxASoF_OXbs1",
    "X-Requested-With": "XMLHttpRequest",
}

with open("links", "r") as links:
    for idx, link in enumerate(links):
        print(f"{idx + 1}/86: {link}", file=sys.stderr)
        page = requests.get(link.strip(), headers=HEADERS)
        faculty = BeautifulSoup(page.content, 'html.parser')
        courses = faculty.find_all("div", class_="courseblock")
        for course in courses:
            spans = course.find_all("span")
            for span in spans:
                strongs = span.find_all("strong")
                first_text = strongs[0].text if strongs else None
                if first_text == "Prerequisite(s): ":
                    if '"' in spans[0].text:
                        print(f"EXCEPTION {spans[0].text}")
                        exit(1)
                    elif '"' in span.text:
                        print(f"EXCEPTION {span.text}")
                        exit(1)
                    print(f'"{spans[0].text}","{span.text.replace("Prerequisite(s): ","")}"')
        time.sleep(0.1)
