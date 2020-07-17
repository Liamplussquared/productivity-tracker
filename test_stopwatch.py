import unittest
import tkinter as tk
import time
from stopwatch import stopwatch

class TestSW(unittest.TestCase):
	def setUp(self):
		"""Create the tkinter app"""
		self.window = tk.Tk()
		self.sw = stopwatch.StopWatch(self.window)
		self.sw.pack()

		# Buttons
		tk.Button(self.window,text='Start',command=self.sw.start_watch).pack(side=tk.LEFT)
		tk.Button(self.window,text='Stop',command=self.sw.stop).pack(side=tk.LEFT)
		tk.Button(self.window,text='Reset',command=self.sw.reset).pack(side=tk.LEFT)
		tk.Button(self.window,text='Exit',command=self.window.quit).pack(side=tk.LEFT)

		self.window.mainloop()


	def tearDown(self):
		"""Close the tkinter app"""
		self.window.destroy()

	def test_start(self):
		"""Test that timer starts successfully"""
		self.sw.start_watch()
		self.assertEqual(True, self.sw.running, "Must start running once start() activated")

	def test_stop(self):
		"""Test that timer stops successfully"""
		self.sw.start_watch()
		self.sw.stop()
		self.assertEqual(False, self.sw.running, "Must stop running once stop() activated")

	def test_reset_running(self):
		"""Test that timer stops on reset"""
		self.sw.start_watch()
		self.sw.reset()
		self.assertEqual(False, self.sw.running, "Must stop running once reset() activated")

	def test_reset_zero(self):
		"""Test that label reset to 0 on reset"""
		self.sw.start_watch()
		time.sleep(0.5)
		self.sw.reset()
		self.assertEqual(0, self.sw.lapsed_time, "Elapsed time must reset to 0 once reset() activated")


if __name__ == '__main__':
	unittest.main()