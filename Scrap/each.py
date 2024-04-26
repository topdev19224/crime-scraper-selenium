from selenium import webdriver
from bs4 import BeautifulSoup as BS
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

import csv
from datetime import datetime
import os

SCRAPING_URL = 'https://communitycrimemap.com/'
FLAG = False
EXTRA_DATA = False

class Scrap:
  # ! Init
  def __init__(self):
    self.header = [ 'Class', 'Incident', 'Crime', 'Date/Time', 'Location_Name', 'Address', 'Accuracy', 'Agency', 'keyword' ]
    self.search_keyword = self.Class = self.Incident = self.Crime = self.Date = self.Location_Name = self.Address = self.Accuracy = self.Agency = self.from_date = self.last_date_temp = self.last_date = ''
    arg1 = "--profile-directory=Person1"
    arg2 = "user-data-dir=C:\\Users\\Administrator\\AppData\\Local\\Google\\Chrome\\User Data\\Person6"
    arg3 = '--start-maximized'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(arg1)
    chrome_options.add_argument(arg2)
    chrome_options.add_argument(arg3)

    chrome_options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    self.DRIVER = webdriver.Chrome()

  # FORMAT scraping system whenever scraping new business
  def format(self):  
     self.search_keyword = self.Class = self.Incident = self.Crime = self.Date = self.Location_Name = self.Address = self.Accuracy = self.Agency = ''

  # WRITE location info for each business in file's row
  def write_info(self, data):
     try:
        with open("results/" + str(self.search_keyword) + ".csv", mode = 'a', newline='', encoding='utf-8') as file:
           writer = csv.writer(file)
           writer.writerow(data)

     except Exception as e:     
        print("Error: while writing data \n", e)
     
  # WRITE header into each business file
  def write_header(self):
     data = self.header
     if os.path.exists("results/" + self.search_keyword + ".csv"): return
     try:
        with open("results/" + self.search_keyword + ".csv", 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(data)

     except Exception as e: 
        print('Error while writing header \n', e)


  # GET all locations info using internal statement
  def get_info(self):   
     print('waiting until data is displayed')
     # Wait until data is displyed
     try:
        WebDriverWait(self.DRIVER, 300).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/table/thead/tr')))
     except: 
        print('data is not displayed')
        return

     print(self.search_keyword, 'filtered')

     try:
        self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/div/app-paginator/div/div[2]/mat-paginator/div/div/div[2]/button[4]').click()

        cnt = self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/div/app-paginator/div/div[3]/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span/span').text

        if not cnt: 
           print('No total page number')
           return

        # return first page
        self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/div/app-paginator/div/div[2]/mat-paginator/div/div/div[2]/button[1]').click()
        sleep(1)
     except: 
        print("No pagination")
        return
     ####### Find the number of total pagination #######

     for i in range(int(cnt)):
        global EXTRA_DATA
        EXTRA_DATA = False
        soup = BS(self.DRIVER.page_source, 'html.parser')
        
        # Check all data is displayed
        try:
           WebDriverWait(self.DRIVER, 50).until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/table/tbody/tr/td[string-length(normalize-space()) > 0]')))
        except: 
           print('No data to get')
           break

        tbody_ele = soup.find('tbody')
        tr_eles = tbody_ele.find_all('tr')

        # Extraction each data in Array to scrap
        for j in range(len(tr_eles)):
           data = []
           td_eles = tr_eles[j].find_all('td')
           for k in range(len(td_eles)):
              data.append(td_eles[k].get_text().strip())
              
              # Compare first date and last date
              if int(cnt) == 10 and len(tr_eles) == 50 and i == (int(cnt) - 1) and j == (len(tr_eles) - 1) and k == 3:
                 EXTRA_DATA = True
                 self.last_date_temp = td_eles[k].get_text().split(' ')[1]
                 print(self.last_date_temp)

           data.append(self.search_keyword)
           self.write_info(data)
        
        try:
           
           self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/main/app-grid/div/div[2]/app-simple-table/div/div/app-paginator/div/div[2]/mat-paginator/div/div/div[2]/button[3]').click()

        except Exception as e: pass

     if (self.last_date_temp != self.from_date) and EXTRA_DATA:
        print(self.last_date_temp)
        self.filter()
        self.last_date_temp = self.last_date
        print('Last date updated into original')
        self.get_info()
     else: 
        self.last_date_temp = self.last_date
        print('Last date updated into original')
        print('')
        print(self.search_keyword, ' completed')
        
  ############## Filter data changing date ######################

  def filter(self):
    print('filtering...')
    global FLAG
    # Click filter button
    WebDriverWait(self.DRIVER, 30).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/button/span[1]'))).click()

    # Input date(from)
    if not FLAG:
      self.DRIVER.execute_script('document.getElementById("mat-input-1").value = ""')
      self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[1]/div[3]/div[2]/mat-form-field/div/div[1]/div[3]/input').send_keys(self.from_date)
      
    ###### Input date(to) ######
      
    if not FLAG:
      self.DRIVER.execute_script('document.getElementById("mat-input-2").value = ""')
      self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[1]/div[3]/div[3]/mat-form-field/div/div[1]/div[3]/input').send_keys(self.last_date_temp)

    self.DRIVER.execute_script('document.getElementById("mat-input-2").value = ""')
    self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[1]/div[3]/div[3]/mat-form-field/div/div[1]/div[3]/input').send_keys(self.last_date_temp)
    
    ###### Input date(to) ######
    
    if not FLAG:
      self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[2]/mat-tab-group/div/mat-tab-body[1]/div/div[1]/mat-checkbox/label/span[2]').click()
      sleep(1)
    
    # Click apply button
    self.DRIVER.find_element(By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/div/app-filter-options/div/div[3]/button[2]/span[1]').click()
    print('filtering applied')
    FLAG = True
  
  ############## Filter data changing date ######################

  # START to scrap
  def start(self):  
    self.DRIVER.maximize_window()
    while True:
        search_keyword = input("Please input search keyword: ")
        self.search_keyword = search_keyword
        print("Please input date range: ")
        self.from_date = input("From: (01/01/2000): ")
        self.last_date_temp = input("To: (12/31/2024):(if you want current date, enter) ")
      
        if not search_keyword or not self.from_date: continue
      
        if not self.last_date_temp: self.last_date_temp = datetime.now().strftime("%m/%d/%Y")
      
        print(search_keyword, "scraping start between", self.from_date, "and", self.last_date_temp)
        break
  
    self.DRIVER.get(SCRAPING_URL)
    sleep(3)

    FLAG = False 
    # Accept cookie
    try:
      
      WebDriverWait(self.DRIVER, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[2]/div/mat-dialog-container/app-welcome-disclaimer/div/div/div[5]/button'))).click()

      sleep(2)

    except Exception as e: pass

    self.write_header()

    self.DRIVER.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/div/mat-form-field/div/div[1]/div[3]/input").clear()
    self.DRIVER.find_element(By.XPATH, "/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/div/mat-form-field/div/div[1]/div[3]/input").send_keys(self.search_keyword)

    WebDriverWait(self.DRIVER, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[2]/app-search/div/div/mat-form-field/div/div[1]/div[4]/button[2]/span[1]'))).click()

    WebDriverWait(self.DRIVER, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/app-root/app-main-layout/div/header/div/app-navbar/header/div/div[3]/app-navbar-actions/div/div[2]/button/i'))).click()

    self.filter()
    self.get_info()