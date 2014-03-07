import time
from datetime import datetime
import urllib2
import re
import sys

def searchBetween(sb, sa, html):
	try:
		stringBefore = re.escape(sb)
		stringAfter = re.escape(sa)
		searchString = stringBefore + "(.+?)" + stringAfter
		return re.search(searchString, html).group(1)
	except AttributeError:
		# if not found in string
		print "something went wrong!"

def getHTML(input):
	# CPSC 304
	if input == "1":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=CPSC&course=304&section=911")
	# MATH 221
	elif input == "2":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=221&section=921")
	else:
		req = urllib2.Request(input)
	
	# let's check
	try:
		response = urllib2.urlopen(req)
	except ValueError:
		print "That isn't a valid URL. What are you doing with your life? Let's try this again. \n \n \n"
		getHTML(input)
	return response.read()

input = raw_input("To select an option, type the corresponding number and press enter. \n"
				"Alternatively, you can type the URL of the section of the course you want. \n"
				"\t1: check spaces for CPSC 304\n"
				"\t2: check spaces for MATH 221\n")
	
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
	
	time.sleep(2)