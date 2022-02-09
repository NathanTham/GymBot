#pyinstaller .\GymBot.py -F
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import numpy as np

login_url = "https://iac01.ucalgary.ca/CamRecWebBooking/Login.aspx"
default_url = "https://iac01.ucalgary.ca/CamRecWebBooking/Login.aspx"

def login(username, password): #Returns True if successful, else returns False
    un_field = driver.find_element('id', "ctl00_ContentPlaceHolder1_logCamRec_UserName")
    pw_field = driver.find_element('id', "ctl00_ContentPlaceHolder1_logCamRec_Password")
    login_btn = driver.find_element('id', "ctl00_ContentPlaceHolder1_logCamRec_LoginButton")
    un_field.send_keys(username)
    pw_field.send_keys(password)
    login_btn.click()

    status = login_status()
    if status == True:
        print("Logged in")
    else:
        print("Could not log in")
    return status

def login_status():  #returns True if logged in, False if logged out
    status = driver.find_element('id', "ctl00_hyLogin")
    if status.text == "LOGOUT":
        return True
    if status.text == "LOGIN":
        return False

def logout():
    logout_btn = driver.find_element('id', "ctl00_hyLogin")
    if login_status() == True:
        logout_btn.click()
        print("Logged out")
    if login_status() == False:
        print("Already logged out")
    return

print("Ensure you do not currently have a booking. Apointments will be booked day-of only.")

#Check validity of input time
valid_time = False
while valid_time == False:
    time_input = input("Input 2-digit 24hr number of desired appointment start time (i.e., 09, 13, 18):")
    if time_input not in ['06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']:
        print("Invalid input (hint: use 2 digits, i.e., 09)")
        print()
    else:
        valid_time = True

desired_time = time_input + ":00 to " + str(int(time_input)+1) + ":00"
#desired_date = input("Input desired date (i.e., January 28):")
nums = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15']
time_available = False

#Define webdriver
ser = Service("C:/Users/Lukas Morrison/OneDrive - University of Calgary/chromedriver.exe")
op = webdriver.ChromeOptions()
op.add_argument("--headless")
op.add_argument('--log-level=3')
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(service=ser, options=op)

driver.get(default_url)
creds_good = False
while creds_good == False:  #check credentials
    username = input("Input your username:")
    password = input("Input your password:")
    login(username, password)
    if login_status() == True:
        creds_good = True
    else:
        print("Invalid credentials try again")
        print()

while time_available == False:  #main loop
    #Refresh / login if timed out
    logged_in = login_status()
    if logged_in:
        driver.refresh()
    else:
        driver.get(login_url)
        login(username, password)

    #Get available slots / Check if desired slot is available
    slots_array = []
    for i in range(16):
        try:
            slot_id = "ctl00_ContentPlaceHolder1_ctl00_repAvailFitness_ctl" + nums[i] + "_lnkBtnFitness"
            time_slot = driver.find_element('id', slot_id)
            text = time_slot.text
            slots_array.append(text)
            if desired_time in slots_array[i]:
                time_available = True
                print(text)
                break
        except:
            pass
    if time_available == False:
        print('not available - trying again')

#Check for an existing booking - do later

#Book desired time slot
if time_available == True:
    slot = driver.find_element('id', slot_id)
    slot.click()
    print("Booked")

driver.quit()