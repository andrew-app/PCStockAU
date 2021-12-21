import time
from colorama import Fore, Style, init
from multiprocessing import Process
import datetime
import pickle
import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
import json
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
inv = {}
body = []
key = f"Nano Noé in Monogram canvas @ Louis Vuitton"
url = "view-source:https://api.louisvuitton.com/api/eng-au/catalog/availability/010573"
def CheckStock():
    
    driver.get(url)
    content = driver.page_source
    content = driver.find_element_by_tag_name('pre').text
    product = json.loads(content)
    inv[key] = {}
    for item in product['skuAvailability']:
        if item['inStock'] is True:
            inv[key] = "In Stock"
            print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.GREEN}In Stock{Style.RESET_ALL}")
            
        else:
            inv[key] = "Out of Stock"
            print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.RED}Out of Stock{Style.RESET_ALL}")
            
        
while(1):
    CheckStock()
