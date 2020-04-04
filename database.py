import sqlite3


class DataBase():
    def __init__(self):
        self.conn = sqlite3.connect("timetracker.db")
        self.cur = self.conn.cursor()

    # creating table in database if table not exists already
    def createTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Activities (id INTEGER PRIMARY KEY AUTOINCREMENT, activity TEXT, time_total REAL DEFAULT '0', time_today REAL DEFAULT 0)")
        self.conn.commit()

    # function to check how many activities there are in the database
    def numActivities(self):
        self.num_activities = len(self.cur.execute("SELECT * FROM Activities").fetchall())
        return self.num_activities

    # function to get all the activities with time spent in total and time spent today
    def getActivities(self):
        self.activities = self.cur.execute("SELECT activity, time_total, time_today FROM Activities").fetchall()
        return self.activities

    # function to delete all activities
    def deleteAllFromTable(self):
        self.cur.execute("DELETE FROM Activities")
        self.conn.commit()

    # function to add activity to database
    def addActivity(self, activity_to_add):
        self.cur.execute(f'INSERT INTO Activities (activity) VALUES ("{activity_to_add.get()}")')
        self.conn.commit()