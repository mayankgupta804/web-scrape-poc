import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
CHROME_DRIVER = "chromedriver"

def get_driver():
	driver = webdriver.Chrome(executable_path=os.path.abspath(CHROME_DRIVER), chrome_options=chrome_options)
	return driver
