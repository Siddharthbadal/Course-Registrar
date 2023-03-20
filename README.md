# Course Registrar Command Line Interface


**Command line interface for Course Registrar** is an interface built with python and mysql where users can manage 
their students and courses data. Users can perform operations like create, read, update, and delete on data.
users start with setting up a database either by  initializing the inbuilt dataset or can add his/her data.


Course Registrar Command line interface is built with **Python and mysql** and also have used 
typer and rich libraries. 
Typer is a library for building CLI applications while rich is used to create highlighted and colored text and tables 
on the command line.


Other Libraries used:
    - Typer
    - Rich
    - MySQL Connector
    
    
Few Operations to be performed:

    - Add a student
    - Add a course and course prerequisite
    - Enroll and Un-enroll students
    - Set grades to mark completed
    - View top students and courses
    - Get a student transcript 

    
    
Files details in the Project: 

    registrar.py: A file for commands. registrar.py has all the function used to create and perform certain commands. 
                These commands work on different database functions to perform SQL queries.
    
    database.py: perform the database operation including creating connection with mysql server
                and initializing inbuilt dataset for the registrar and creating all tables and triggers. 
    
    ddl.sql: data definition query to create tables inside the database. In mySQL Temp tables are used and Triggers 
            are created to meet certain criteria to enroll in the courses.
    
    data.txt: inbuilt dataset.




### Commands
To see all commnads:
```
    python registrar.py --help
```

reset-database command:
```
    python registrar.py reset-database --verbose --with-data / --no-with-data
```

add a course:
```
        python registrar.py add-courses py50 "Introduction to Python" "Computer Science"
```


## All Commands:
| Command      | Details                                                  |
|--------------|----------------------------------------------------------|

| `reset-database`      |   Reset the database. and initialize the inbuilt dataset. By default, reset database is 
                            performed with inbuilt data. 
                            can also use:     
                                    --with-data OR --no-with-data
                                    --verbose (to see the execution process)  |
                                

| `add-courses`         |   Add a course by giving code, course name, and department |  

 | `add-prereq`         |   Add course prerequisites by giving course name, prereq course name and 
                            minimum grade (optional)    |     

 | `add-student`        |   Add a student by giving firstname, lastname, and uniq_id |      

 | `enroll-student`     |   enroll student by entering student id, course code and year |

 | `set-grade`          |   set grade in student_course table by entering student, course, grade.     |

 | `show-courses`       |   Show courses by department. Eg:"Computer Science" |                      

 | `show-prereqs`       |   See the prerequisites of a course by entering course code(moniker) eg: cs101 |

 | `show-students`      |   Show student name by last name letters. eg: neg.  | 

 | `unenroll-student`   |   Un-enroll a student from a course by entering student id and course code   │

 | `student-transcript` |   get details of a student completed course by giving student name |

 | `top-performers`     |   Find the top performers |

 |  `most-enrolled-courses` |   get the most enrolled courses by giving a number (optional)|
                          



## Applied Constraints on data and operations:
    - for courses with prerequisites would display message if prerequisites aren't met.
    - there are two kind of prerequisites. 1. course 2. grades
    - both prerequisites must match.
    - once grades are assigned, courses don't show up in the student list. as It is completed now.
    - course code and student ID are unique key constraint. will display error on repetition. 



Screenshots:

![img](https://github.com/Siddharthbadal/Course-Registrar/blob/main/images/commands.png)

![img](https://github.com/Siddharthbadal/Course-Registrar/blob/main/images/first.png)

![img](https://github.com/Siddharthbadal/Course-Registrar/blob/main/images/second.png)
