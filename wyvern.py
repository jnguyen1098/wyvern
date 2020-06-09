#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import csv
import sys
import re

def main(argv):

    gryph_url_default = "https://www.uoguelph.ca/registrar/calendars/undergraduate/current/c12/"

    if len(argv) > 3 or len(argv) == 1:
        print("Usage:", argv[0], "outfile [calendarurl]")
        exit()

    if len(argv) == 2:
        print("No calendar url specified; will default to", gryph_url_default)
        gryph_url = gryph_url_default
    else:
        gryph_url = argv[2]

    print("Loading...", gryph_url)
    page = requests.get(gryph_url)

    print("Creating BeautifulSoup...")
    homepage = BeautifulSoup(page.content, 'html.parser')

    faculties = {}

    print("Scraping course codes...")
    sidebar_links = homepage.find_all("a")
    for link in sidebar_links:
        try:
            match = re.match(r'\.\/c12(.+)\.shtml', link['href'])
            if match:
                faculties[match.group(1)] = gryph_url + match.group(0)[2:]
        except:
            pass

    print("Urls ready:")
    for faculty, link in faculties.items():
        print(link)

    print("Getting regex ready...")
    deathgex        = re.compile(r"^([A-Z]{2,4})\*([0-9]{4}) ([A-Za-z0-9 \?–\&'\(\)\:\/,\.\-]+) ([SFWU,]{1,7}|P1|P2|P3|P4) \(([0-9V\.]{1,3})\-([0-9V\.]{1,3})\) \[([0-9]\.[0-9][0-9])\]$")
    restrictiongex  = re.compile(r"\nRestriction\(s\)\:\n(.*)")
    prereqgex       = re.compile(r"\nPrerequisite\(s\):\n(.*)")
    coreqgex        = re.compile(r"\nCo\-requisite\(s\):\n(.*)")
    equategex       = re.compile(r"\nEquate\(s\):\n(.*)")
    departmentgex   = re.compile(r"\nDepartment\(s\):\n(.*)")
    offeringgex     = re.compile(r"\nOffering\(s\):\n(.*)")
    externalgex     = re.compile(r"\nExternal Course Code\(s\):\n(.*)")


    print("Overwriting 'courses.csv' for export...")
    guelphWriter = csv.writer(open(argv[1], 'w'))
    guelphWriter.writerow(['Common Name', 'Faculty', 'Number', 'Course Title', 'Schedule', 'Lecture Hours', 'Lab Hours', 'Weight', 'Description', 'Prerequisites', 'Corequisites', 'Restrictions', 'Equates', 'Departments', 'Offerings', 'External Course Codes'])

    curr_fac = 0
    total = 0

    print("Iterating over faculties...")
    for key, value in faculties.items():
        cnt = 0
        curr_fac += 1
        print("Scraping", key, "({}/{})".format(curr_fac, len(faculties)))
        page = requests.get(value)
        faculty = BeautifulSoup(page.content, 'html.parser')
        courses = faculty.find_all("div", class_="course")
        for course in courses:
            # Variables
            common_name                 = None
            faculty                     = None
            number                      = None
            title                       = None
            semesters                   = None
            lecture_hours               = None
            lab_hours                   = None
            weight                      = None
            description_text            = None
            prerequisite_text           = None
            corequisite_text            = None
            restriction_text            = None
            equate_text                 = None
            department_text             = None
            offering_text               = None
            external_course_code_text   = None

            # Find course
            candidates = course.find_all("a", {'name': re.compile(r'[A-Z]{2,4}[0-9]{4}')})
            for candidate in candidates:
                match = deathgex.match(candidate.text)
                if match:
                    common_name = match.group(1) + "*" + match.group(2)
                    faculty = match.group(1)
                    number = match.group(2)
                    title = match.group(3)
                    semesters = match.group(4)
                    lecture_hours = match.group(5)
                    lab_hours = match.group(6)
                    weight = match.group(7)
            
            # Find prerequisites
            prerequisites = course.find_all("tr", class_="prereqs")
            for prerequisite_text in prerequisites:
                match = prereqgex.match(prerequisite_text.text)
                if match:
                    prerequisite_text = match.group(1)
                else:
                    print("??", prerequisite_text.text)
                    raise Exception('Prerequisite failure')

            # Find corequisites
            corequisites = course.find_all("tr", class_="coreqs")
            for corequisite in corequisites:
                match = coreqgex.match(corequisite.text)
                if match:
                    corequisite_text = match.group(1)
                else:
                    raise Exception('Corequisite failure')

            # Find restrictions
            restrictions = course.find_all("tr", class_="restrictions")
            for restriction_text in restrictions:
                match = restrictiongex.match(restriction_text.text)
                if match:
                    restriction_text = match.group(1)
                else:
                    print("??", restriction_text.text)
                    raise Exception('Restriction failure')

            # Find description
            description = course.find_all("tr", class_="description")
            if description[0]:
                description_text = re.sub(r'[ ]+', ' ', description[0].text).replace("\n","")
            else:
                raise Exception('Description failure')

            # Find equates
            equate = course.find_all("tr", class_="equates")
            for eq in equate:
                match = equategex.match(eq.text)
                if match:
                    equate_text = match.group(1)
                else:
                    raise Exception('Equate failure')

            # Find department
            department = course.find_all("tr", class_="departments")
            for depart in department:
                match = departmentgex.match(depart.text)
                if match:
                    department_text = match.group(1)
                else:
                    raise Exception('Department failure')

            # Find offering
            offering = course.find_all("tr", class_="offerings")
            for offer in offering:
                match = offeringgex.match(offer.text)
                if match:
                    offering_text = match.group(1)
                else:
                    raise Exception('Offering failure')

            # Find external course code
            external_code = course.find_all("tr", class_="externalinfo")
            for external in external_code:
                match = externalgex.match(external.text)
                if match:
                    external_course_code_text = match.group(1)
                else:
                    raise Exception('External code failure')
                    
            # Output
            """
            print(common_name)
            print("Faculty:", faculty)
            print("Number:", number)
            print("Title:", title)
            print("Schedule:", semesters)
            print("Lecture hours:", lecture_hours)
            print("Lab hours:", lab_hours)
            print("Course weight:", weight)
            print("Description_text:", description_text)
            print("Prerequisites:", prerequisite_text)
            print("Corequisites:", corequisite_text)
            print("Restrictions:", restriction_text)
            print("Equates:", equate_text)
            print("Departments:", department_text)
            print("Offerings:", offering_text)
            print("External course codes:", external_course_code_text)
            print("     ")
            print("     ")
            """
            guelphWriter.writerow([common_name, faculty, number, title, semesters, lecture_hours, lab_hours, weight, description_text, prerequisite_text, corequisite_text, restriction_text, equate_text, department_text, offering_text, external_course_code_text])
            cnt += 1

        # Done
        print("Scraped", cnt, "courses in", key)
        print("")
        total += cnt

    print("Scraped", total, "courses at uog")

if __name__ == "__main__":
    sys.exit(main(sys.argv))
