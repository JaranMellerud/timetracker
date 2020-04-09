import tkinter as tk
import time
from database import DataBase


class StopWatch:  
    """ Implements a stop watch label. """                                                                
    def __init__(self, frame, activity, row, column):        
        db = DataBase()
        self.activity = db.getActivity(activity)
        self._start = 0.0
        self._elapsedtime = self.getElapsedTime()
        self._running = 0
        self.timestr = tk.StringVar()
        self.frame = frame
        self.row = row
        self.column = column
        self.makeWidgets()
        self.makeButtons()

    def getElapsedTime(self):
        """ Gets the elapsed time for the activity from the database """
        seconds_elap = int(self.activity[-1][-2:])
        minutes_elap = int(self.activity[-1][-5:-3])
        hours_elap = int(self.activity[-1][-8:-6])
        total_elap = seconds_elap + minutes_elap*60 + hours_elap*3600
        return total_elap

    def makeWidgets(self):                         
        """ Make the time label. """
        self.time_label = tk.Label(self.frame, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        self.time_label.grid(row=self.row, column=self.column)

    def makeButtons(self):
        """ Make the buttons for start/stop and reset. """
        self.start_stop_button = tk.Button(self.frame, text="Start/Stop", command=self.startStop)
        self.start_stop_button.grid(row=self.row, column=self.column+1)
        self.reset_button = tk.Button(self.frame, text="Reset", command=self.Reset)
        self.reset_button.grid(row=self.row, column=self.column+2)               
    
    def _update(self): 
        """ Update the label with elapsed time. """
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.time_label.after(50, self._update)
    
    def _setTime(self, elap):
        """ Set the time string to Minutes:Seconds:Hundreths """
        hours = int(elap/3600)
        minutes = int(elap/60 - hours*60)
        seconds = int(elap - hours*3600 - minutes*60)                
        self.timestr.set('%02d:%02d:%02d' % (hours, minutes, seconds))
        
    def startStop(self):                                                     
        """ The first if starts the stopwatch, ignore if running.
            The second elif stops the stopwatch, ignore if stopped."""
        if not self._running:            
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = 1
        elif self._running:
            self.time_label.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = 0

    def Reset(self):                                  
        """ Reset the stopwatch. """
        self._start = time.time()         
        self._elapsedtime = 0.0    
        self._setTime(self._elapsedtime)