"""
Methods for displaying time spent daily/weekly working.
"""
import pickle
import os
from datetime import date

class Display():
	def __init__(self):
		self.infile = open('../data/data.pkl', 'rb')
		self.days_dict = pickle.load(self.infile)
		self.daily_time = self.get_daily_time()


	def get_daily_time(self):
		""" This function retrieves the total time spent on the current date """
		_day_time = 0
		_curr_date = str(date.today())
		_day_items = self.days_dict[_curr_date]

		for item in _day_items:
			_day_time += item[0]

		return _day_time

	def convert_time(self, day_time):
		""" Convert to standard time used """
		_hours = int(day_time/3600)
		_minutes = int(day_time/60)
		_seconds = int(day_time - _minutes*60.0)
		_msecs = int((day_time - _minutes*60.0 - _seconds)*100)
		return ('%02d:%02d:%02d:%02d' % (_hours, _minutes, _seconds, _msecs))


if __name__ == '__main__':
	dsp = Display()


