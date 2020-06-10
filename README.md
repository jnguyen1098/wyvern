# Wyvern

Scrapes the courselist of the [University of Guelph](https://uoguelph.ca) website and writes it all to a .CSV file. I used BeautifulSoup to traverse the DOM.

Example run:

```
python3 wyvern.py courses.csv
```

You'd only need to specify the `[calendarurl]` if the default URL becomes outdated. Please make an issue if there are any changes to the UofG website that break the scraper.

If you don't have the time to scrape an updated copy, there is a pre-made `courses.csv` file in this repo (though it may become outdated).

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
