"""
Methods for displaying time spent daily/weekly working.
"""
import pickle
import os
import datetime
import json

class Display():
	def __init__(self):
		if not self.is_empty():
			self.infile = open('../data/data.txt')
			self.days_dict = json.load(self.infile)
			print(self.days_dict)

	def is_empty(self):
		""" Checks if data.txt is empty"""
		return os.stat('../data/data.txt').st_size == 0 
		

	def get_daily_time(self, curr_date):
		""" This function retrieves the total time spent on the current date """
		total = 0.0
		if not self.is_empty():
			if curr_date in self.days_dict:
				lst = self.days_dict[curr_date]
				for _ in lst:
					total += _[0]
		return total


	def call_daily_time(self):
		""" Calls get_daily_time() with current date, used by stopwatch"""
		return self.get_daily_time(str(datetime.date.today()))


	def get_weekly_time(self):
		total = 0
		""" This function retrieves total time from current week"""
		# retrieve all dates in current week
		curr_day = datetime.date.today()
		weekday = curr_day.isoweekday()
		start = curr_day - datetime.timedelta(days=weekday)
		dates = [start + datetime.timedelta(days=d) for d in range(7)]

		# make sure weeks start on Mondays
		dates = [date + datetime.timedelta(days=1) for date in dates]

		for date in dates:
			total += self.get_daily_time(str(date))

		print(total)
		return total
		

	def convert_time(self, day_time):
		""" Convert to standard time used """
		hours = int(day_time/3600)
		minutes = int(day_time/60)
		seconds = int(day_time - minutes*60.0)
		msecs = int((day_time - minutes*60.0 - seconds)*100)
		return ('%02d:%02d:%02d:%02d' % (hours, minutes, seconds, msecs))


