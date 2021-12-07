import time
from colorama import Fore, Style, init
from multiprocessing import Process
from em_service import sendemail
import datetime
import pickle
import os
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver

options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
checktxt = f"\"inStock\":true"
inv = {}
body = []
key = f"Nano Noé in Monogram canvas @ Louis Vuitton"
url = "https://au.louisvuitton.com/eng-au/products/nano-noe-monogram-010573"

def CheckStock():
    driver.get("https://api.louisvuitton.com/api/eng-au/catalog/availability/010573")
    status = driver.find_element_by_xpath("//div[@id='json']").text
    
    inv[key] = {}
    if checktxt in status:
        inv[key] = "In Stock"
        print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.GREEN}In Stock{Style.RESET_ALL}")

    else:
        inv[key] = "Out of Stock"
        print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.RED}Out of Stock{Style.RESET_ALL}")

def UpdateStock():
    CheckStock()
    time.sleep(15) #check stock every x seconds
    
    body.append([inv, url])
    with open(status, 'wb') as fi:
        pickle.dump(inv, fi)
    with open(emailb, 'wb') as fi:
        pickle.dump(body, fi)


if __name__ == '__main__':
    check_time = time.strftime("%H:%M:%S", time.gmtime(15))
    start_time = time.time()
    status = "data.pk"
    emailb = "emb.pk"

    while True:
        p = Process(target=UpdateStock)
        p.start()
        p.join()

        current_time = time.time()
        elapsed_time = current_time - start_time
        t = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        print("Uptime: ", t)
        if t >= check_time:  # email sent every 30 minutes when in stock
            os.system('clear')
            h, m, s = check_time.split(":")
            check_time_u = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
            check_time = check_time_u + 900
            check_time = time.strftime("%H:%M:%S", time.gmtime(check_time))
            with open(status, 'rb') as fi:
                inv = pickle.load(fi)
            with open(emailb, 'rb') as fi:
                body = pickle.load(fi)
            if "In Stock" in inv.values():
                print("email sent")
                sendemail("", "Nano Noe @LV In Stock!", body)
                sendemail("", "Nano Noe @LV In Stock!", body)
                

