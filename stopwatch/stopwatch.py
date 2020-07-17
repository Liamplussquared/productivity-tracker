import tkinter as tk
from tkinter import *
from datetime import date
import pickle
import time

class StopWatch(Frame):
	def __init__(self, parent=None, **kw):
		Frame.__init__(self, parent, **kw)
		self.start = 0.0
		self.lapsed_time = 0.0
		self.running = False
		self.time_string = StringVar()
		self.category = StringVar()
		self.make_label()

	def make_label(self):
		# label for time 
		label = Label(self, textvariable=self.time_string)
		self.set_time()
		label.pack(fill=X,expand=NO, pady=2, padx=2)

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
		hours = int(self.lapsed_time/3600)
		minutes = int(self.lapsed_time/60)
		seconds = int(self.lapsed_time - minutes*60.0)
		msecs = int((self.lapsed_time - minutes*60.0 -seconds)*100)
		self.time_string.set('%02d:%02d:%02d:%02d' % (hours, minutes, seconds, msecs))

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
			with open('data/data.pkl', 'rb') as pickle_in:
				all_days = pickle.load(pickle_in, encoding='bytes')
				print("DICTIONARY:", all_days)
		except EOFError:
			all_days = {str(date.today()): [[self.lapsed_time, self.category.get()]]}
			with open('data/data.pkl', 'wb') as pickle_out:
				pickle.dump(all_days, pickle_out)

		curr_date = str(date.today())
		if curr_date in all_days:
			# add to existing list
			all_days[curr_date].append([self.lapsed_time, self.category.get()])
		else:
			# make new entry
			all_days[curr_date] = [self.lapsed_time, self.category.get()]

		# save the dictionary
		with open('data/data.pkl', 'wb') as pickle_out:
			pickle.dump(all_days, pickle_out)

		# print(date.today(), round(self.lapsed_time, 3), self.category.get())

def main():
	window = tk.Tk()
	stopwatch = StopWatch(window)
	stopwatch.pack()

	# Buttons
	Button(window,text='Start',command=stopwatch.start_watch).pack(side=LEFT)
	Button(window,text='Stop',command=stopwatch.stop).pack(side=LEFT)
	Button(window,text='Reset',command=stopwatch.reset).pack(side=LEFT)
	Button(window,text='Exit',command=window.quit).pack(side=LEFT)

	window.mainloop()

if __name__ == '__main__':
	main()