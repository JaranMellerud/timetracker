import tkinter as tk
from stopwatch import StopWatch
from database import DataBase


class TimeTracker:
    def __init__(self, root):
        self.activities = db.getActivities()
        self.num_activities = db.getActivities()
        self.FONT_TYPE = "helvetica" #property
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.saveTimeToDatabase) # saves the current times from the labels to the database on exit
        self.root.title("Time Tracker")
        self.updateInterface()

    def updateInterface(self):
        """ Updates the interface, between two different ones. """
        self.num_activities = db.getActivities()
        try:
            self.main_frame.destroy()
        except Exception:
            pass
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()
        if not self.num_activities:
            self.showFirstInterface()
        else:
            self.showSecondInterface()
    
    def showFirstInterface(self):
        """ Shows the interface if the user has not added any activities yet. """
        self.add_activity_label = tk.Label(self.main_frame, text="Add An Activity To Start!", font=(self.FONT_TYPE, '16', 'bold'))
        self.add_activity_label.pack()
        self.createAddArea() # initializing the function to create the area to add the new activities.

    def showSecondInterface(self):
        """ Shows the interface if the user has added activities. """
        def createActivityRows():
            """ Creates a rows with each activity, time and start/stop button. Inside a frame. """
            self.activities_frame = tk.Frame(self.main_frame)
            self.activities_frame.pack()
            self.title_label_1 = tk.Label(self.activities_frame, text="Activity")
            self.title_label_1.grid(row=0, column=0)
            self.title_label_2 = tk.Label(self.activities_frame, text="Total")
            self.title_label_2.grid(row=0, column=1)
            self.title_label_3 = tk.Label(self.activities_frame, text="Session")
            self.title_label_3.grid(row=0, column=2)
            """ Creates a dictionary where the keys are activity number and the values are lists with the corresponding activity name and time labels. """
            self.activities = db.getActivities()
            self.activities_dict = {}
            for index, activity in enumerate(self.activities):
                self.activities_dict[index] = []
                for ind, act_time in enumerate(activity):
                    """ If ind == 0, then the object is a activity name, and labels are created for them.
                        If ind == 1, then the object is a timestring, and labels are created for them with the StopWatch class. """
                    if ind == 0:
                        self.activities_dict[index].append(tk.Label(self.activities_frame, text=act_time))
                        self.activities_dict[index][ind].grid(row=index+1, column=ind)
                    elif ind == 1:
                        self.activities_dict[index].append(StopWatch(self.activities_frame, activity[0], total_or_session="total", row=index+1, column=ind))
                        self.activities_dict[index].append(StopWatch(self.activities_frame, activity[0], total_or_session="session", row=index+1, column=ind+1))
                self.activities_dict[index].append(tk.Button(self.activities_frame, text="Start/Stop", command=self.combine_funcs(self.activities_dict[index][1].startStop, self.activities_dict[index][2].startStop)))             
                self.activities_dict[index][-1].grid(row=index+1, column=3)
        createActivityRows() # initializing the function to create the rows with all the activities.
        self.createAddArea() # initializing the function to create the area to add new activities.

    """ Combines functions. Is used to execute the two commands for the start/stop button (start/stop the total time and start/stop the session time) """
    def combine_funcs(self, *funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func


    def createAddArea(self):
        """ Creates area where the user can add new activities. """
        self.add_activity_entry = tk.Entry(self.main_frame, text="Activity", font=(self.FONT_TYPE, '13'))
        self.add_activity_entry.pack(side=tk.LEFT)
        self.add_activity_button = tk.Button(self.main_frame, text="Add", font=(self.FONT_TYPE, '13'), command=lambda:[db.addActivity(self.add_activity_entry), self.add_activity_entry.delete(first=0, last="end"), self.updateInterface()])
        self.add_activity_button.pack(side=tk.LEFT)

    def saveTimeToDatabase(self):
        """ Saves the current time from the labels to the database. Is to be run on exit """
        for value in self.activities_dict.values():
            activity_name = value[0]['text']
            activity_time = value[1].timestr.get()
            db.saveTime(activity_name, activity_time)
        self.root.destroy()


if __name__ == '__main__':
    db = DataBase()
    root = tk.Tk()
    tt = TimeTracker(root)
    root.mainloop()
