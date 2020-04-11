import sqlite3
from datetime import datetime


class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect("timetracker.db")
        self.cur = self.conn.cursor()
        self.createTable()

    def createTable(self):
        """ Creating table in database if the table does not exists already. """
        date = datetime.today().strftime('%Y-%m-%d')
        self.cur.execute(f"CREATE TABLE IF NOT EXISTS Activities (id INTEGER PRIMARY KEY AUTOINCREMENT, activity TEXT, time TEXT DEFAULT '00:00:00', date_added TEXT DEFAULT '{date}')")
        self.conn.commit()

    def addActivity(self, activity_to_add):
        """ Adds activity to the database """
        self.cur.execute(f'INSERT INTO Activities (activity) VALUES ("{activity_to_add.get()}")')
        self.conn.commit()

    def saveTime(self, activity_name, activity_time):
        """ Saves the time to the database """
        self.cur.execute(f'UPDATE Activities SET time="{activity_time}" WHERE activity="{activity_name}"' )
        self.conn.commit()

    def numActivities(self):
        """ Checks how many activities there are in the database """
        num_activities = len(self.cur.execute("SELECT * FROM Activities").fetchall())
        return num_activities

    def getActivities(self):
        """ Gets all the activities with time spent in total and time spent today """
        activities = self.cur.execute("SELECT activity, time, date_added FROM Activities").fetchall()
        return activities

    def getActivity(self, activity):
        """ Gets one activity with the time spent on the activity"""
        activity = self.cur.execute(f"SELECT activity, time FROM Activities WHERE activity='{activity}'").fetchall()[0]
        return activity

    def deleteActivity(self, activity_to_delete):
        """ Deletes activity from the database """
        self.cur.execute(f'DELETE FROM Activities WHERE activity="{activity_to_delete}"')
        self.conn.commit()

    def deleteAllFromTable(self):
        """ Deletes all activities from the database """
        self.cur.execute("DELETE FROM Activities")
        self.conn.commit()