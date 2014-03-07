#! /usr/local/bin/python
import time
from datetime import datetime
import urllib2
import re
import sys
import os

# email stuff
SMTPserver = 'smtp.att.yahoo.com'
sender =     "b_loong5@yahoo.com"
destination = ['6043633029@msg.telus.com']
USERNAME = "b_loong5@yahoo.com"
PASSWORD = "29083ragnarok"
text_subtype = 'plain'
subject=""

# get URL input from user
input = raw_input("To select an option, type the corresponding number and press enter. \n"
					"Alternatively, you can type the URL of the section of the course you want. \n"
					"\t1: check spaces for CPSC 304\n"
					"\t2: check spaces for MATH 221\n"
					"\t3: check spaces for MATH 200\n"
					"\t4: EXPERIMENTAL (kind of)\n")

def searchBetween(sb, sa, html):
	try:
		stringBefore = re.escape(sb)
		stringAfter = re.escape(sa)
		searchString = stringBefore + "(.+?)" + stringAfter
		return re.search(searchString, html).group(1)
	except AttributeError:
		# if not found in string
		print "something went wrong!"

def getHTML(input_arg):
	global input
	# CPSC 304
	if input_arg == "1":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=CPSC&course=304&section=911")
	# MATH 221
	elif input_arg == "2":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=221&section=921")
	elif input_arg == "3":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=200&section=921")
	elif input_arg == "4":
		dept = raw_input("Now type the department code (example: CPSC) and MAKE SURE IT'S ALL CAPS: ")
		courseNumber = raw_input("Now type the course number: ")
		section = raw_input("Now type the section number: ")
		input = "https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=" + dept + "&course=" + courseNumber + "&section=" + section
		req = urllib2.Request(input)
	else:
		req = urllib2.Request(input_arg)
	
	# let's check
	try:
		response = urllib2.urlopen(req)
	except ValueError:
		global input
		input = raw_input("That isn't a valid URL. What are you doing with your life? \n")
		return getHTML(input)
	return response.read()

def sendMessage(course):
	from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
	# from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
	from email.MIMEText import MIMEText
	
	content = "A spot has opened up in %s. Quick, go find some wifi!" % (course)
	try:
		msg = MIMEText(content, text_subtype)
		msg['Subject']=       ""
		msg['From']   = "UBC_course_tester" # some SMTP servers will do this automatically, not all

		conn = SMTP(SMTPserver)
		conn.set_debuglevel(False)
		conn.login(USERNAME, PASSWORD)
		try:
			conn.sendmail(sender, destination, msg.as_string())
		finally:
			conn.close()

	except Exception, exc:
		sys.exit( "mail failed; %s" % str(exc) ) # give a error message
	
	
# "main" loop
while True:
	now = datetime.now()
	html = getHTML(input)
	
	# Look for relevant info
	try:
		seatsRemaining = searchBetween('Total Seats Remaining:</td><td align=left><strong>', '</strong></td>', html)
		course = searchBetween("<h4>", "</h4>", html)
		print "there are %s seats remaining in %s on %s/%s/%s at %s:%s" % (seatsRemaining, course, now.year, now.month, now.day, now.hour, now.minute)
	except AttributeError:
		print "something went wrong!"
	if int(seatsRemaining) > 0:
		sendMessage(course)
		print "a spot opened up in %s! sent a notification message" % (course)
		quit = ""
		while quit != "quit":
			global quit
			quit = raw_input("type \"quit\" to exit the program")
		sys.exit("bye")
	time.sleep(60)