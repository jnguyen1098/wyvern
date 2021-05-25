#!/usr/bin/env python3

new_codes = open("new_course_codes.txt") 
old_codes = open("old_course_codes.txt")

n_codes = set([code[:-1:] for code in new_codes])
o_codes = set([code[:-1:] for code in old_codes])

new_courses = sorted([code for code in n_codes if code not in o_codes])
del_courses = sorted([code for code in o_codes if code not in n_codes])

print("New courses:")
for course in new_courses:
    print(course)

print()

print("Deleted courses:")
for course in del_courses:
    print(course)
