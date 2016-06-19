#!/usr/bin/python

"""
Author: Christopher Ellis
Version: 1.0

This is a simple script to process participant data from FNIR brain scanning
studies.

If you use and/or modify this script for your own research please acknowledge:
christopher.ellis@nottingham.ac.uk 

"""

import glob, re, os, csv
from os import chdir

print __doc__

#Read in particpants path and file type and calculate output variables
print 'Please enter the path to your FNIR participant files and a keyphrase used in\nyour filenames to identify the file type e.g. "/Users/john/participantData oxy".\n'
path, fileFormat = raw_input().split()
dataFrames = {}

#Change to working directory supplied by user
chdir(path)
outputFileName = os.path.relpath(".","..")

#Setup output file
with open(outputFileName + '.csv', 'wb') as output:
	outwriter=csv.writer(output, delimiter=',')

	#Process participant files
	for file in glob.glob("*."+ fileFormat + ".*"):
	    filename = os.path.splitext(file)[0];
	    outwriter.writerow([filename])
	    outwriter.writerow([])	    

	    with open(file, 'rb') as participantCSVFile:
	        reader = csv.reader(participantCSVFile)
	       
	        #Get intervals from first row
	        intervals = map(float, filter(None, reader.next()[1:]))
	        intervalsLen = len(intervals)
	        
	        #Get header values
	        fileHeaders = reader.next()
	        fileHeaders[0] = 'Intervals'
	        
	        #Calculate actual values and +5sec and -10sec interval values
	        actualValues, plus5AveragedResults, minus10AveragedResults, plus5intervals, minus10intervals = ([] for x in range(5))
	        for i in range(intervalsLen):
	        	for row in reader:
	        		if float(row[0]) >= intervals[i]:
	        			actualValues.append(row)
	        			plus5intervals.append(float(row[0]) + 5)
	        			minus10intervals.append(float(row[0]) -10)
	        			participantCSVFile.seek(0)
	        			reader.next()
	        			reader.next()
	        			break

	        #Get +5sec and -10sec rows
	        plus5Total, plus5Count, minus10Total, minus10Count = ([] for x in range(4))
	        for i in range(intervalsLen):
	        	participantCSVFile.seek(0)
	        	reader.next()
	        	reader.next()
	        	plus5row =  [float(0) for x in range(len(fileHeaders))]
	        	minus10row = [float(0) for x in range(len(fileHeaders))]
	        	rowCount5sec, rowCount10sec = 0,0
	        	for row in reader:
	        		if float(row[0]) >= intervals[i] and float(row[0]) <= plus5intervals[i]:
	        			rowCount5sec += 1
	        			plus5row = [sum(x) for x in zip(plus5row, [float(y) for y in row])]
	        		if float(row[0]) >= minus10intervals[i] and float(row[0]) <= plus5intervals[i]:
	        			rowCount10sec += 1
	        			minus10row = [sum(x) for x in zip(minus10row, [float(y) for y in row])]

	        	plus5Count.append(rowCount5sec)
	        	minus10Count.append(rowCount10sec)
	        	plus5Total.append(plus5row)
	        	minus10Total.append(minus10row)

	        #Calculated averages between actual and +5sec value and between interval -10sec and interval +5sec
	        for i in range(len(actualValues)):
	        	plus5AveragedResults.append([x / plus5Count[i] for x in plus5Total[i]])
	        	minus10AveragedResults.append([x / minus10Count[i] for x in minus10Total[i]])
	    

	    #Output processed data
	    outwriter.writerow(['Actual Values'])
	    outwriter.writerow(fileHeaders)
	    for row in actualValues:
	    	outwriter.writerow(row)

	    outwriter.writerow([])
	    outwriter.writerow([])
	    outwriter.writerow(['5 Second Averaged Values'])
	    outwriter.writerow(fileHeaders)
	    for row in plus5AveragedResults:
	    	outwriter.writerow(row)

	    outwriter.writerow([])
	    outwriter.writerow([])
	    outwriter.writerow(['15 Second Averaged Values'])
	    outwriter.writerow(fileHeaders)
	    for row in minus10AveragedResults:
	    	outwriter.writerow(row)

	    outwriter.writerow([])
	    outwriter.writerow([])
	    outwriter.writerow([])



