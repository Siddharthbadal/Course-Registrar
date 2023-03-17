# Course Registrar Command Line Interface

(project is still in Progress)
**Command line interface for course registrar**. Project allows user to perform various operation using allowed commands.
Course Registrar CLI is built with Python and mysql and also have used typer and rich libraries. 
Typer is a library for building CLI applications while rich is used to create highlighted and colored text and tables 
on the command line.


Files details in the Project: 
    registrar.py: A file for commands. registrar.py has all the function used to create and perform certain commands. 
                These commands are work on different database functions to perform SQL queries.
    database.py: perform the database operation including creating connecting and initializing inbuilt dataset for 
                the registrar.
    ddl.sql: data definition query to create tables inside the database. In mySQL Temp tables are used and Triggers 
            are created to meet certain criteria to enroll in the courses.
    data.txt: inbuilt dataset.



### Commands
help:
```
    python registrar.py --help
```

reset-database:
    ```
        python registrar.py reset-database --with-data / --no-with-data
    ```

add a course:
    ```
        python registrar.py add-courses py50 "Introduction to Python" "Computer Science"
    ```


## All Commands:
    
┌─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ add-courses     Add a course by giving code, course name, and department                                   │
│ add-prereq      Add course prerequisites by giving course name, prereq course name and minimum grade       │
│                 (optional)                                                                                 │
│ add-student     Add a student by giving firstname, lastname, and uniq_id                                   │
│ enroll-student  enroll student by entering student id, course code and year                                │
│ reset-database  Reset the database. and initialize the inbuilt dataset. By default, reset database is      │
│                 performed with inbuilt data. can also use:     --with-data & --no-with-data                │
│ set-grade       set grade in student_course table by entering student, course, grade.                      │
│ show-courses    Show courses by department. Eg:"Computer Science"                                          │
│ show-prereqs    See the prerequisites of a course by entering course code(moniker) eg: cs101               │
│ show-students   Show student name by last name letters. eg: neg.                                           │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────┘



