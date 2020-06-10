run:
	python3 wyvern.py courses.csv && cmp courses.csv backup.csv

cmp:
	cmp courses.csv backup.csv
