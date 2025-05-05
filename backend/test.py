# Import Flask and Z3 modules
from flask import Flask
from z3 import *

# Initialise Flask app
app = Flask(__name__)

# Define course “slots” as variables

year1_S1_course1 = String('year1_S1_course1')
year1_S1_course2 = String('year1_S1_course2')
year1_S1_course3 = String('year1_S1_course3')
year1_S1_course4 = String('year1_S1_course4')

year1_S2_course1 = String('year1_S2_course1')
year1_S2_course2 = String('year1_S2_course2')
year1_S2_course3 = String('year1_S2_course3')
year1_S2_course4 = String('year1_S2_course4')

year1_S1 = [year1_S1_course1, year1_S1_course2, year1_S1_course3, year1_S1_course4]
year1_S2 = [year1_S2_course1, year1_S2_course2, year1_S2_course3, year1_S2_course4]
year1_full = [year1_S1_course1, year1_S1_course2, year1_S1_course3, year1_S1_course4, 
              year1_S2_course1, year1_S2_course2, year1_S2_course3, year1_S2_course4]

year2_S1_course1 = String('year2_S1_course1')
year2_S1_course2 = String('year2_S1_course2')
year2_S1_course3 = String('year2_S1_course3')
year2_S1_course4 = String('year2_S1_course4')

year2_S2_course1 = String('year2_S2_course1')
year2_S2_course2 = String('year2_S2_course2')
year2_S2_course3 = String('year2_S2_course3')
year2_S2_course4 = String('year2_S2_course4')

year2_S1 = [year2_S1_course1, year2_S1_course2, year2_S1_course3, year2_S1_course4]
year2_S2 = [year2_S2_course1, year2_S2_course2, year2_S2_course3, year2_S2_course4]
year2_full = [year2_S1_course1, year2_S1_course2, year2_S1_course3, year2_S1_course4, 
              year2_S2_course1, year2_S2_course2, year2_S2_course3, year2_S2_course4]

year2_progress = [year1_S1_course1, year1_S1_course2, year1_S1_course3, year1_S1_course4, 
                  year1_S2_course1, year1_S2_course2, year1_S2_course3, year1_S2_course4, 
                  year2_S1_course1, year2_S1_course2, year2_S1_course3, year2_S1_course4, 
                  year2_S2_course1, year2_S2_course2, year2_S2_course3, year2_S2_course4]

year3_S1_course1 = String('year3_S1_course1')
year3_S1_course2 = String('year3_S1_course2')
year3_S1_course3 = String('year3_S1_course3')
year3_S1_course4 = String('year3_S1_course4')

year3_S2_course1 = String('year3_S2_course1')
year3_S2_course2 = String('year3_S2_course2')
year3_S2_course3 = String('year3_S2_course3')
year3_S2_course4 = String('year3_S2_course4')

year3_S1 = [year3_S1_course1, year3_S1_course2, year3_S1_course3, year3_S1_course4]
year3_S2 = [year3_S2_course1, year3_S2_course2, year3_S2_course3, year3_S2_course4]
year3_full = [year3_S1_course1, year3_S1_course2, year3_S1_course3, year3_S1_course4,
              year3_S2_course1, year3_S2_course2, year3_S2_course3, year3_S2_course4]

year3_progress = [year1_S1_course1, year1_S1_course2, year1_S1_course3, year1_S1_course4, 
                  year1_S2_course1, year1_S2_course2, year1_S2_course3, year1_S2_course4, 
                  year2_S1_course1, year2_S1_course2, year2_S1_course3, year2_S1_course4, 
                  year2_S2_course1, year2_S2_course2, year2_S2_course3, year2_S2_course4,
                  year3_S1_course1, year3_S1_course2, year3_S1_course3, year3_S1_course4,
                  year3_S2_course1, year3_S2_course2, year3_S2_course3, year3_S2_course4]

# Initialise Z3 Solver
s = Solver()

# Add values to these course “slots” as constraints depending on prerequisites and majors/minors

