import typer
import time
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
from os import environ as env
from datetime import datetime
from database import reset, add_a_student, add_a_course, add_a_prerequisites, initalize_data,\
    show_course_prerequisites, show_students_by, show_courses_by, enroll, set_student_grade, unenroll,\
    show_courses_a_student_enrolled_in, get_transcript_for, most_enrolled_students_courses, top_performing_students


app = typer.Typer()
console = Console()
min_passing_grade = 50

def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")
    for row in data:
        table.add_row(*map(str, row))
    console.print(table, justify="center")


def print_message(message: str):
    text = Text(message)
    text.stylize("bold orange3", 0)
    console.print(text)


@app.command()
def add_student(first_name: str, last_name: str, uniq_id: str):
    """
    Add a student by giving firstname, lastname, and uniq_id

    :param first_name:
    :param last_name:
    :param uniq_id:
    """
    console.print("Adding a student.. .")
    add_a_student(first_name, last_name, uniq_id)


@app.command()
def add_courses(moniker: str, name: str, department: str):
    """
    Add a course by giving code, course name, and department

    """
    console.print("Adding courses.. .")
    add_a_course(moniker, name, department)


@app.command()
def add_prereq(course: str, prereq: str, min_grade: int = typer.Argument(min_passing_grade)):
    """
    Add course prerequisites by giving course name, prereq course name and minimum grade (optional)

    :param course:
    :param prereq:
    :param min_grade:
    :return:
    """
    add_a_prerequisites(course, prereq, min_grade)
    console.print("\nPrerequisite added!")

#  SHOW Commands

@app.command()
def show_prereqs(course: str):
    """
    See the prerequisites of a course by entering course code(moniker) eg: cs101

    :param course:

    """
    pretty_table(["Course","Prerequisites","Minimum Grade"],data=show_course_prerequisites(course), in_color="red")

@app.command()
def show_students(last_name: str):
    """
    Show student name by last name letters. eg: neg.

    :param last_name:

    """

    data = show_students_by(last_name)
    if len(data):
        pretty_table(['First Name', 'Last Name', 'Unique ID'], data=data, in_color='blue')
    else:
        console.print("\nNo student found!")


@app.command()
def show_courses(department: str):
    """
    Show courses by department. Eg:"Computer Science"

    :param department:

    """
    data = show_courses_by(department)
    if len(data):
        pretty_table(["Code", "name", "Department"], data=data, in_color='green_yellow')
    else:
        console.print(f"\nNo courses found under {department}!")


@app.command()
def enroll_student(student: str, course: str, year: int = typer.Argument(datetime.now().year)):
    """
    enroll student by entering student id, course code and year

    :param student:
    :param course:
    :param year:

    """

    enroll(student, course, year)
    console.print(f"\n{student} current courses:")
    student_current_courses(student)
    # print_message(message=f"\n{student} enrolled in course {course}!!!")




@app.command()
def unenroll_student(student: str, course: str, year: int = datetime.now().year):
    """
    Un-enroll a student from a course by entering student id and course code

    :param student:
    :param course:
    :param year:

    """
    unenroll(student, course, year)
    console.print(f"\n{student} un-enrolled from course {course}!", style='bold red')
    console.print(f"\n{student} current courses:", justify='center')
    student_current_courses(student)

@app.command()
def set_grade(student: str, course: str, grade: int, year:int = datetime.now().year):
    """
    set grade in student_course table by entering student, course, grade.

    :param student:
    :param course:
    :param grade:
    :param year: default
    """
    set_student_grade(student, course, grade, year)
    console.print(f"\nGrade Updated for{course}!", style="bold yellow")



@app.command()
def student_current_courses(student: str):
    """
    Show the all courses a student is enrolled in by giving student id

    :param student:

    """
    data = show_courses_a_student_enrolled_in(student)
    if len(data):
        pretty_table(['Course', 'Year'], data=data, in_color="blue")
    else:
        console.print(f"\nNo courses for {student}. Please enroll!", style="bold blue")


@app.command()
def student_transcript(student: str):
    """
    get details of a student completed course by giving student name
    """
    data = get_transcript_for(student)
    if len(data):
        print_message(message=f"\n{student} completed courses!")
        pretty_table(['Course', 'Year', 'Grade', "Grade Level"], data=data, in_color="green")
        console.print(f"Average GPA: {sum([row[2] for row in data]) / len(data):.2f}", style="bold", justify='center')
    else:
        console.print(f"\n{student} yet to complete a course!")



@app.command()
def most_enrolled_courses(n: int = 10):
    """
    get the most enrolled courses by giving a number (optional) / --n=1
    :param n:  --n=1 (optional)

    """
    data = most_enrolled_students_courses(n)
    pretty_table(["Course", "Name", "Enrollemnt"], data=data, in_color="green")


@app.command()
def top_performers(n: int=5):
    """
    Find the top performers
    :param n: total number of students (optional)

    """
    data = top_performing_students(n)
    pretty_table(['UniqID', 'First_name', 'Last_name', 'Courses', 'GPA'], data=data, in_color="yellow")



@app.command()
def reset_database(verbose: bool=False, with_data: bool = True):
    """
    Reset the database. and initialize the inbuilt dataset.
    By default, reset database is performed with inbuilt data. can also use:
        --with-data & --no-with-data


    """
    answer = input("This will create a new database. Do you want to continue? (y/n): ")

    if verbose:
        env['MYSQL_VERBOSE'] = "YES"

    if answer.strip().lower() == 'y':
        reset()
        time.sleep(2)
        typer.echo("\nDatabase reset done successfully!")

        if with_data:
            time.sleep(2)
            initalize_data()
            typer.echo("All tables created. Data initialize successfully!")

    else:
        typer.echo("\nDatabase reset aborted.")


if __name__ == "__main__":
    app()
