# THIS SCRIPT WILL EXECUTE THE QUEIRIES BELOW TO PARSE OUT DATA FOR THE SELECTED APPLICATION.
# APPLICATION: iOS device locations as of 2023-03-23
# DATABASES REQUIRED: Cache.sqlite
#
#       \private\var\mobile\Library\Caches\com.apple.routined\
#           Cache.sqlite
#
# Version 1.0
# Date  2023-03-23
# Copyright (C) 2023 - Aaron Dee Roberts
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You can view the GNU General Public License at <http://www.gnu.org/licenses/>
#
# UTC QUERY USED
# SELECT "<Placemark><name>" || DATETIME(ZTIMESTAMP + 978307200, 'unixepoch') || "  UTC  (" || SUBSTR(ZHORIZONTALACCURACY, 1, 7) || " Meters)</name><description><![CDATA[<p>" || DATETIME(ZTIMESTAMP + 978307200, 'unixepoch') || "</p>]]></description><TimeStamp><when>" || SUBSTR(DATETIME(ZTIMESTAMP + 978307200, 'unixepoch'), 1, 10) || "T" || SUBSTR(DATETIME(ZTIMESTAMP + 978307200, 'unixepoch'), 12, 8) || "</when></TimeStamp><Point><altitudeMode>clampedToGround</altitudeMode><coordinates>" || ZLONGITUDE || ", " || ZLATITUDE || "</coordinates></Point></Placemark>" AS placemark, ZTIMESTAMP, ZLONGITUDE, ZLATITUDE, ZALTITUDE, ZHORIZONTALACCURACY
# FROM ZRTCLLOCATIONMO WHERE ZHORIZONTALACCURACY < 200 ORDER BY ZTIMESTAMP
#
# HEADER AND FOOTER OF KML FILE
# <?xml version="1.0" encoding="utf-8"?>
# <kml xmlns:gx="http://www.google.com/kml/ext/2.2" xmlns="http://www.opengis.net/kml/2.2">
# <Document>
#
# </Document>
# </kml>


import sys
import os
import datetime

# PRE SETTING A FEW VARIABLES
isError = 0 # Allows for determining when to exit a while loop
response = "" # Basic input response
zone_dic = {} #dictionary to house timezone response. 


# LIST THE FUNCTONS FOR REPEATED USE

# FUNCTION FOR RETURNING MAC ABSOLUTE TIME FROM FORMATTED DATE TIME OR JUST DATE
def datetime_to_mac(timestamp, isEnd = 0):
	# Requires import datetime, import time
	# Returns "INVALID" if the format is incorrect.
	
	date_time = timestamp
	epoch_start = datetime.datetime(2001, 1, 1, 0, 0, 0) # SET THE EPOCH FOR MAC ABSOLUTE
	try:
		x = " " in date_time
		if x == True:
			split_date_time = date_time.split(" ")
		else:
			split_date_time = [date_time,'00:00:00']

		# USING THIS TO ACCOINT FOR "/" USED IN DATES INSTEAD OF "-"
		x = "-" in split_date_time[0]
		if x == True:
			split_date = split_date_time[0].split("-")
		elif x == False:
			split_date = split_date_time[0].split("/")
		# ACCOUNT FOR NO TIME ADDED AND IF IT'S FROM THE START OR END (isEnd)
		if split_date_time[1] != '00:00:00':
			split_time = split_date_time[1].split(":")
		else:
			if isEnd == 1:
				split_time = ['23','59','59']
			else:
				split_time = ['00','00','00']

		isEnd = 0
		date_time_comb = split_date + split_time
		date_time = ""
		intYear = int(date_time_comb[0])
		intMonth = int(date_time_comb[1])
		intDay = int(date_time_comb[2])
		intHour = int(date_time_comb[3])
		intMinute = int(date_time_comb[4])
		intSecond = int(date_time_comb[5])

		# assigned regular string date
		date_time = datetime.datetime(intYear, intMonth, intDay, intHour, intMinute, intSecond)
		time_diff = (date_time - epoch_start)
		time_return_utc = time_diff.total_seconds()
		return str(time_return_utc)
		
	except:
		 print(f'Invalid format entered. {date_time} is not the proper format for the date time and will cause an error.')
		 return 'INVALID'

def list_timezones(): # Here to later list the timezones when selecting and re-list when an invalid one used.
	print('          UTC - Universal Time Coordinated')
	print('          EST - Eastern Standard Time (UTC-5), Daylight Savings (UTC-4)')
	print('          CST - Central Standard Time (UTC-6), Daylight Savings (UTC-5)')
	print('          MST - Mountain Standard Time (UTC-7), Daylight Savings (UTC-6)')
	print('          PST - Pacific Standard Time (UTC-8), Daylight Savings (UTC-7)')
	print()


