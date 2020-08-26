run:
	python3 wyvern.py courses.csv

cmp:
	cmp courses.csv backup.csv
