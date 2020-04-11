# timetracker
With TimeTracker, you can track the time you spend on different activities. The tool is designed for people learning new skills that requires a lot of time. Having a time tracker application can add some motivation for spending the necessary time on something, for example if you are studying a new language. The app allows you to track several different activities.

## Getting Started

### Prerequisites
You need the Python interpreter installed on your computer. If you are using Python2, just import tkinter with a capital T.

### Installing
**1.** Change directory to the directory you want the files to be stored inside, and clone the git repository with this command:
```
git clone https://github.com/JaranMellerud/timetracker.git
```
**2.** Change directory to the project directory and install the required packages (preferably in a virtual environment you have created):
```
pip install -r requirements.txt
```
**3.** Run the application like this:
```
python timetracker.py
```
**4.** Now the GUI opens. Here you can add or delete new activities and start/pause the timer. When you open the application again after you have closed it, all your activities and the time spent will be saved.

## Why I Made It
I am learning Russian, as well as programming, and I thought it would be nice to be able to track the time I spend on learning these skills. This way, I can set weekly minimum goals for how many hours I want to spend learning. I tried a few different apps, but they were just to complicated. I wanted an extremely minimalistic GUI that just sits in the corner of the screen and records time, nothing more. In addition, I realized that I should learn more about object-oriented programming. Building a GUI with tkinter is a good way to do this, since you have to organize a lot of different objects when using tkinter.

## What I Have Learned
* Building a simple Graphical User Interface with tkinter
* Setting up and querying databases with sqlite3
* Object-oriented programming fundamentals
* Working with time with the built-in time module

## Images
![Without added activities](https://user-images.githubusercontent.com/56685171/79041373-a393e400-7bef-11ea-89a3-3d26a046d067.png)
![With added activities](https://user-images.githubusercontent.com/56685171/79041470-709e2000-7bf0-11ea-8b1e-0d01526505fa.png)
