import time, re, os, sys, threading, math, multiprocessing, subprocess, pymongo
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from selenium.webdriver.common.action_chains import ActionChains

# pandas setting for displaying rows and columns
pd.options.display.max_columns = 999
pd.options.display.max_rows = 999

num = os.cpu_count()
# driverPath = r'C:\Users\USER\chromedriver_win32\chromedriver.exe'
driverPath = r'C:\Users\Foreshop 6\chromedriver\chromedriver.exe'


# chrome options 
chrome_options = Options()
prefs = {
    "download.open_pdf_in_system_reader": False,
    "download.prompt_for_download": True,
    "plugins.always_open_pdf_externally": False
}
chrome_options.add_experimental_option(
    "prefs", prefs
)

chrome_options.add_argument("window-size=1200,1100");
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument(r"--user-data-dir=C:\Users\Foreshop 6\AppData\Local\Google\Chrome\User Data")
chrome_options.add_argument(r'--profile-directory=Default') 



#calculating start time
start = datetime.now()
current_time = start.strftime("%H:%M:%S")

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
# Find a workbook by name and open the first sheet
sheet = client.open("Automation - Social Media Check")
sheet = sheet.get_worksheet(1)
allRecords = sheet.get_all_records()


social_names = ['facebook', 'instagram', 'pinterest']
def removeSlash(target):
    name = target.rstrip(target[-1])
    return name

def updateCell(val, color):
    if color == 'green':
        sheet.update(val, 'V')
        sheet.format(val, {
            "backgroundColor": {
              "red":0,
              "green": 50,
              "blue": 0
            },
            "horizontalAlignment": "CENTER",
            "textFormat": {
              "foregroundColor": {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
              },
              "fontSize": 12,
              "bold": False
            }
        })
    else:
        sheet.update(val, '')
        sheet.format(val, {
            "backgroundColor": {
              "red": 20,
              "green": 0,
              "blue": 0
            },
            "horizontalAlignment": "CENTER",
            "textFormat": {
              "foregroundColor": {
                "red": 1.0,
                "green": 1.0,
                "blue": 1.0
              },
              "fontSize": 12,
              "bold": False
            }
        })
        

def explicitVisit(socialUrl, socialType):
    global boolinsta
    global boolpin
    global boolfb
    global boolinsta1
    global boolpin1
    global boolfb1

    try:
        driver.get(socialUrl)
        time.sleep(3)
        explicitSocialLink = driver.current_url
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
    except:
        print("Error in explicit domain get by driver")
        return

    if socialType == 'insta':
        boolinsta = False
        if "Sorry, this page isn't available" in str(soup):
            print("Instagram Error")
            boolinsta1 = False
        else:
            print("here 1")
            updateCell(instacellname1, 'green')
            boolinsta1 = True 
    
    elif socialType == 'pin':
        boolpin = False
        if 'show_error=true' in socialLink:
            print("error in pinterest ",socialLink)
            boolpin1 = False
            
        else:
            print("here 10")
            updateCell(pincellname1, 'green')
            boolpin1 = True
        
    elif socialType == 'fb':
        boolfb = False
        if "This Page Isn't Available" in str(soup):
            print("Facebook Error")
            boolfb1 = False
            
        else:
            print("here 11")
            updateCell(fbcellname1, 'green')
            boolfb1 = True
            
    print("quit in explicit ", i)
    return
        
    
        
