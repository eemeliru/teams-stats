# Teams meeting statistics

This tool combines different Teams meeting statistics into nice looking graphs.

Requirements: 
Python (developed & tested with v.3.8.7.)  
Teams language to English

[DEMOPAGE](http://teams-stats-anon.herokuapp.com/)


### Install and user manual:  
1. Download meetingAttendance reports from meeting's chat
2. Move those reports to /attendanceReports -folder
3. Run with console: ``pip install -r requirements.txt``
4. Run CSV2XLSXrunner.py: this modifies attendanceReports - pseudo-csv's to .xlsx -format
5. Run ExcelCombiner.py: this performs preprocessing to reports and combines them to one .csv -file
   1. (Here you can anonymize the dataset with the anonGen.py)
6. Run app.py: and open 127.0.0.1:8050 -> you now have Dash server, where you can see the stats. Iff you want local .html -file, press the Download HTML -button located in bottom-left corner of the page.

Enjoy :)
