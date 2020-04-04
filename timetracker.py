import tkinter as tk
from database import DataBase


class TimeTracker:
    def __init__(self, master):
        # loading variables to set properties
        self.num_activities = database.numActivities()
        self.activities = database.getActivities()

        # properties for sizes and fonts
        HEIGHT = 75 + self.num_activities * 35
        WIDTH = 300
        TITLE = "Time Tracker"
        FONT_TYPE = 'helvetica'
        BIG_LABEL_FONT = (FONT_TYPE, '16', "bold")
        SMALL_LABEL_FONT = (FONT_TYPE, '13')
        ENTRY_FONT = (FONT_TYPE, '12')

        self.master = master
        self.master.title(TITLE)
        self.canvas = tk.Canvas(self.master, width=WIDTH, height=HEIGHT)
        self.canvas.pack()
        
        # showing different interface if no activities added
        if self.num_activities == 0:
            self.label_add = tk.Label(self.canvas, text="Add An Activity To Start!", font=BIG_LABEL_FONT)        
            self.canvas.create_window(140, 15, window=self.label_add)
            # entry to add new activities
            self.entry_add = tk.Entry(self.canvas, text="Activity", font=ENTRY_FONT)
            self.canvas.create_window(110, 50, window=self.entry_add)
            self.button_add = tk.Button(text="Add", command=lambda:[database.addActivity(self.entry_add), self.entry_add.delete(first=0, last="end")])
            self.button_add.focus_set()
            self.canvas.create_window(250, 50, window=self.button_add)
        else:
            # grid with activities, total and time in a frame
            self.frame = tk.Frame(self.canvas)
            self.frame.place(relwidth=1, relheight=1)
            self.label_activity = tk.Label(self.frame, text="Activity", font=SMALL_LABEL_FONT)
            self.label_activity.grid(row=0, column=0)   
            self.label_total = tk.Label(self.frame, text="Total", font=SMALL_LABEL_FONT)
            self.label_total.grid(row=0, column=1)
            self.label_time = tk.Label(self.frame, text="Time", font=SMALL_LABEL_FONT)
            self.label_time.grid(row=0, column=2)

            # creating rows with all the activities
            self.createActivityRows()

            # section to add new activities
            self.entry_add = tk.Entry(self.canvas, text="Activity", font=ENTRY_FONT)
            self.canvas.create_window(110, 45 + self.num_activities * 35, window=self.entry_add)
            self.button_add = tk.Button(text="Add", command=lambda:[database.addActivity(self.entry_add), self.entry_add.delete(first=0, last="end"), self.createActivityRows()])
            self.canvas.create_window(250, 45 + self.num_activities * 35, window=self.button_add)

    # function to create rows with activities and time
    def createActivityRows(self):
        self.activities = database.getActivities()
        for ind, activity in enumerate(self.activities):
            for index, value in enumerate(activity):
                self.label_activity = tk.Label(self.frame, text=value)
                self.label_activity.grid(row=ind+1, column=index)     
            self.button_start_stop = tk.Button(self.frame, text="Start/Stop")
            self.button_start_stop.grid(row=ind+1, column=4)


if __name__ == "__main__":
    database = DataBase()
    database.createTable()
    master = tk.Tk()
    tt = TimeTracker(master)
    master.mainloop()