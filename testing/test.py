from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from colorama import Fore, Style, init
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
checktxt = f"\"inStock\":true"
def CheckStock():
    driver.get("https://api.louisvuitton.com/api/eng-au/catalog/availability/010573")
    status = driver.find_element_by_xpath("//div[@id='json']").text



    if checktxt in status:
        print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.GREEN}In Stock{Style.RESET_ALL}")

    else:
        print(f"{Fore.BLUE} Nano Noé in Monogram canvas @Louis Vuitton::{Fore.RED}Out of Stock{Style.RESET_ALL}")