# PROMPT TO INFORM WHAT DATABASES ARE NEEDED AND ASK TO PROCEED OR ABORT
print()
print("This program requires the following database files in the current folder to proceed.")
print("If you don't have them press \"N\" to exit or any other key to proceed.")
print("DATABASE:  Cache.sqlite")
print('LOCATION: \\private\\var\\mobile\\Library\\Caches\\com.apple.routined\\')
print()
response = input("INPUT:  ")
if response == "N" or response == "n":
    print('"N" selected, aborting')
    sys.exit(0)

response = "" #RESET THE RESPONSE

print()
print("Provide the path to the database including the file including the file name.")
print("EXAMPLE: C:\\WORK\\Cache.sqlite.")
print("If nothing is entered, the default is \"Cache.sqlite\" in the current location.")
print()
file_path = input("INPUT:  ")
print()

if file_path == "N" or file_path == "n":
    print('"N" selected, aborting')
    sys.exit(0)
elif file_path =="":
    file_path = "Cache.sqlite"
else:
    print(f"{file_path} is being used.")

# CHECK TO SEE IF THE FILE EXISTS
print(f'Checking to see if {file_path} exists.')
if os.path.isfile(file_path) is True:
    print(f'{file_path} does exist so we are proceeding.')
else:
    print(f'{file_path} does not appear to exist.  Aborting.')
    print()
    sys.exit(0)

# ESTABLISHING THE HIGHEST DISTANCE RANGE (IN METERS)
print()
print("What do you want your accuracy cutoff to be?")
print("Example would be 200 for all locations with accuracy below 200 meters.")
print("200 meters is the default and will be used if nothing is entered.")
print()
acc_cutoff = input("INPUT:  ")
if acc_cutoff == "":
    acc_cutoff = "200"
print()

# SETTING UP THE RANGE OF TIME
print()
print('You can select a time range for your results.')
print('Selecting nothing will default to the earliest and/or latest.')
print('The date alone can be used and the time will default to \"00:00:00\".')
print('If no time value is entered on the end date it will default to 23:59:59. ')
print('This means it will include the full day.')
print('The format for the date is \"YYYY-MM-DD HH:MM:SS\" in UTC.')
print('    EXAMPLE: \"2023-03-13 02:12:56\"  or  \"2023-03-13\"   or   \"2023-3-13\"')
print()


# SET THE START TIME
start_timestamp = 'INVALID'
while start_timestamp == 'INVALID':
	start_time = input('INPUT START TIME:   ')

	if start_time == "":
		start_time = '2001-01-01 00:00:00'

	start_timestamp = datetime_to_mac(start_time,0)

# SET THE END TIME
end_timestamp = 'INVALID'
while end_timestamp 	== 'INVALID':
	end_time = input('INPUT END TIME:   ')
	
	if end_time =="":
		end_time = '2400-01-01 00:00:00' # Just in time for Buck Rogers' return to earth

	end_timestamp = datetime_to_mac(end_time,1)
print()

buck_addon = ""
mac_addon = ""
if end_time == '2400-01-01 00:00:00':
	buck_addon = ' - Just in time for Captain William Anthony Roger\'s return to earth'
if start_time == '2001-01-01 00:00:00':
	mac_addon = ' - Beginning of Mac Absolute time.'
	
print(f'Start Time:  {start_time}{mac_addon}')
print(f'End Time:    {end_time}{buck_addon}')
print()

#SETTING UP THE TIME ZONE DICTIONARY
time_zones = {
    'UTC':{'UTC':'-0'},
    'EST':{'UTC':'-0','EST':'-18000','EDT':'-14400'}, # -5, -4
    'CST':{'UTC':'-0','CST':'-21600','CDT':'-18000'}, # -6, -5
    'MST':{'UTC':'-0','MST':'-25200','MDT':'-21600'}, # -7, -6
    'PST':{'UTC':'-0','PST':'-28800','PDT':'-25200'} # -8, -7
}


# GETTING THE DESIRED TIME ZONE SET
print('Select the timezone you want to adjust for.')
print('Using UTC will ONLY output UTC.')
print('Selecting any other timezone will output 3 files:')
print('     UTC Times, Timezone STANDARD times, and Timezone DAYLIGHT SAVINGS times')
print('     Allowed entries (Just the 3 letter prefix:')

list_timezones() # Call the timezone list
print()


# SETTING THE DICTIONARY FOR THE SELECTED TIME ZONES

isError = 1 # Set the error so it will only exit the loop upon clearing the error...choosing a correct timezone.

