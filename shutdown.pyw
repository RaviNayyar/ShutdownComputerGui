from datetime import datetime
from time import sleep
import os
import sys
import tkinter as tk
from tkinter import *
import tkinter
from threading import Thread
import threading



error_color = "red"
success_color = "green"
foreground_color = "yellow"
background_color = "black"


class Shutdown_Computer():
	def __init__(self):
		self.window = tk.Tk()
		self.window.resizable(False, False)

		self.window.title('Shutdown')
		self.frame1 = tkinter.Frame(self.window, borderwidth=2, relief='ridge')
		self.frame2 = tkinter.Frame(self.window, borderwidth=2, relief='ridge')
		self.frame3 = tkinter.Frame(self.window, borderwidth=2, relief='ridge')

		self.frame1.grid(column=0, row=0, sticky="nsew")
		self.frame2.grid(column=0, row=1, sticky="nsew")
		self.frame3.grid(column=0, row=2, sticky="nsew")
		
		year_label = tk.Label(self.frame1, text="Year")
		self.year_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		month_label = tk.Label(self.frame1, text="Month")
		self.month_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		day_label = tk.Label(self.frame1, text="Day")
		self.day_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		hour_label = tk.Label(self.frame1, text="Hour")
		self.hour_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		minute_label = tk.Label(self.frame1, text="Minute")
		self.minute_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		second_label = tk.Label(self.frame1, text="Second")
		self.second_entry = tk.Entry(self.frame1, fg=foreground_color, bg=background_color, width=5)

		empty_label = tk.Label(self.frame1, text="")

		
		month_label.grid(row=0, column=0)
		self.month_entry.grid(row=0, column=1)

		day_label.grid(row=0, column=2)
		self.day_entry.grid(row=0, column=3)

		year_label.grid(row=0, column=4)
		self.year_entry.grid(row=0, column=5)


		today_button_label = tk.Label(self.frame1, text=" ")
		today_button_label.grid(row=0, column=6)

		self.today_button = tk.Button(self.frame1, 
		    text="Today", bg=background_color, fg=foreground_color,
		    width=6, command=self.Today
		)

		self.today_button.grid(row=0, column=7)


		hour_label.grid(row=2, column=0)
		self.hour_entry.grid(row=2, column=1)

		minute_label.grid(row=2, column=2)
		self.minute_entry.grid(row=2, column=3)

		second_label.grid(row=2, column=4)
		self.second_entry.grid(row=2, column=5)

		clear_button_label = tk.Label(self.frame1, text=" ")
		clear_button_label.grid(row=0, column=6)

		self.clear_button = tk.Button(self.frame1, 
		    text=" Clear", bg=background_color, fg=foreground_color,
		    width=6, command=self.Clear
		)

		self.clear_button.grid(row=2, column=7)


		self.shutdown_button = tk.Button(self.frame3, 
		    text="Shutdown", width=41,
		    bg=background_color, fg=foreground_color,
		    command=self.Return
		)

		self.shutdown_button.grid(row=4, column=0)

		self.text = tk.StringVar()
		self.text.set("")
		self.feedback_label = tk.Label(self.frame2, textvariable=self.text)
		self.feedback_label.grid(row=0, column=0)

		self.window.mainloop()

	
	def Return(self):
		year = self.year_entry.get()
		month = self.month_entry.get()
		day = self.day_entry.get()
		hour = self.hour_entry.get()
		minute = self.minute_entry.get()
		second = self.second_entry.get()
		self.parse_cmdline(year, month, day, hour, minute, second)
	

	def Today(self):
		today = datetime.today()
		
		#Preventing insertion of multiple entries if current date already set		
		month, day, year = self.month_entry.get(), self.day_entry.get(), self.year_entry.get()
		if month == str(today.month) and day == str(today.day) and year == str(today.year):
			return

		self.month_entry.insert(0, today.month)
		self.day_entry.insert(0, today.day)
		self.year_entry.insert(0, today.year)
		print(year, month, day)


	def Clear(self):
		self.month_entry.delete(0, 'end')
		self.day_entry.delete(0, 'end')
		self.year_entry.delete(0, 'end')
		self.hour_entry.delete(0, 'end')
		self.minute_entry.delete(0, 'end')
		self.second_entry.delete(0, 'end')
		self.set_feedback_label("", color=background_color)
		self.find_difference()


	def parse_cmdline(self, year, month, day, hour, minute, second):
		if not (year.isnumeric() and month.isnumeric() and day.isnumeric() and \
			hour.isnumeric() and minute.isnumeric() and second.isnumeric()):
			self.set_feedback_label("User Entries Are Not All Numerical Values", color=error_color)
			return

		year = int(year)

		month = int(month)
		if not (month >= 1 and month <= 12):
			self.set_feedback_label("Month Entry is Invalid", color=error_color)
			return

		days_per_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
		max_day = days_per_month[month]

		day = int(day)
		if not (day >= 1 and day <=max_day):
			self.set_feedback_label("Day Entry is Invalid", color=error_color)
			return

		hour = int(hour)
		if not (hour >= 0 and hour <=23):
			self.set_feedback_label("Hour Entry is Invalid", color=error_color)
			return

		minute = int(minute)
		if not (minute >= 0 and minute <=60):
			self.set_feedback_label("Minute Entry is Invalid", color=error_color)
			return

		second = int(second)
		if not (second >= 0 and second <=60):
			self.set_feedback_label("Second Entry is Invalid", color=error_color)
			return
		
		microsecond = 000000
		shutdown_datetime = datetime(year, month, day, hour, minute, second, microsecond)
		
		current_datetime = datetime.now()

		if current_datetime >= shutdown_datetime:
			self.set_feedback_label("Shutdown Time is Before the Current Time", color=error_color)
			return

		time_disp = str(month)+"/"+str(day)+"/"+str(year)+" "+str(hour)+":"+str(minute) 
		self.set_feedback_label("Shutdown Time: "+time_disp, color=success_color)
		shutdown_check_thread = Thread(target = self.shutdown_check, args = (shutdown_datetime, ))
		differnce_check_thread = Thread(target = self.find_difference, args = (shutdown_datetime, time_disp, ))
		shutdown_check_thread.daemon = True
		differnce_check_thread.daemon = True

		shutdown_check_thread.start()
		differnce_check_thread.start()


	def find_difference(self, shutdown_datetime, time_disp):
		current_datetime = datetime.now()

		while True:
			sleep(1)
		
			current_datetime = datetime.now()

			difference = shutdown_datetime - current_datetime 
			label_str = "Shutdown Time: " + time_disp + "    |    " + str(difference)
			
			self.set_feedback_label(label_str, color=success_color)


	def set_feedback_label(self, msg, color):
		self.text.set(msg)
		self.feedback_label.configure(foreground=color)


	def shutdown_check(self, shutdown_datetime):
		current_datetime = datetime.now()
		while True:
			sleep(1)
			if current_datetime >= shutdown_datetime:
				os.system("powershell Stop-Computer")
			
			current_datetime = datetime.now()


Shutdown_Computer()  
