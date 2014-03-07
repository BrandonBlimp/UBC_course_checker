import time
from datetime import datetime
import urllib2
import re
import sys

def searchBetween(sb, sa):
	try:
		stringBefore = re.escape(sb)
		stringAfter = re.escape(sa)
		searchString = stringBefore + "(.+?)" + stringAfter
		return re.search(searchString, response).group(1)
	except AttributeError:
		# if not found in string
		print "something went wrong!"
		sys.exit()

def getURLInput():
	# wait for user to type URL
	input = raw_input("To select an option, type the corresponding number and press enter. \n"
					"Alternatively, you can type the URL of the section of the course you want. \n"
					"\t1: check spaces for CPSC 304\n"
					"\t2: check spaces for MATH 221\n")
	# CPSC 304
	if input == "1":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=CPSC&course=304&section=911")
	# MATH 221
	elif input == "2":
		req = urllib2.Request("https://courses.students.ubc.ca/cs/main?pname=subjarea&tname=subjareas&req=5&dept=MATH&course=221&section=921")
	else:
		try:
			req = urllib2.Request(input)
		# if not valid URL
		except ValueError:
			print "That wasn't a valid URL. What are you doing with your life?"
			getURLInput()
	return req

while True:
	now = datetime.now()
	# prints the time the line was printed
	# print "This line was printed on %s/%s/%s at %s:%s" % (now.year, now.month, now.day, now.hour, now.minute)
	response = urllib2.urlopen(getURLInput())
	response = response.read()
	
	# Look for relevant info
	seatsRemaining = searchBetween('Total Seats Remaining:</td><td align=left><strong>', '</strong></td>')
	course = searchBetween("<h4>", "</h4>")
	
	print "there are %s seats remaining in %s on %s/%s/%s at %s:%s" % (seatsRemaining, course, now.year, now.month, now.day, now.hour, now.minute)

	
	time.sleep(1000)