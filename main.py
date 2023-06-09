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
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


#create a function that returns not finished work
def get_open_project():
    c.execute("SELECT * FROM works WHERE time_end IS NULL")
    return c.fetchall()

#create a function that returns a list of works
def get_all_works():
    c.execute("SELECT * FROM works")
    return c.fetchall()

# create a function that returns a list of all projects from table works
def get_all_projects():
    c.execute("SELECT DISTINCT project FROM works")
    return c.fetchall()

def stop_all_projects():
    try:
        c.execute("UPDATE works SET time_end = :now WHERE time_end IS NULL", {'now': now1})
    except Error as e:
        print(e)

# create a function that returns a list of all projects from table works with todays start_date
def get_todays_projects():
    today = str(datetime.now().date()) + "%"
    c.execute("SELECT * FROM works WHERE time_start LIKE :today", {'today': today})
    return c.fetchall()

# create a function that returns difference in seconds between two timestamps
def get_diffrence_in_seconds(time_start, time_end):
    time_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S.%f')
    time_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S.%f')
    return (time_end - time_start).total_seconds()

#return hours, minutes and seconds from seconds
def get_hours_minutes_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return h, m, s

def command_help():
    print("help:")
    print("python main.py help")
    print("python main.py delete")
    print("python main.py start project_name")
    print("python main.py stop")
    print("python main.py list")
    print("python main.py projects")
    print("python main.py stats")
    print("python main.py [opened]")


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

    if command == "delete":
        if os.path.exists(db_file):
            os.remove(db_file)
            print("delete file " + db_file)
        else:
            print("The file does not exist")
        exit()

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
                time_start text,
                time_end text
                )""")

    # create timestamp
    now1 = str(datetime.now())


    if command == "help":
        command_help()
    elif command == "opened":
        print(get_open_project())
    elif command == "list":
        print(get_all_works())
    elif command == "projects":
        print(get_all_projects())
    elif command == "stop":
        stop_all_projects()
        conn.commit()
        print("stopped projects at " + now1)
    elif command == "stats":
        print("todays stats")
        works =  get_todays_projects()
        # sum all seconds for every project
        sum = {}
        cnt = {}
        for work in works:
              sum[work[1]] = sum.get(work[1], 0) + get_diffrence_in_seconds(work[2], work[3] or now1)
              if work[3] is None:
                  cnt[work[1]] = work[1]

        # print the key and value for each item in sum
        for key, val in sum.items():
            h, m, s = get_hours_minutes_seconds(val)

            print(("* continued * " if key in cnt else "") + key + " " + str(int(h)) + " hodin, " + str(int(m)) + " minut," + str(int(s)) + " sekund")


    elif command == "start":
        if len(sys.argv) < 3:
            print("please enter a project name")
            command_help()
            exit()
        else:
            project = sys.argv[2]


        # update time_end at last row in table works with now1
        stop_all_projects()

        c.execute("INSERT INTO works (project, time_start) VALUES (:project, :now)", {'project': project, 'now': now1});
        conn.commit()
        # call the function and print the results
        print("start project: " + project + " at " + now1)
    else:
        print(get_open_project())

    # close the connection
    conn.close()

