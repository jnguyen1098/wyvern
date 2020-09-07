FILE=exitfile.csv

if [ -f "$FILE" ]; then
    echo "Intermediate file $FILE exists. Please date and rename it."
else
    mv courses.csv exitfile.csv
    python3 wyvern.py courses.csv
    cmp courses.csv exitfile.csv
fi
