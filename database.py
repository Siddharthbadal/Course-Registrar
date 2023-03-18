import mysql.connector
import time
import typer
from mysql.connector import connect, Error
from dotenv import load_dotenv
from os import environ as env
import data

load_dotenv()

# load .env file to access the variables
def get_connection():
    """
    connecting to mysql server
    """
    connection = None
    try:
        connection = connect(
            user=env.get('user'),
            password=env.get('password'),
            host=env.get('host'),
            port=env.get('port'),
            database=env.get('database'),
        )
        if env.get("MYSQL_VERBOSE") == "YES":
            print("Connected to Mysql...!\n")
            time.sleep(2)

    except Error as e:
        print(f"Error '{e}' occured while attempting to connect to the database")

    return connection


def query_connection(connection, q, data=None, fetch=None, many=False):
    """
    creating connection to the mysql server to perform sql queies
    :param connection: mysql connection
    :param q: sql query
    :return:
    """
    cursor = connection.cursor()
    try:
        if many:
            cursor.executemany(q, data)

        else:
            cursor.execute(q, data)
        if fetch:
            return cursor.fetchall()
        else:
            connection.commit()
            if env.get("MYSQL_VERBOSE") == "YES":

                print(q)
                typer.echo(typer.style("Successful!\n", bg=typer.colors.YELLOW))
                time.sleep(1)
        #
    except (mysql.connector.IntegrityError, mysql.connector.DatabaseError) as e:
        typer.echo(f"\nStatement execution failed\n: {typer.style(e, bg=typer.colors.WHITE, fg=typer.colors.RED)}")
    finally:
        cursor.close()


# database reset
def reset():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            with open('ddl.sql', 'r') as f:
                for result in cursor.execute(f.read(), multi=True):
                    if env.get('MYSQL_VERBOSE') =='YES':
                        pass


def initalize_data():
    """
    Inserting avilable data into the database
    """
    with get_connection() as conn:
        stu_query = "INSERT INTO students (first_name, last_name, uniq_id) VALUES(%s, %s, %s);"
        stu_data = data.students
        query_connection(conn,stu_query, stu_data, many = True)

        courses_query = "INSERT INTO courses (moniker, name, department) VALUES(%s, %s, %s);"
        courses_data = data.courses
        query_connection(conn, courses_query, courses_data, many = True)

        prereq_query = "INSERT INTO prerequisites (course, prereq, min_grade) VALUES(%s, %s, %s);"
        prereq_data = data.prerequisites
        query_connection(conn, prereq_query, prereq_data, many = True)





def add_a_student(first_name: str, last_name: str, uniq_id: str):
    """
    adding a student
    :param first_name:
    :param last_name:
    :param uniq_id:
    """
    with get_connection() as conn:
        query= "INSERT INTO STUDENTS (first_name, last_name, uniq_id) VALUES (%s, %s, %s);"
        data = (first_name, last_name, uniq_id)
        query_connection(conn, query, data)


def add_a_course(moniker: str, name: str, department: str):
    """
    Add a course
    :param moniker:
    :param name:
    :param department:
    """
    with get_connection() as conn:
            query = "INSERT INTO courses(moniker, name, department) VALUES (%s, %s, %s);"
            data = (moniker, name, department)
            query_connection(conn, query, data)


def add_a_prerequisites(course, prereq, min_grade=50):
    """
    Add a prerequisite for course
    :param course:
    :param prereq:
    :param min_grade: 50, defualt
    """
    with get_connection() as conn:
            query = "INSERT INTO prerequisites(course, prereq, min_grade) VALUES (%s, %s, %s);"
            data = (course, prereq, min_grade)
            query_connection(conn, query, data)



def show_course_prerequisites(course):
    """
    Show prerequisites for the entered course
    :param course:
    :return:
    """
    with get_connection() as conn:
        query = "SELECT course, prereq, min_grade FROM prerequisites WHERE course = %s"
        data = (course,)

        return query_connection(conn, query, data, fetch=True)



def show_students_by(last_name):
    """
    Query to fetch student by last name letters
    :param last_name:
    :return:
    """
    with get_connection() as conn:
        query = "SELECT first_name, last_name, uniq_id FROM students where last_name LIKE %s;"
        data = ('%' + last_name + '%',)

        return query_connection(conn, query, data, fetch=True)


def show_courses_by(department):
    """
    Query to fetch courses by department
    :param department:
    :return:
    """
    with get_connection() as conn:
        query = "SELECT moniker, name, department FROM courses where department = %s;"
        data = (department ,)

        return query_connection(conn, query, data, fetch=True)


def enroll(student, course, year):
    with get_connection() as conn:
        query = "INSERT INTO student_course (student, course, year) VALUES (%s, %s, %s);"
        data = (student, course, year)
        query_connection(conn, query, data=data)


def unenroll(student, course, year):
    with get_connection() as conn:
        query = "DELETE FROM student_course WHERE student = %s AND course = %s AND year =%s;"
        data = (student, course, year)
        query_connection(conn, query, data)


def set_student_grade(student, course, grade, year):
    with get_connection() as conn:
        query = "UPDATE student_course SET grade =%s WHERE student = %s AND course = %s AND year =%s"
        data = (grade, student, course, year)
        query_connection(conn, query, data=data)












