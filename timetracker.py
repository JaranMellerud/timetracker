import tkinter as tk
from database import DataBase


class TimeTracker:
    def __init__(self, master):
        # loading variables to set properties
        self.num_activities = database.numActivities()
        self.activities = database.getActivities()

        # properties for sizes and fonts
        self.HEIGHT = 75 + self.num_activities * 35
        self.WIDTH = 300
        self.TITLE = "Time Tracker"
        self.FONT_TYPE = 'helvetica'
        self.BIG_LABEL_FONT = (self.FONT_TYPE, '16', "bold")
        self.SMALL_LABEL_FONT = (self.FONT_TYPE, '13')
        self.ENTRY_FONT = (self.FONT_TYPE, '12')

        self.master = master
        self.master.title(self.TITLE)
        self.canvas = tk.Canvas(self.master, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill="both", expand=True)

        self.entry_add = None
        
        # showing different interface if no activities added
        if self.num_activities == 0:
            self.showFirstInterface()
        else:
            self.showSecondInterface()

    # function to show interface if there arent added any activities yet
    def showFirstInterface(self):        
        self.label_add = tk.Label(self.canvas, text="Add An Activity To Start!", font=self.BIG_LABEL_FONT)        
        self.canvas.create_window(140, 15, window=self.label_add)
        # entry to add new activities
        self.entry_add = tk.Entry(self.canvas, text="Activity", font=self.ENTRY_FONT)
        self.canvas.create_window(110, 50, window=self.entry_add)
        self.button_add = tk.Button(text="Add", command=lambda:[database.addActivity(self.entry_add), self.entry_add.delete(first=0, last="end"), self.showSecondInterface()])
        self.button_add.focus_set()
        self.canvas.create_window(250, 50, window=self.button_add)
        
    # function to show interface if there are added activities
    def showSecondInterface(self):
        # grid with activities, total and time in a frame
        self.frame = tk.Frame(self.canvas)
        self.frame.place(relwidth=1, relheight=1)
        self.label_activity = tk.Label(self.frame, text="Activity", font=self.SMALL_LABEL_FONT)
        self.label_activity.grid(row=0, column=0)   
        self.label_total = tk.Label(self.frame, text="Total", font=self.SMALL_LABEL_FONT)
        self.label_total.grid(row=0, column=1)
        self.label_time = tk.Label(self.frame, text="Time", font=self.SMALL_LABEL_FONT)
        self.label_time.grid(row=0, column=2)
        # creating rows with all the activities
        self.createActivityRows()
        # creating entry and button to add new activities
        self.createActivityEntry()

    # function to create entry and button to add new activities
    def createActivityEntry(self):
        if self.entry_add is not None:
            self.entry_add.destroy()
            self.button_add.destroy()
        self.num_activities = database.numActivities()
        self.entry_add = tk.Entry(self.canvas, text="Activity", font=self.ENTRY_FONT)
        self.canvas.create_window(110, 45 + self.num_activities * 35, window=self.entry_add)
        self.button_add = tk.Button(text="Add", command=lambda:[database.addActivity(self.entry_add), self.entry_add.delete(first=0, last="end"), self.createActivityRows()])
        self.canvas.create_window(250, 45 + self.num_activities * 35, window=self.button_add)

    # function to create rows with activities and time
    def createActivityRows(self):
        self.activities = database.getActivities()
        self.num_activities = database.numActivities()
        self.HEIGHT = 75 + self.num_activities * 35
        self.createActivityEntry()
        for ind, activity in enumerate(self.activities):
            for index, value in enumerate(activity):
                self.label_activity = tk.Label(self.frame, text=value)
                self.label_activity.grid(row=ind+1, column=index)     
            self.button_start_stop = tk.Button(self.frame, text="Start/Stop")
            self.button_start_stop.grid(row=ind+1, column=4)
        self.canvas.configure(height=self.HEIGHT)


if __name__ == "__main__":
    database = DataBase()
    database.createTable()
    master = tk.Tk()
    tt = TimeTracker(master)
    master.mainloop()