import tkinter as tk
from tkinter import *
from datetime import date
import pickle
import time
from time_info import Display

class StopWatch(Frame):
	def __init__(self, parent=None, **kw):
		Frame.__init__(self, parent, **kw)

		# variables for managing running of clock
		self.start = 0.0
		self.lapsed_time = 0.0
		self.running = False

		# store time spent on current task
		self.time_string = StringVar()

		# store time spent today
		self.dsp = Display()
		self.day_time = self.dsp.call_daily_time()
		self.day_string = StringVar()

		# store time spent this week
		self.week_time = self.dsp.get_weekly_time()
		self.week_string = StringVar()

		# user inputted category
		self.category = StringVar()
		self.make_label()

	def make_label(self):
		# labels for time spent in current split and daily total
		label = Label(self, textvariable=self.time_string)
		day_label = Label(self,textvariable=self.day_string)
		week_label = Label(self,textvariable=self.week_string)

		# change font, size of labels
		week_label.config(font=("Courier", 8))
		day_label.config(font=("Courier", 10))
		label.config(font=("Courier", 12))

		# initialise times
		self.set_time()

		# pack the labels
		week_label.pack(side = "top")
		day_label.pack(side = "top")
		label.pack(side = "top")
	
		# entry for user input
		entry = Entry(self, textvariable=self.category)
		entry.pack()


	def update(self):
		"""Calculates time passed and calls set_time, waits 50ms to do the same"""
		self.lapsed_time = time.time() - self.start
		self.set_time()
		self.timer = self.after(50, self.update)

	def set_time(self):
		"""Sets the time on the stopwatch"""
		self.week_string.set("Weekly time: " + self.convert_time(self.week_time + self.lapsed_time))
		self.day_string.set("Today's time: " + self.convert_time(self.day_time + self.lapsed_time))
		self.time_string.set("Current split: " + self.convert_time(self.lapsed_time))

	def convert_time(self, time_dur):
		hours = int(time_dur/3600)
		minutes = int(time_dur/60)
		seconds = int(time_dur - minutes*60.0)
		msecs = int((time_dur - minutes*60.0 -seconds)*100)
		return ('%02d:%02d:%02d:%02d' % (hours, minutes, seconds, msecs))

	def start_watch(self):
		"""Starts the timer, ignored if already running"""
		if not self.running:
			self.start = time.time() - self.lapsed_time
			self.update()
			self.running = True

	def stop(self):
		"""Stops the timer, ignored if not running"""
		if self.running:
			self.after_cancel(self.timer)
			self.lapsed_time = time.time() - self.start
			self.set_time()
			self.running = False

	def reset(self):
		"""Resets the time"""
		self.stop()
		self.start = time.time()

		# update day & week time
		self.week_time += self.lapsed_time
		self.day_time += self.lapsed_time

		# retrieve what user was working on from the Entry
		if self.lapsed_time > 0 :
			self.log_activity()

		# reset time & input box
		self.lapsed_time = 0.0
		self.category.set("")
		self.set_time()

	def log_activity(self):
		"""Store time of split & what was done"""
		# load the dictionary
		try:
			with open('../data/data.pkl', 'rb') as pickle_in:
				all_days = pickle.load(pickle_in, encoding='bytes')
				print("DICTIONARY:", all_days)
		except EOFError:
			all_days = {str(date.today()): [[self.lapsed_time, self.category.get()]]}
			with open('../data/data.pkl', 'wb') as pickle_out:
				pickle.dump(all_days, pickle_out)
			return

		curr_date = str(date.today())
		if curr_date in all_days:
			# add to existing list
			all_days[curr_date].append([self.lapsed_time, self.category.get()])
		else:
			# make new entry
			all_days[curr_date] = [self.lapsed_time, self.category.get()]

		# save the dictionary
		with open('../data/data.pkl', 'wb') as pickle_out:
			pickle.dump(all_days, pickle_out)

		# print(date.today(), round(self.lapsed_time, 3), self.category.get())

def main():
	window = tk.Tk()
	window.geometry("300x300")
	stopwatch = StopWatch(window)
	stopwatch.pack(expand=True)

	# Buttons
	Button(window,text='Start',command=stopwatch.start_watch).pack(side="top", pady=5)
	Button(window,text='Stop',command=stopwatch.stop).pack(side="top", pady=5)
	Button(window,text='Reset',command=stopwatch.reset).pack(side="top", pady=5)
	Button(window,text='Exit',command=window.quit).pack(side="top", pady=5)

	window.mainloop()

if __name__ == '__main__':
	main()