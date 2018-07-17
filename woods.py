import os
import time
import RPi.GPIO as GPIO
import glob
import tkinter as tk
import json
import sys
import time
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#JSON file name
GDOCS_OAUTH_JSON       = 'WoodsTemp1-06b290b754ae.json'

# Google Docs spreadsheet name.
GDOCS_SPREADSHEET_NAME = 'WoodsTemp1'

global worksheet
worksheet = None
def login_open_sheet(oauth_key_file, spreadsheet):
    
    """Connect to Google Docs spreadsheet and return the first worksheet."""
    try:
        scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(oauth_key_file, scope)
        gc = gspread.authorize(credentials)
        worksheet = gc.open('WoodsTemp1').sheet1
        return worksheet
        print("succesfully logged in!")
    except Exception as ex:
        print('Unable to login and get spreadsheet.  Check OAuth credentials, spreadsheet name, and make sure spreadsheet is shared to the client_email address in the OAuth .json file!')
        print('Google sheet login failed with error:', ex)
        sys.exit(1)

root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
global finalTemp
finalTemp = 85
global lastSet
lastSet = 0
def raisetemp():
        global finalTemp
        global lastSet
        lastSet = finalTemp
        finalTemp += 1
        print ("Set temperature to:",finalTemp, "lastSet:", lastSet)
def lowertemp():
        global finalTemp
        global lastSet
        lastSet = finalTemp
        finalTemp -= 1
        print ("Set temperature to:",finalTemp, "lastSet:", lastSet)
up = tk.Button(frame,
        font = ("Courier", 30),
        height = 7,
        width = 10,
        text="+1F", 
        fg="red",
        command=raisetemp)
up.pack(side=tk.LEFT)
down = tk.Button(frame,
        font =  ("Courier", 30),
        height = 7,
        width = 10,
        text="-1F",
        fg="blue",
        command=lowertemp)
down.pack(side=tk.LEFT)

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#temp_sensor = 'sys/bus/w1/devices/28-0417710b11ff/w1_slave'

        
def readtemp():

        tfile = open("/sys/bus/w1/devices/28-0417710b11ff/w1_slave") 
        text = tfile.read() 
        tfile.close() 
        secondline = text.split("\n")[1] 
        temperaturedata = secondline.split(" ")[9] 
        temperature = float(temperaturedata[2:]) 
        temperaturec = temperature / 1000
        temperaturef = temperaturec * 1.8 + 32
        temp = round(temperaturef, 3)
        return temp;

global a
a = 27
global b
b = 22
global c
c = 17
global counter
counter = 0
global count
count = 1
global lastTemp
lastTemp = 0
def change():
        global a
        global b
        global c
        global count
        if count == 1:
                count = 2
        elif count == 2:
                count = 3
        elif count == 3:
                count = 1
        if count == 1:
                a = 27
                b = 22
                c = 17
        if count == 2:
                a = 17
                b = 27
                c = 22
        if count == 3:
                a = 22
                b = 17
                c = 27
        print ("a=", a, "b=", b, "c=", c);


def main():
        global worksheet
        if worksheet is None:
            worksheet = login_open_sheet(GDOCS_OAUTH_JSON, GDOCS_SPREADSHEET_NAME);
        temperature = readtemp()
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(17,GPIO.OUT)
        GPIO.setup(27,GPIO.OUT)
        GPIO.setup(22,GPIO.OUT)
        global lastTemp
        global lastSet
        global a
        global b
        global c

        # Append the data in the spreadsheet, including a timestamp
        try:
            worksheet.append_row([datetime.datetime.now().strftime("%y-%m-%d-%H-%M"), temperature])
        except:
            worksheet = None
            print("logging in again");
        print ("current temperature is:", temperature, "lastTemp:", lastTemp)
        if temperature <= lastTemp -2 or temperature >= lastTemp +2 or lastSet != finalTemp:
                print ("thonk")
                lastSet = finalTemp
                if temperature <= finalTemp -9:
                        lastTemp = temperature
                        GPIO.output(a,0)
                        GPIO.output(b,0)
                        GPIO.output(c,0)
                        change()
                elif temperature <= finalTemp - 6:
                        lastTemp = temperature
                        GPIO.output(a,0)
                        GPIO.output(b,0)
                        GPIO.output(c,1)
                        change()
                elif temperature <= finalTemp -3:
                        lastTemp = temperature
                        GPIO.output(a,0)
                        GPIO.output(b,1)
                        GPIO.output(c,1)
                        change()
                if temperature >= finalTemp:
                        lastTemp = temperature
                        GPIO.output(a,1)
                        GPIO.output(b,1)
                        GPIO.output(c,1)
                        change();

                

        root.after(3000, main)
root.after(3000, main)
root.mainloop()