for i in range(len(allRecords)):
    each = allRecords[i]
    num = i+2
    
    boolinsta = ''
    boolpin = ''
    boolfb = ''
    
    boolinsta1 = ''
    boolpin1 = ''
    boolfb1 = ''
    
    instabool = True
    pinbool = True
    fbbool = True
    
    
    driver = webdriver.Chrome(driverPath, chrome_options=chrome_options)
    domain = each["DOMAIN"]
    insta = each['Instagram']
    fb = each['Facebook']
    pin = each['Pinterest']

    
    try:
        eachDomain = "https://"+domain
        print("Visiting  >>>> ", eachDomain)
        print()
        driver.get(eachDomain)
        time.sleep(3)
    except:
        print("Error in getting domain by driver ::", eachDomain)
        driver.quit()
        continue
    
    nav = driver.find_elements_by_tag_name('nav')
    for eachNav in nav:
        divs = eachNav.find_elements(By.TAG_NAME, 'div') 
        for eachdiv in divs:
            finalDiv = eachdiv.find_elements(By.TAG_NAME, 'div')
            for eachFinalDiv in finalDiv:
                uls = eachFinalDiv.find_elements(By.TAG_NAME, 'ul')
                for eachUl in uls[1:]:
                    lis = eachUl.find_elements(By.TAG_NAME, 'li')
                    for eachli in lis[:1]:
                        allas = eachli.find_elements(By.TAG_NAME, 'a')
                        for i in range(len(allas)):
                            eachAs = allas[i]
                            
                            for social in social_names:
                                if social in eachAs.get_attribute('href'):
                                    linkDiv = eachAs.get_attribute('href')
                                    print(linkDiv)
                                    eachAs.click()  
                                    

    time.sleep(2)
    urlname = eachDomain.split("//")[1]
    name = urlname.split(".")[0]

    currentWindow = driver.current_window_handle
    print("Current window title: " + driver.title)
    print()
    chwd = driver.window_handles

    instacellname = 'D'+str(num)
    instacellname1 = 'E'+str(num)
    
    pincellname = 'G'+str(num)
    pincellname1 = 'H'+str(num)
    
    fbcellname = 'J'+str(num)
    fbcellname1 = 'K'+str(num)
    
    # #switch focus to child window
    for w in chwd:
        if(w!= currentWindow):
            driver.switch_to.window(w)
            socialLink = driver.current_url
            print("Current url : ", socialLink)
            
            if 'www' not in socialLink:
                chunks = socialLink.split("//")
                socialLink = chunks[0]+"//www."+chunks[1]
            if socialLink[-1] ==  '/':
                socialLink = removeSlash(socialLink)
            
            
            #INSTAGRAM
            if 'instagram' in  socialLink:
                instabool = False
                if socialLink in insta:
                    print("Valid instagram page link : ", socialLink, insta)
                    updateCell(instacellname, 'green')
                    boolinsta = True 
                else:
                    boolinsta = False 

                source = driver.page_source
                soup = BeautifulSoup(source, 'html.parser')
                if "Sorry, this page isn't available" in str(soup):
                    print("Instagram Error")
                    boolinsta1 = False 
                else:
                    updateCell(instacellname1, 'green')
                    boolinsta1 = True 
                    
                                        
            #PINTEREST
            elif 'pinterest' in socialLink:
                pinbool = False
                #onsite checker
                if socialLink in pin:
                    print("Valid pinterest page link : ", socialLink, pin)
                    updateCell(pincellname, 'green')
                    boolpin = True
                else:
                    boolpin = False
                    
                    
                #onlive checker
                if 'show_error=true' in socialLink:
                    print("error in pinterest ",socialLink)
                    boolpin1 = False
                else:
                    updateCell(pincellname1, 'green')
                    boolpin1 = True
                    
            #FACEBOOK   
            elif 'facebook' in socialLink:
                fbbool = False
                if socialLink in fb:
                    print("Valid facebook page link : ", socialLink, fb)
                    updateCell(fbcellname, 'green')
                    boolfb = True
                else:
                    boolfb = False
                    
                #onlive section
                source = driver.page_source
                soup = BeautifulSoup(source, 'html.parser')
                if "You must log in to continue." or "This Page Isn't Available" in str(soup):
                    print("Facebook Error")
                    boolfb1 = False
                else:
                    updateCell(fbcellname1, 'green')
                    boolfb1 = True
            else:
                print("Not a valid page link", socialLink)
            
    #Explicitly visit link and update onlive
    if instabool == True:
        print("Explicit visit for insta in domain : ", domain)
        res = explicitVisit(insta, 'insta')
        instabool = False
    if pinbool == True:
        print("Explicit visit for pin in domain : ", domain)
        res = explicitVisit(pin, 'pin')
        pinbool = False
    if fbbool == True:
        print("Explicit visit for fb in domain : ", domain)
        res = explicitVisit(fb, 'fb')
        fbbool = False
             
    #ONSITEBOOL
    if boolinsta == False:
        updateCell(instacellname, 'red')
    if boolpin == False:
        updateCell(pincellname, 'red')
    if boolfb == False:
        updateCell(fbcellname, 'red')
            
    #ONLIVEBOOL
    if boolinsta1 == False:
        updateCell(instacellname1, 'red')
    if boolpin1 == False:
        updateCell(pincellname1, 'red')
    if boolfb1 == False:
        updateCell(fbcellname1, 'red')
    
    driver.quit()
    print()     
    print()     
    print()     
    print()     
    print()     
