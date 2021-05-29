# Wyvern

5/29/2021 update: very broken at the moment, doesn't work unless you use a link that predates the time period `current` (for example `2017-2018`)

Scrapes the courselist of the [University of Guelph](https://uoguelph.ca) website and writes it all to a .CSV file. I used BeautifulSoup to traverse the DOM.

```
usage: wyvern.py [-h] [-v] [-u URL] outfile

positional arguments:
  outfile              output file name

  optional arguments:
    -h, --help         show this help message and exit
    -v, --verbose      verbose debug output
    -u URL, --url URL  specify calendar URL
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
