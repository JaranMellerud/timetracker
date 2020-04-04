import tkinter as tk
import time
from functools import partial
from database import conn, cur, numActivities, getActivities


class TimeTracker:
    def __init__(self, root):
        # setting default values for height, width and font
        self.root = root
        self.root.title("Time Tracker")
        num_activities = numActivities()
        HEIGHT = 75 + num_activities * 35
        WIDTH = 300
        FONT_TYPE = 'helvetica'
        BIG_LABEL_FONT = (FONT_TYPE, '16', "bold")
        SMALL_LABEL_FONT = (FONT_TYPE, '13')
        ENTRY_FONT = (FONT_TYPE, '12')
        
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # if user doesnt have activities yet show label_add. else show the activities with time spent in a grid
        if num_activities == 0:
            self.label_add = tk.Label(self.canvas, text="Add An Activity To Start!")
            self.label_add.config(font=BIG_LABEL_FONT)
            self.canvas.create_window(140, 15, window=self.label_add)

            # section to add new activities
            self.entry_add = tk.Entry(self.canvas, text="Activity", font=ENTRY_FONT)
            self.canvas.create_window(110, 50, window=self.entry_add)   
            self.button_add = tk.Button(text="Add", command=self.addToDatabase)
            self.canvas.create_window(250, 50, window=self.button_add)
        else:
            self.frame_show = tk.Frame(self.canvas)
            self.frame_show.place(relwidth=1, relheight=1)
            self.label_activity = tk.Label(self.frame_show, text="Activity")
            self.label_activity.config(font=SMALL_LABEL_FONT)
            self.label_activity.grid(row=0, column=0)
            
            self.label_total = tk.Label(self.frame_show, text="Total")
            self.label_total.config(font=SMALL_LABEL_FONT)
            self.label_total.grid(row=0, column=1)

            self.label_time = tk.Label(self.frame_show, text="Time")
            self.label_time.config(font=SMALL_LABEL_FONT)
            self.label_time.grid(row=0, column=2)

            # creating rows with all the activities
            activities = getActivities()
            for ind, activity in enumerate(activities):
                for index, value in enumerate(activity):
                    self.label_activity = tk.Label(self.frame_show, text=value)
                    self.label_activity.grid(row=ind+1, column=index)     
                self.button_start_stop = tk.Button(self.frame_show, text="Start/Stop", command=partial(self.updateClock, row=ind+1, column=2, time_click=time.time()))
                self.button_start_stop.grid(row=ind+1, column=4)

            # section to add new activities
            self.entry_add = tk.Entry(self.canvas, text="Activity", font=ENTRY_FONT)
            self.canvas.create_window(110, 45 + num_activities * 35, window=self.entry_add)
            self.button_add = tk.Button(text="Add", command=self.addToDatabase)
            self.canvas.create_window(250, 45 + num_activities * 35, window=self.button_add)

    # function to add activity to activities table in timetracker.db
    def addToDatabase(self):
        cur.execute(f'INSERT INTO Activities (activity) VALUES ("{self.entry_add.get()}")')
        conn.commit()

    # function that runs the clock and displays time. the function is initialized by the start_stop_clock function
    def updateClock(self, row, column, time_click):
        now = time.time()
        timer = self.frame_show.grid_slaves(row=row, column=column)[-1]
        time_passed = now - time_click
        timer.config(text=time_passed)
        timer.after(1000, self.updateClock, row, column, time_click)

    # starts and stops the clock. command for the start/stop button
    #def startClock(self):
        #time_click = 
            
        
        
    


if __name__ == "__main__":
    root = tk.Tk()
    timetracker = TimeTracker(root)
    root.mainloop()