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
    # Get info from external input.
    student_info = get_student_info()
    courses = get_course_data()

    # Initialise Z3 solver.
    solver = Solver()

    course_taken = {c: Bool(c) for c in courses} # If true, the course has already been taken.'

    # Initialise array for semester taken per course.
    # Y1 S1 = 0, Y1 S2 = 1, Y2, S1 = 3 and so on...
    semester_taken = {c: Int(f"semester_{c}") for c in courses } # The semester that course will be taken.

    # Initialise semester taken to be -1 (not taken).
    for c in courses: 
        solver.add(Or(
            semester_taken[c] == -1,
            And (semester_taken[c] >= 0, semester_taken[c] < 6)
        ))

    # Constraint: The prerequisite must be taken before the course.
    for course, data in courses.items():
        for pre in data["prerequisites"]:
            if pre in course_taken:
                solver.add(Implies(
                    semester_taken[course] != -1, 
                    And(
                        semester_taken[pre] != -1,  
                        semester_taken[pre] < semester_taken[course]  
                    )
                ))

    # Fix taken courses to True
    for c in student_info["taken"]:
        if c in course_taken:
            solver.add(course_taken[c] == True)

    # Categorize courses
    compulsory_courses = [c for c, data in courses.items() if "Compulsory" in data.get("majors", [])]
    major1_courses = [c for c, data in courses.items() if student_info["firstMajor"] in data.get("majors", [])]
    major2_courses = [c for c, data in courses.items() if student_info["secondMajor"] in data.get("majors", [])]
    minor1_courses = [c for c, data in courses.items() if student_info["firstMinor"] in data.get("minors", [])]
    minor2_courses = [c for c, data in courses.items() if student_info["secondMinor"] in data.get("minors", [])]

    # elective_courses = [
    #     c for c, data in courses.items()
    #     if student_info["firstMajor"] not in data.get("majors", []) and
    #        (not student_info["secondMajor"] or student_info["secondMajor"] not in data.get("majors", [])) and
    #        (not student_info["firstMinor"] or student_info["firstMinor"] not in data.get("minors", [])) and
    #        (not student_info["secondMinor"] or student_info["secondMinor"] not in data.get("minors", []))
    # ] 

    # Degree requirements
    solver.add(Sum([If(course_taken[c], 1, 0) for c in compulsory_courses]) == 8)
    if type == "doubleMajor":
        solver.add(Sum([If(course_taken[c], 1, 0) for c in major1_courses]) == 8)
        solver.add(Sum([If(course_taken[c], 1, 0) for c in major2_courses]) == 8)
    elif type == "majorTwoMinors":
        # Constraint: 8 courses from major
        solver.add(Sum([If(course_taken[c], 1, 0) for c in major1_courses]) == 8)
        # Constraint: 1 L5 course, depending on major.
        if (student_info["firstMinor"] == "Networks and Cybersecurity" or student_info["secondMinor"] == "Networks and Cybersecurity"):
            solver.add(PbEq([(c == "COMP504", 1)]))
        if (student_info["firstMinor"] == "Software Development" or student_info["secondMinor"] == "Software Development"):
            solver.add(PbEq([(c == "COMP503", 1)]))
        if (student_info["firstMinor"] == "Data Science" or student_info["secondMinor"] == "Data Science"):
            solver.add(PbEq([(c == "COMP517", 1)]))
        if (student_info["firstMinor"] == "Digital Services" or student_info["secondMinor"] == "Digital Services"):
            solver.add(PbEq([(c == "INFS502", 1)])) 
        if (student_info["firstMinor"] == "Computer Science" or student_info["secondMinor"] == "Computer Science"):
            solver.add(PbEq([(c == "COMP503", 1)])) 
        if (student_info["firstMinor"] == "Artificial Intelligence" or student_info["secondMinor"] == "Artificial Intelligence"):
            solver.add(PbEq([(c == "COMP517", 1)])) 
        # Constraints: 
        # Artificial Intelligence: 15 points L6 course, 30 points L7 courses
        # Everything else: 60 points L6 courses, 15 points L7 course
        if (student_info["firstMinor"] != "Artificial Intelligence"):
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor1_courses]) == 2)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor1_courses]) == 1)
        else:
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor1_courses]) == 1)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor1_courses]) == 2)
        if (student_info["secondMinor"] != "Artificial Intelligence"):
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor2_courses]) == 2)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor2_courses]) == 1)
        else:
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor2_courses]) == 1)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor2_courses]) == 2)
        
        # solver.add(Sum([If(course_taken[c], 1, 0) for c in minor1_courses]) >= 4)
        # solver.add(Sum([If(course_taken[c], 1, 0) for c in minor2_courses]) >= 4)
    elif type == "majorMinorElectives":
        # Constraint: 8 courses from major
        solver.add(Sum([If(course_taken[c], 1, 0) for c in major1_courses]) == 8)
        # Constraint: 1 L5 course, depending on major.
        if (student_info["firstMinor"] == "Networks and Cybersecurity"):
            solver.add(PbEq([(c == "COMP504", 1)]))
        if (student_info["firstMinor"] == "Software Development"):
            solver.add(PbEq([(c == "COMP503", 1)]))
        if (student_info["firstMinor"] == "Data Science"):
            solver.add(PbEq([(c == "COMP517", 1)]))
        if (student_info["firstMinor"] == "Digital Services"):
            solver.add(PbEq([(c == "INFS502", 1)])) 
        if (student_info["firstMinor"] == "Computer Science"):
            solver.add(PbEq([(c == "COMP503", 1)])) 
        if (student_info["firstMinor"] == "Artificial Intelligence"):
            solver.add(PbEq([(c == "COMP517", 1)])) 
        # Constraints: 
        # Artificial Intelligence: 15 points L6 course, 30 points L7 courses
        # Everything else: 60 points L6 courses, 15 points L7 course
        if (student_info["firstMinor"] != "Artificial Intelligence"):
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor1_courses]) == 2)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor1_courses]) == 1)
        else:
            solver.add(Sum([If(course_taken[c] and data.get("level") == "6", 1, 0) for c in minor1_courses]) == 1)
            solver.add(Sum([If(course_taken[c] and data.get("level") == "7", 1, 0) for c in minor1_courses]) == 2)
        # solver.add(Sum([If(course_taken[c], 1, 0) for c in elective_courses]) >= 4)

    # Total course count constraint - excluding electives
    solver.add(Sum([If(course_taken[c], 1, 0) for c in courses]) <= 24)

    # Create eligible courses then sort by semester
    # eligible_courses = [
    #     c for c in courses
    #     if c not in student_info["taken"] 
    #     and course_taken[c]
    #     and c in (major1_courses or major2_courses or minor1_courses or minor2_courses)
    # ]

    # Generate recommendations
    recommendations = []
    for c in courses:
        if c not in student_info["taken"] and (c in compulsory_courses or c in major1_courses or c in major2_courses or c in minor1_courses or c in minor2_courses):
            test_solver = Solver()
            test_solver.add(solver.assertions())
            test_solver.add(course_taken[c] == True)
            if test_solver.check() == sat:
                courseType = "";
                if (c in compulsory_courses):
                    courseType = "compulsory"
                elif (c in major1_courses):
                    courseType = "major1"
                elif (c in major2_courses): 
                    courseType = "major2" 
                elif (c in minor1_courses):
                    courseType = "minor1" 
                elif (c in minor2_courses): 
                    courseType = "minor2"
                recommendations.append({
                    "code": c,
                    "title": courses[c]["title"],
                    "type": courseType
                })

    return recommendations

# Running app
if __name__ == '__main__':
    app.run(debug=True)