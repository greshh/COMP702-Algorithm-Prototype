import React, { useState, useEffect } from "react";

function App() {
    const [courses, setCourses] = useState({
        year1_S1 : ["", "", "", ""],
        year1_S2 : ["", "", "", ""],
        year2_S1 : ["", "", "", ""],
        year2_S2 : ["", "", "", ""],
        year3_S1 : ["", "", "", ""],
        year3_S2 : ["", "", "", ""],
    });

    useEffect(() => {
        fetch("/data").then((res) =>
            res.json().then((courses) => {
                setCourses({
                  year1_S1: courses.Year1_S1,
                  year1_S2: courses.Year1_S2,
                  year2_S1: courses.Year2_S1,
                  year2_S2: courses.Year2_S2,
                  year3_S1: courses.Year3_S1,
                  year3_S2: courses.Year3_S2,
                });
            })
        );
    }, []);

    return (
      <>
        <h1>BCIS Course Planner</h1>
        <h2>2025 - Semester 1</h2>
        {courses.year1_S1.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
        <h2>2025 - Semester 2</h2>
        {courses.year1_S2.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
        <h2>2026 - Semester 1</h2>
        {courses.year2_S1.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
        <h2>2026 - Semester 2</h2>
        {courses.year2_S2.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
        <h2>2027 - Semester 1</h2>
        {courses.year3_S1.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
        <h2>2027 - Semester 2</h2>
        {courses.year3_S2.map((course, index) => (
          <p key={index}>{course}</p>
        ))}
      </>
    );
}

export default App;
