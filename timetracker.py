import tkinter as tk
import tkinter.messagebox
from functools import partial
from PIL import Image, ImageTk
from stopwatch import StopWatch
from database import DataBase


class TimeTracker:
    def __init__(self, root):
        self.setProperties()
        self.activities = db.getActivities()
        self.num_activities = db.getActivities()
        self.root = root
        self.root.configure(bg=self.background_color)
        self.root.protocol("WM_DELETE_WINDOW", partial(self.saveTimeToDatabase, self.root.destroy)) # saves the current times from the labels to the database on exit
        self.root.title("Time Tracker")
        self.updateInterface()

    def setProperties(self):
        """ Sets the styling properties for the timetracker object """
        self.STARTSTOPICON = ImageTk.PhotoImage(Image.open("./static/play_pause.png").resize((30, 30), Image.ANTIALIAS))
        self.DELETEICON = ImageTk.PhotoImage(Image.open("./static/delete.png").resize((30, 30), Image.ANTIALIAS))
        self.ADDICON = ImageTk.PhotoImage(Image.open("./static/add.png").resize((30, 30), Image.ANTIALIAS))
        self.PADDINGX = 10 # Horizontal padding between the grid elements
        self.PADDINGY = 20 # Vertical padding between the grid elements
        self.FONTTYPE = "Helvetica"
        self.TITLEFONT = (self.FONTTYPE, 16, "bold")
        self.ACTIVITYFONT = (self.FONTTYPE, 12)       
        self.background_color = "gray26"
        self.foreground_color = "white"


    def updateInterface(self):
        """ Updates the interface, between two different ones. """
        self.num_activities = db.getActivities()
        try:
            self.main_frame.destroy()
        except Exception:
            pass
        self.main_frame = tk.Frame(self.root, bg=self.background_color)
        self.main_frame.pack(pady=10, padx=10)
        if not self.num_activities:
            self.showFirstInterface()
        else:
            self.showSecondInterface()
    
    def showFirstInterface(self):
        """ Shows the interface if the user has not added any activities yet. """
        self.add_activity_label = tk.Label(self.main_frame, text="Add An Activity To Start!", font=(self.FONTTYPE, '16', 'bold'), fg=self.foreground_color, bg=self.background_color)
        self.add_activity_label.pack()
        self.createAddArea() # initializing the function to create the area to add the new activities.

    def showSecondInterface(self):
        """ Shows the interface if the user has added activities. """
        def createActivityRows():
            """ Creates a rows with each activity, time and start/stop button. Inside a frame. """
            self.activities_frame = tk.Frame(self.main_frame, bg=self.background_color)
            self.activities_frame.pack()
            self.title_label_1 = tk.Label(self.activities_frame, text="Activity", font=self.TITLEFONT, bg=self.background_color, fg=self.foreground_color)
            self.title_label_1.grid(row=0, column=0, padx=self.PADDINGX)
            self.title_label_2 = tk.Label(self.activities_frame, text="Total", font=self.TITLEFONT, bg=self.background_color, fg=self.foreground_color)
            self.title_label_2.grid(row=0, column=1, padx=self.PADDINGX)
            self.title_label_3 = tk.Label(self.activities_frame, text="Session", font=self.TITLEFONT, bg=self.background_color, fg=self.foreground_color)
            self.title_label_3.grid(row=0, column=2, padx=self.PADDINGX)
            """ Creates a dictionary where the keys are activity number and the values are lists with the corresponding activity name and time labels. """
            self.activities = db.getActivities()
            self.activities_dict = {}
            for index, activity in enumerate(self.activities):
                self.activities_dict[index] = []
                for ind, act_time in enumerate(activity):
                    """ If ind == 0, then the object is a activity name, and labels are created for them.
                        If ind == 1, then the object is a timestring, and labels are created for them with the StopWatch class. """
                    if ind == 0:
                        self.activities_dict[index].append(tk.Label(self.activities_frame, text=act_time, font=self.ACTIVITYFONT, bg=self.background_color, fg=self.foreground_color))
                        self.activities_dict[index][ind].grid(row=index+1, column=ind)
                    elif ind == 1:
                        self.activities_dict[index].append(StopWatch(self.activities_frame, activity[0], total_or_session="total", row=index+1, column=ind))
                        self.activities_dict[index].append(StopWatch(self.activities_frame, activity[0], total_or_session="session", row=index+1, column=ind+1))
                self.activities_dict[index].append(tk.Button(self.activities_frame, text="Start/Stop", borderwidth=0, highlightthickness=0, fg=self.background_color, activebackground=self.background_color, bg=self.background_color, image=self.STARTSTOPICON, command=self.combine_funcs(self.activities_dict[index][1].startStop, self.activities_dict[index][2].startStop)))             
                self.activities_dict[index][-1].grid(row=index+1, column=3)
                self.activities_dict[index].append(tk.Button(self.activities_frame, text="Delete", borderwidth=0, highlightthickness=0, fg=self.background_color, activebackground=self.background_color, bg=self.background_color, image=self.DELETEICON, command=lambda:[self.deleteActivity(activity[0]), self.updateInterface()]))
                self.activities_dict[index][-1].grid(row=index+1, column=4)

        createActivityRows() # initializing the function to create the rows with all the activities.
        self.createAddArea() # initializing the function to create the area to add new activities.

    """ Combines functions. Is used to execute the two commands for the start/stop button (start/stop the total time and start/stop the session time) """
    def combine_funcs(self, *funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)
        return combined_func

    def deleteActivity(self, activity):
        """ Opens a pop up window with confirmation. Deletes activity if yes. """
        result = tkinter.messagebox.askyesno('Delete Activity', 'Are you sure you want to delete the activity?')
        if result:
            db.deleteActivity(activity)

    def createAddArea(self):
        """ Creates area where the user can add new activities. """
        self.add_activity_entry = tk.Entry(self.main_frame, text="Activity", font=(self.FONTTYPE, '13'))
        self.add_activity_entry.pack(side=tk.LEFT, ipadx=30)
        self.add_activity_button = tk.Button(self.main_frame, text="Add", image=self.ADDICON, borderwidth=0, highlightthickness=0, fg=self.background_color, activebackground=self.background_color, bg=self.background_color, font=(self.FONTTYPE, '13'), command=lambda:[db.addActivity(self.add_activity_entry), self.add_activity_entry.delete(first=0, last="end"), self.updateInterface()])
        self.add_activity_button.pack(side=tk.LEFT)

    def saveTimeToDatabase(self, second_command=None):
        """ Saves the current time from the labels to the database. Is to be run on exit and when updating the window. That is what the second_command is for."""
        try:
            for value in self.activities_dict.values():
                activity_name = value[0]['text']
                activity_time = value[1].timestr.get()
                db.saveTime(activity_name, activity_time)
        except Exception:
            pass
        second_command()


if __name__ == '__main__':
    db = DataBase()
    root = tk.Tk()
    tt = TimeTracker(root)
    root.mainloop()
