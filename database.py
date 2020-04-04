import sqlite3

# database connection and cursor in sqlite
conn = sqlite3.connect("timetracker.db")
cur = conn.cursor()

# creating table in database if table not exists already
cur.execute("CREATE TABLE IF NOT EXISTS Activities (id INTEGER PRIMARY KEY AUTOINCREMENT, activity TEXT, time_total REAL DEFAULT '0', time_today REAL DEFAULT 0)")
conn.commit()

# function to check how many activities added
def numActivities():
    num_activities = len(cur.execute("SELECT * FROM Activities").fetchall())
    return num_activities

# function to get all the activities with time
def getActivities():
    activities = cur.execute("SELECT activity, time_total, time_today FROM Activities").fetchall()
    return activities


#cur.execute("delete from Activities")
#conn.commit()