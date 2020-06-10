# Wyvern

Scrapes the courselist of the [University of Guelph](https://uoguelph.ca) website and writes it all to a .CSV file. I used BeautifulSoup to traverse the DOM.

Example run:

```
python3 wyvern.py courses.csv
```

The .CSV file represents each course (row) with the following columns:

- Common Name
- Faculty
- Number
- Course Title
- Schedule
- Lecture Hours
- Lab Hours
- Weight
- Description
- Prerequisites
- Corequisites
- Restrictions
- Equates
- Departments
- Offerings
- External Course Codes
