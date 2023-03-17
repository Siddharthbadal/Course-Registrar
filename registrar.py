import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text
from datetime import datetime
from database import reset, add_a_student, add_a_course, add_a_prerequisites, initalize_data,\
    show_course_prerequisites, show_students_by, show_courses_by, enroll, set_student_grade


app = typer.Typer()
console = Console()
min_passing_grade = 50

def pretty_table(with_headers, data, in_color):
    table = Table(*with_headers, show_header=True, header_style=f"bold {in_color}")
    for row in data:
        table.add_row(*map(str, row))
    console.print(table)


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
def add_prereq(course: str, prereq: str, min_grade: int = min_passing_grade):
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
    :return:
    """
    pretty_table(["Course","Prerequisites","Minimum Grade"],data=show_course_prerequisites(course), in_color="red")

@app.command()
def show_students(last_name: str):
    """
    Show student name by last name letters. eg: neg.

    :param last_name:
    :return:
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
    :return:
    """
    data = show_courses_by(department)
    if len(data):
        pretty_table(["Code", "name", "Department"], data=data, in_color='green_yellow')
    else:
        console.print(f"\nNo courses found under {department}!")


@app.command()
def enroll_student(student: str, course: str, year: int = datetime.now().year):
    """
    enroll student by entering student id, course code and year

    :param student:
    :param course:
    :param year:
    :return:
    """
    enroll(student, course, year)
    print_message(message=f"\n{student} enrolled in course {course}!!!")


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
    print_message(message="\nGrade Updated!")







@app.command()
def reset_database(with_data: bool = True):
    """
    Reset the database. and initialize the inbuilt dataset.
    By default, reset database is performed with inbuilt data. can also use:
        --with-data & --no-with-data


    """
    answer = input("This will create a new database. Do you want to continue? (y/n): ")

    if answer.strip().lower() == 'y':
        reset()
        typer.echo("\nDatabase reset done successfully!")

        if with_data:
            initalize_data()
            typer.echo("Data initialize successfully!")

    else:
        typer.echo("\nDatabase reset aborted.")


if __name__ == "__main__":
    app()