while isError == 1:
	zone_select = input('INPUT:  ').upper()

	if zone_select == "" or zone_select == None:
		zone_select = "UTC"
		zone_dic = time_zones[zone_select]
		isError = 0
	else:
		try:
			zone_dic = time_zones[zone_select]
			isError = 0
		except KeyError: #Accounting for mistyping or improper entries
			print('Invalid zone entered.  Use one in the list or ENTER for the default UTC.')
			list_timezones()

# SETTING UP LOGGING TO BE ABLE TO LOG ACTIONS
import logging
level    = logging.INFO
format   = '%(message)s'
log_file = "iOS_device_locations_parser.log"
handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)

#GET DATE AND TIME FOR LOGGING

now = datetime.datetime.now()
# USAGE: # print (now.strftime("%Y-%m-%d %H:%M:%S LT"))

# START THE LOGGING OF THE EVENTS FOR THE LOG FILE
print(f'Starting the log file {log_file}') 

logging.info("=====================================================================================")
logging.info("============================== LOG FILE =============================================")
logging.info("=====================================================================================")
logging.info(f'Starting log for parsing of file {file_path} parsing.')
logging.info(now.strftime('Time started:  %Y-%m-%d %H:%M:%S LT'))
logging.info('')
logging.info('Parameters chosen:')
if start_time == '2001-01-01 00:00:00':
	start_time = '2001-01-01 00:00:00 (Default earliest)'
if end_time == '2400-01-01 00:00:00':
	end_time = '2400-01-01 00:00:00 (Default latest)'
logging.info(f'       Timezone: {zone_select},  Accuracy: < {acc_cutoff}')
logging.info(f'       Starting Time: {start_time},  Ending Time: {end_time}')
logging.info('')

import sqlite3
con = sqlite3.connect('Cache.sqlite')

files_written = [] # Set space to write list of files written to

for time_zone_label, time_zone_offset in zone_dic.items(): # Put the dictionary items into the variables and loop through each item.
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    sqlite_query_utc = f"""SELECT "<Placemark><name>" || DATETIME(ZTIMESTAMP + 978307200{time_zone_offset}, 'unixepoch') || "  {time_zone_label}  (" \
    || SUBSTR(ZHORIZONTALACCURACY, 1, 7) || " Meters)</name><description><![CDATA[<p>" || \
    DATETIME(ZTIMESTAMP + 978307200{time_zone_offset}, 'unixepoch') || "</p>]]></description><TimeStamp><when>" || \
    SUBSTR(DATETIME(ZTIMESTAMP + 978307200{time_zone_offset}, 'unixepoch'), 1, 10) || "T" || \
    SUBSTR(DATETIME(ZTIMESTAMP + 978307200{time_zone_offset}, 'unixepoch'), 12, 8) || \
    "</when></TimeStamp><Point><altitudeMode>clampedToGround</altitudeMode><coordinates>" \
    || ZLONGITUDE || ", " || ZLATITUDE || "</coordinates></Point></Placemark>" AS placemark, \
    ZTIMESTAMP, ZLONGITUDE, ZLATITUDE, ZALTITUDE, ZHORIZONTALACCURACY
    FROM ZRTCLLOCATIONMO \
    WHERE ZHORIZONTALACCURACY < {acc_cutoff} \
    AND ZTIMESTAMP BETWEEN {start_timestamp} AND {end_timestamp} \
    ORDER BY \
    ZTIMESTAMP"""

    logging.info("Query being used:")
    logging.info(f"{sqlite_query_utc}")
    logging.info("")

    # EXECUTE THE QUERY
    cur.execute(sqlite_query_utc)
    records = cur.fetchall()
    logging.info("Successful query")
    logging.info('')

    # LOGGING THE TOTAL NUMBER OF RECORDS RETURNED
    num_records = str(len(records))
    logging.info(f'Total rows in return: {num_records}')

    out_file = f'iOS_device_locations_{time_zone_label}.kml'
    files_written.append(out_file)
    file2write = open(out_file,'w')
    file2write.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
    file2write.write("<kml xmlns:gx=\"http://www.google.com/kml/ext/2.2\" xmlns=\"http://www.opengis.net/kml/2.2\">\n")
    file2write.write("<Document>\n")
    for row in records:
        file2write.write(row[0] + "\n")

    file2write.write("</Document>\n")
    file2write.write("</kml>")
    file2write.close()
    logging.info(f'File kml data written to: {out_file}')
    logging.info('Contents include the header, first column of the query return, and footer.')
    logging.info('')

print('If you got this far with no errors, everything probably worked fine.')
print('Files written: ')
print('       iOS_device_locations_parser.log')
for files_written_for in files_written:
	print(f'       {files_written_for}')
	
print()
