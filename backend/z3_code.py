from z3 import *

def generate_recommendations(courses, taken, type, firstMajor, secondMajor=None, firstMinor=None, secondMinor=None):
    solver = Solver()
    vars = {c: Bool(c) for c in courses}

    # Prerequisite constraints
    for course, data in courses.items():
        for pre in data["prerequisites"]:
            if pre in vars:
                solver.add(Implies(vars[course], vars[pre]))

    # Fix taken courses to True
    for c in taken:
        if c in vars:
            solver.add(vars[c] == True)

    # Categorize courses
    major1_courses = [c for c, data in courses.items() if firstMajor in data.get("majors", [])]
    major2_courses = [c for c, data in courses.items() if secondMajor and secondMajor in data.get("majors", [])]
    minor1_courses = [c for c, data in courses.items() if firstMinor and firstMinor in data.get("minors", [])]
    minor2_courses = [c for c, data in courses.items() if secondMinor and secondMinor in data.get("minors", [])]

    elective_courses = [
        c for c, data in courses.items()
        if firstMajor not in data.get("majors", []) and
           (not secondMajor or secondMajor not in data.get("majors", [])) and
           (not firstMinor or firstMinor not in data.get("minors", [])) and
           (not secondMinor or secondMinor not in data.get("minors", []))
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
        if c not in taken:
            test_solver = Solver()
            test_solver.add(solver.assertions())
            test_solver.add(vars[c] == True)
            if test_solver.check() == sat:
                recommendations.append({
                    "code": c,
                    "title": courses[c]["title"]
                })

    return recommendations