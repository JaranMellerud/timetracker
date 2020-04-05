import time


class StopWatch:
    def __init__(self):
        self.seconds = int(0)
        self.minutes = int(0)
        self.hours = int(0)
        self.run = False

        # creating the stopwatch
        self.createStopWatch()

    # function to create the stopwatch
    def createStopWatch(self):
        while self.run == True:
            if self.seconds > 59:
                self.seconds = 0
                self.minutes += 1
            if self.minutes > 59:
                self.minutes = 0
                self.hours += 1
            self.seconds += 1
            # setting format of the clock to hh:mm:ss
            if len(str(self.hours)) == 1:
                self.hours_string = "0" + str(self.hours)
            else:
                self.hours_string = str(self.hours)
            if len(str(self.minutes)) == 1:
                self.minutes_string = "0" + str(self.minutes)
            else:
                self.minutes_string = str(self.minutes)
            if len(str(self.seconds)) == 1:
                self.seconds_string = "0" + str(self.seconds)
            else:
                self.seconds_string = str(self.seconds)
            # string with time to be displayed
            self.time_string = self.hours_string + ":" + self.minutes_string + ":" + self.seconds_string
            time.sleep(1)
            print(self.time_string)

    # function to start and stop the stopwatch
    def startStopWatch(self):
        pass
