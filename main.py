from selenium import webdriver
import chromedriver_autoinstaller
import csv
class Bot:
    def __init__(self, headless=False):
        self.driver = self._init_driver(headless)
        self.driver.get('https://platform.worldquantbrain.com/')

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
    
    def crawler(self):
        self.driver.get('https://platform.worldquantbrain.com/learn/data-and-operators/company-fundamental-data-for-equity')
        rows = self.driver.find_elements('xpath', '//div[@class="rt-tr-group"]')
        with open('data.csv', 'w') as f:
            mywriter = csv.writer(f)
            for row in rows:
                row_data = []
                for data in row.find_elements('xpath', './/div[@class="rt-td"]'):
                    row_data.append(data.text)
                mywriter.writerow(row_data)
        print(1)

        
    
if __name__ == '__main__':
    bot = Bot()
    bot.crawler()