s.add(PbEq([(c == "COMP500", 1) for c in year1_S1], 1))
s.add(PbEq([(c == "MATH503", 1) for c in year1_S1], 1))
s.add(PbEq([(c == "COMP501", 1) for c in year1_full], 1))
s.add(PbEq([(c == "COMP507", 1) for c in year1_full], 1))
s.add(PbEq([(c == "COMP508", 1) for c in year1_full], 1))
s.add(PbEq([(c == "DIGD507", 1) for c in year1_full], 1))

## SOFTWARE DEVELOPMENT MAJOR ##
s.add(PbEq([(c == "COMP503", 1) for c in year1_full], 1)) 
s.add(Implies(Or(Or([c == "COMP503" for c in year2_progress]), Or([c == "ENSE502" for c in year2_progress]), Or([c == "ENSE602" for c in year2_progress])), PbEq([(c == "COMP610", 1) for c in year2_full], 1)))
s.add(Implies(Or(Or([c == "COMP603" for c in year2_progress]), Or([c == "COMP610" for c in year2_progress])), PbEq([(c == "COMP602", 1) for c in year2_full], 1)))
s.add(Implies(Or(Or([c == "COMP503" for c in year2_progress]), Or([c == "COMP610" for c in year2_progress]), Or([c == "ENSE502" for c in year2_progress])), PbEq([(c == "COMP603", 1) for c in year2_full], 1)))
# COMP604 and COMP611 not applied - depends on decision of user.
s.add(Implies(Or(Or([c == "COMP603" for c in year3_progress]), Or([c == "ENSE600" for c in year3_progress])), PbEq([(c == "COMP721", 1) for c in year3_S1], 1)))
s.add(PbEq([(c == "COMP719", 1) for c in year3_S1], 1))
s.add(Implies(Or(Or([c == "COMP603" for c in year3_progress]), Or([c == "COMP610" for c in year3_progress]), Or([c == "ENSE600" for c in year3_progress])), PbEq([(c == "ENSE701", 1) for c in year3_full], 1)))

## R&D PROJECT COURSES ##
s.add(Implies(Or(Or([c == "COMP500" for c in year3_progress]), 
                 Or([c == "COMP501" for c in year3_progress]), 
                 Or([c == "COMP507" for c in year3_progress]),
                 Or([c == "COMP508" for c in year3_progress]),
                 Or([c == "DIGD507" for c in year3_progress]),
                 Or([c == "MATH503" for c in year3_progress])
                 # still need to implement major-specific courses
                 ), PbEq([(c == "COMP702", 1) for c in year3_full], 1)))
s.add(Implies(Or([c == "COMP702" for c in year3_S1]), PbEq([(c == "COMP703", 1) for c in year3_S2], 1)))

# If there is a satisfiable solution, return the result as an API
@app.route("/data")
def data():
    if s.check()==sat:
        m = s.model()
        return {
            "Year1_S1" : [m[year1_S1_course1].as_string(), m[year1_S1_course2].as_string(), m[year1_S1_course3].as_string(), m[year1_S1_course4].as_string()],
            "Year1_S2" : [m[year1_S2_course1].as_string(), m[year1_S2_course2].as_string(), m[year1_S2_course3].as_string(), m[year1_S2_course4].as_string()],
            "Year2_S1" : [m[year2_S1_course1].as_string(), m[year2_S1_course2].as_string(), m[year2_S1_course3].as_string(), m[year2_S1_course4].as_string()],
            "Year2_S2" : [m[year2_S2_course1].as_string(), m[year2_S2_course2].as_string(), m[year2_S2_course3].as_string(), m[year2_S2_course4].as_string()],
            "Year3_S1" : [m[year3_S1_course1].as_string(), m[year3_S1_course2].as_string(), m[year3_S1_course3].as_string(), m[year3_S1_course4].as_string()],
            "Year3_S2" : [m[year3_S2_course1].as_string(), m[year3_S2_course2].as_string(), m[year3_S2_course3].as_string(), m[year3_S2_course4].as_string()]
        }
    else:
        return s.check()

# Running app
if __name__ == '__main__':
    app.run(debug=True)