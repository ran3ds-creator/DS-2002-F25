import csv

def make_csv():
    data = [
        [1001, "Data Science", 3,    "Yes", "15.0"],
        [1002, "Biochemistry", 2,    "No",  "12.5"],
        [1003, "Computer Science", 4, "Yes", "18.5"],
        [1004, "English",      2.95, "No",  "12.0"],
        [1005, "Psychology",   3,    "No",  "9.0"],
    ]

    with open("raw_survey_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "major", "GPA", "is_cs_major", "credits_taken"])
        writer.writerows(data)

if __name__ == "__main__":
    make_csv()
    print("Sucess")


import json
def make_json():
    courses = [
        {
            "course_id": "DS2002",
            "section": "001",
            "title": "Data Science Systems",
            "level": 200,
            "instructors": [
                {"name": "Austin Rivera", "role": "Primary"},
                {"name": "Heywood Williams-Tracy", "role": "TA"}
            ]
        },
        {
            "course_id": "DS2004",
            "section": "001",
            "title": "Data Ethics",
            "level": 200,
            "instructors": [
                {"name": "Emanuel Moss, PhD", "role": "Primary"}
            ]
        },
        {
            "course_id": "CHEM4410",
            "section": "001",
            "title": "Biochemistry",
            "level": 400,
            "instructors": [
                {"name": "Linda Columbus", "role": "Primary"}
            ]
        },
        {
            "course_id": "CHEM4320",
            "section": "001",
            "title": "Inorganic Chemistry",
            "level": 400,
            "instructors": [
                {"name": "Charles Machaan", "role": "Primary"}
            ]
        }
    ]
    with open("raw_course_catalog.json", "w") as f:
        json.dump(courses, f, indent=3)
    
if __name__ == "__main__":
     make_json()
     print ("Sucess Json")

import pandas as pd
df = pd.read_csv("raw_survey_data.csv")
df["is_cs_major"] = df["is_cs_major"].replace({"Yes": True, "No": False})
df = df.astype({"GPA": "float64", "credits_taken": "float64"})
df.to_csv("clean_survey_data.csv", index=False)

with open("raw_course_catalog.json", "r") as f:
    data = json.load(f)

df = pd.json_normalize(
    data,
    record_path=['instructors'],
    meta=['course_id', 'title', 'level']
)
df.to_csv("clean_course_catalog.csv", index=False)