from flask import Flask, jsonify
from z3 import *
import json

# Initialise Flask app
app = Flask(__name__)

def get_student_info():
    # Write info from json to student info variable in read mode
    with open("testinfo.json", "r") as file:
        student_info = json.load(file)
    return student_info

def get_course_data():
    # Write info from json to courses in read mode
    with open("courses.json", "r") as file:
        courses = json.load(file)
    return courses

@app.route("/data")
def generate_recommendations():
    student_info = get_student_info()
    courses = get_course_data()

    solver = Solver()
    vars = {c: Bool(c) for c in courses}

    # Prerequisite constraints
    for course, data in courses.items():
        for pre in data["prerequisites"]:
            if pre in vars:
                solver.add(Implies(vars[course], vars[pre]))

    # Fix taken courses to True
    for c in student_info["taken"]:
        if c in vars:
            solver.add(vars[c] == True)

    # Categorize courses
    major1_courses = [c for c, data in courses.items() if student_info["firstMajor"] in data.get("majors", [])]
    major2_courses = [c for c, data in courses.items() if student_info["secondMajor"] and student_info["secondMajor"] in data.get("majors", [])]
    minor1_courses = [c for c, data in courses.items() if student_info["firstMinor"] and student_info["firstMinor"] in data.get("minors", [])]
    minor2_courses = [c for c, data in courses.items() if student_info["secondMinor"] and student_info["secondMinor"] in data.get("minors", [])]

    elective_courses = [
        c for c, data in courses.items()
        if student_info["firstMajor"] not in data.get("majors", []) and
           (not student_info["secondMajor"] or student_info["secondMajor"] not in data.get("majors", [])) and
           (not student_info["firstMinor"] or student_info["firstMinor"] not in data.get("minors", [])) and
           (not student_info["secondMinor"] or student_info["secondMinor"] not in data.get("minors", []))
    ]

    # Degree requirements
    if type == "doubleMajor":
        solver.add(Sum([If(vars[c], 1, 0) for c in major1_courses]) >= 8)
        solver.add(Sum([If(vars[c], 1, 0) for c in major2_courses]) >= 8)
    elif type == "majorTwoMinors":
        solver.add(Sum([If(vars[c], 1, 0) for c in major1_courses]) >= 8)
        solver.add(Sum([If(vars[c], 1, 0) for c in minor1_courses]) >= 4)
        solver.add(Sum([If(vars[c], 1, 0) for c in minor2_courses]) >= 4)
    elif type == "majorMinorElectives":
        solver.add(Sum([If(vars[c], 1, 0) for c in major1_courses]) >= 8)
        solver.add(Sum([If(vars[c], 1, 0) for c in minor1_courses]) >= 4)
        solver.add(Sum([If(vars[c], 1, 0) for c in elective_courses]) >= 4)

    # Total course count constraint
    solver.add(Sum([If(vars[c], 1, 0) for c in courses]) <= 24)

    # Generate recommendations
    recommendations = []
    for c in courses:
        if c not in student_info["taken"]:
            test_solver = Solver()
            test_solver.add(solver.assertions())
            test_solver.add(vars[c] == True)
            if test_solver.check() == sat:
                recommendations.append({
                    "code": c,
                    "title": courses[c]["title"]
                })

    return recommendations

# Running app
if __name__ == '__main__':
    app.run(debug=True)