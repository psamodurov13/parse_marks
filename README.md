# Collect product ratings and upload to Google Sheets

The program collects product ratings, the number of each rating. Collection perfomed twice a day (morning and evening). This information is recorded in Google Sheet. In the evening, a line is also formed with the difference between the morning and evening values (that is, the number of new ratings is counted).

### To run the program with a timeout, run the main.py file

### Also, to run the program separately in the morning and in the evening, you can write the following lines in crontab on your server:

0 9 * * * python3 /home/user/python/parse-marks/morn.py

0 21 * * * python3 /home/user/python/parse-marks/eve.py

where /home/user/python/parse-marks/ is the path to the folder on the server, and 9 and 21 are the script execution hours
