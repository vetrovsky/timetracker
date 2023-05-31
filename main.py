# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import sqlite3
import sys
from datetime import datetime
from _sqlite3 import Error

def app_folder(prog: str) -> str:
    def createFolder(directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            raise

    if sys.platform == "win32":
        folder = os.path.join(os.path.expanduser("~"), "AppData", "Local", prog)
        createFolder(folder)
        return folder
    else:
        folder = os.path.join(os.path.expanduser("~"), "." + prog)
        createFolder(folder)
        return folder

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

# create a function that returns a list of employees with the given last name
def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last_name=:last", {'last': lastname})
    return c.fetchall()

#create a function that returns a list of all employees
def get_all_emps():
    c.execute("SELECT * FROM employees")
    return c.fetchall()

#create a function that returns a list of all test
def get_all_works():
    c.execute("SELECT * FROM works")
    return c.fetchall()

def command_help():
    print("help:")
    print("python main.py help")
    print("python main.py start project_name")
    print("python main.py stop")
    print("python main.py list")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # save first parameter to var command
    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = "help"

   # set data folder
    folder = app_folder("timetracker")

    # set database file
    db_file = os.path.join(folder, 'data.db')
    print(f"Open file {db_file} in {folder}")
   # create a database connection
    create_connection(db_file)


    # create or open sqlite database test
    conn = sqlite3.connect(db_file)

    # create a cursor
    c = conn.cursor()

    # create sqlite table works if not exists
    c.execute("""CREATE TABLE IF NOT EXISTS works (
                id integer primary key autoincrement,
                project text,
                timestamp text
                )""")

    if command == "help":
        command_help()
    elif command == "list":
        print(get_all_works())
    elif command == "start":
        if len(sys.argv) > 2:
            print("please enter a project name")
            command_help()
            exit()
        else:
            project = sys.argv[2]

        # insert data into table
        now = datetime.now()
        #convert now to string
        now1 = str(now)
        c.execute("INSERT INTO works (project, timestamp) VALUES (:project, :now)", {'project': project, 'now': now1});
        conn.commit()
        # call the function and print the results
        print("start project: " + project + " at " + now1)
    elif command == "stop":
        # insert data into table
        now = datetime.now()
        #convert now to string
        now1 = str(now)
        c.execute("INSERT INTO works (project, timestamp) VALUES (:project, :now)", {'project': "stop", 'now': now1});
        conn.commit()
        # call the function and print the results
        print("stop project at " + now1)

    # close the connection
    conn.close()

