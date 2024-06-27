# iOS-Locations-Parser
iOS device locations as of 2023-03-23 (OUTDATED as of Google Earth changes)
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
