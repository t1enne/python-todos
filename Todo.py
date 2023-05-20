from datetime import date
from sqlite3 import Cursor
from configparser import ConfigParser


class Todo:
    """
    Class that represents a single Todo.
    """

    columns = []
    taskname = ""
    description = ""
    cursor: Cursor

    def __init__(self, cursor, taskname):
        config = ConfigParser()
        config.read("config.ini")
        config.sections()

        self.columns = config["main"]["columns"]
        self.cursor = cursor
        self.taskname = taskname

        while self.taskname == None:
            query = "SELECT * FROM todo"
            self.cursor.execute(query)
            print(self.cursor.fetchall())

            print("Please provide the taskname")
            tmp = input()
            if len(tmp) == 0:
                continue
            self.taskname = tmp

    def create(self):
        """
        Add a todo with given filename and description. If the required positional params
        are not provided, they will be prompted for.
        """

        while self.description == "":
            print("Please provide a description")
            tmp = input()
            if len(tmp) == 0:
                continue
            self.description = tmp

        query = f"INSERT INTO todo VALUES ('{date.today()}', '{self.taskname}', '{self.description}', 'ADDED')"
        self.cursor.execute(query)
        return 1

    def read(self):
        query = f"SELECT * FROM todo WHERE task LIKE '{self.taskname}%'"
        self.cursor.execute(query)
        elem = self.cursor.fetchone()
        print(elem)
        return 1

    def set(self):
        column = ""
        value = ""
        while column == "":
            print("Please provide a column")
            tmp = input()
            if len(tmp) == 0:
                continue
            column = tmp

        while value == "":
            print("Please provide a value")
            tmp = input()
            if len(tmp) == 0:
                continue
            value = tmp

        query = (
            f"UPDATE todo SET {column} = '{value}' WHERE task LIKE '{self.taskname}%'"
        )
        self.cursor.execute(query)
        entry = self.cursor.fetchone()
        print(entry)
        return 0

    def delete(self):
        query = f"DELETE from todo WHERE task='{self.taskname}'"
        print(query)
        self.cursor.execute(query)
        return 1
