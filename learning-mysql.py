from mysql.connector import connect
from urllib.parse import urlparse
# connection_url = "mysql://-hcontainers-us-west-55.railway.app -uroot -pQ4R1klE2HGKxbXbluiXW --port 7523 --protocol=TCP railway"
connection_url = "mysql://root:Q4R1klE2HGKxbXbluiXW@containers-us-west-55.railway.app:7523/railway"

'''
# railway database connection
url = urlparse(connection_url)
print(url)

connection = connect(
    host=url.hostname,
    port=url.port,
    user=url.username,
    password=url.password,
    database=url.path[1:]
)
print(connection.is_connected())
connection.close()
curr = connection.cursor()

curr.execute("""
    DROP TABLE IF EXISTS users;
    CREATE TABLE users(
        id INTEGER PRIMARY KEY AUTO_INCREMENT,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL
    )
""")
curr.execute("""
    INSERT INTO users (username, password) 
    VALUES ("rolf","1234"), ("anna","1974");
""")
connection.commit()

'''

# mysql workbench

get_db_connection = lambda: connect(
    host="127.0.0.1",
    port="3306",
    user='root',
    password="admin.2022",
    database='learnmysqlpython',
    autocommit=True
)
conn = get_db_connection()
print(conn.is_connected())
curr = conn.cursor()

# curr.execute("""
#     DROP TABLE IF EXISTS users;
#     CREATE TABLE users(
#         id INTEGER PRIMARY KEY AUTO_INCREMENT,
#         username VARCHAR(50) NOT NULL,
#         password VARCHAR(50) NOT NULL
#     )
# """)
# with get_db_connection() as conn:
#     with conn.cursor() as curr:
#         curr.execute("""
#             INSERT INTO users (username, password)
#             VALUES ("kanet","7894"), ("Pierye","maine");
#         """)
#
query = "INSERT INTO users(username, password) VALUES (%s, %s)"

users = [
    ("bob", "1234"),
    ("dob", '4567')
]
user = ('lukka', '0720')

# with get_db_connection() as conn:
#     with conn.cursor() as curr:
#         curr.execute(query, user)

# fet data
curr.execute("SELECT * FROM users;")

users = curr.fetchall()
# print(users)



# with get_db_connection() as conn:
#     with conn.cursor() as curr:
#         curr.execute("SELECT * FROM users ORDER BY RAND() LIMIT 1;")
#         print(curr.fetchone())



# buffered cursor
# with get_db_connection() as conn:
#     with conn.cursor(buffered=True ) as curr:
#         curr.execute("SELECT * FROM users ORDER BY RAND() LIMIT 4;")
#         print(curr.fetchmany())
#



# dictionary cursor

with get_db_connection() as conn:
    with conn.cursor(dictionary=True) as curr:
        curr.execute("SELECT * FROM users ORDER BY RAND() LIMIT 4;")
        for user in curr.fetchall():
            print(user['username'] + ": " + user.get('password'))

print("--------")
with get_db_connection() as conn:
    with conn.cursor(named_tuple=True) as curr:
        curr.execute("SELECT * FROM users ORDER BY RAND() LIMIT 1;")
        for user in curr.fetchall():
            print(user.username + ": " + user.password)
            print(type(user))
            print(issubclass(type(user), tuple))

















