from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
import csv
import time
from utils import load_params
from tqdm import tqdm 

class CBot:
    def __init__(self, headless=False):
        self.driver = self._init_driver(headless)
        self.driver.get('https://platform.worldquantbrain.com/')
        self.login()
        
    def _init_driver(self, headless=False):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')
        if headless:
            options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        return driver
    
    def login(self):
        account = load_params()['account']
        #Accpet cookies
        try:
            time.sleep(10) # Waiting for page loading...
            accept_btn = self.driver.find_element('xpath', '//button[@class="button button--md button--primary"]')
            accept_btn.click()
        except NameError as e:
            print(e)
        #Login
        try:
            # self.driver.find_element(By.ID, 'email').send_keys(account['user_name'])
            # self.driver.find_element(By.ID, 'password').send_keys(account['pwd'])
            self.driver.find_element(By.NAME, 'currentEmail').send_keys(account['user_name'])
            self.driver.find_element(By.NAME, 'currentPassword').send_keys(account['pwd'])
            
            self.driver.find_element('xpath', '//button[@class="ui button button button--lg"]').click()
        except:
            print('--Fail to login--')
                    
    def crawler(self, url: str=None, save_path: str=None):
        if url:
            self.driver.get(url)
        else:
            self.driver.get('https://platform.worldquantbrain.com/learn/data-and-operators/company-fundamental-data-for-equity')
        time.sleep(10) # Waiting for loading...
        rows = self.driver.find_elements('xpath', '//div[@class="rt-tr-group"]')
        if save_path is None:
            save_path = 'Company Fundamental Data for Equity - Fundamental Datasets.csv'
        with open(save_path, 'w') as f:
            mywriter = csv.writer(f)
            for row in tqdm(rows):
                row_data = []
                for data in row.find_elements('xpath', './/div[@class="rt-td"]'):
                    row_data.append(data.text)
                mywriter.writerow(row_data)
        print('--Done--')
    
if __name__ == '__main__':
    bot = CBot()
    bot.crawler()