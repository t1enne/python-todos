#!/usr/bin/env python3
import argparse
import sys
import sqlite3
from configparser import ConfigParser
from re import split
from Todo import Todo

config = ConfigParser()
config.read("config.ini")
config.sections()
columns = split(",", config["main"]["columns"])

if len(sys.argv) < 2:
    print("Use [-h] for help with commands")
    exit(1)

dbconn = sqlite3.connect("todos.db")
cur = dbconn.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE name='todo'")
if res.fetchone() is None:
    cur.execute(f"CREATE TABLE todo({config['main']['columns']})")

parser = argparse.ArgumentParser(
    description=f"""
A simple todo app. You can add, read or delete todos.
They will be saved in a sqlite db.
The fields will be {config['main']['columns']}
"""
)
parser.add_argument("action")
parser.add_argument("taskname", nargs="?")

if sys.argv[1] == "set":
    parser.add_argument("field", nargs="?")
    parser.add_argument("new_value", nargs="?")
elif sys.argv[1] == "add":
    parser.add_argument("description", nargs="?")

args = parser.parse_args()

if args.action == "list":
    cur.execute("SELECT * FROM todo")
    for ti, task in enumerate(cur.fetchall()):
        print(f"\nTask #{ti}\n")
        for fi, field in enumerate(task):
            print(f"{columns[fi]}: {field}")

    dbconn.close()
    exit(1)

todo = Todo(cur, args.taskname)
if args.action == "add":
    todo.create()
    dbconn.commit()
elif args.action == "read":
    todo = Todo(cur, args.taskname)
    todo.read()
elif args.action == "delete":
    todo.delete()
    dbconn.commit()
elif args.action == "set":
    todo = Todo(cur, args.taskname)
    todo.set()
else:
    print("Use [-h] for help with commands")

dbconn.close()
exit(1)
