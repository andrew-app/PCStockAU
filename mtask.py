import scrapy
import time
from colorama import Fore, Style, init
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from em_service import sendemail
import datetime
import pickle

#init(convert=True) #if no coloured font with output working use this line

urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth",
        "https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",
        "https://www.msy.com.au/amd-ryzen-5-5600x-100-100000065box-up-to-46ghz-base-clock-37ghzam46-cores12-threads32mb65w-unlocked-boxed-cpu-without-cpu-cooler",
        "https://www.umart.com.au/AMD-Ryzen-5-5600X-6-Core-AM4-4-6GHz-CPU-Processor_57284G.html",
        "https://www.centrecom.com.au/amd-ryzen-5-5600x-460ghz-6-cores-12-threads-am4-desktop-processor"
        ]
i = 0

checktxt = ["In stock", "In Stock", "in stock", "Call", "Yes"]
stores = ["Online", "Bundoora"]
inv = {
    "PCCG": "Out of Stock",
    "PLE": "Out of Stock",
    "CCOM": "Out of Stock",
    "MSY": "Out of Stock",
    "Umart": "Out of Stock"
}

body = []



class MySpider(scrapy.Spider):
    name = "PCStockAU"
    start_urls = ["https://www.pccasegear.com/products/52254/amd-ryzen-5-5600x-with-wraith-stealth"]
    custom_settings = {
        'LOG_ENABLED': 'False',

    }

    def parse(self, response):

        global i, checktxt, stores, inv
        store = False
        j = 0

        if i == 0:

            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            for stock in pccg:
                j = j + 1

                if checktxt[0] in stock:
                    print(f"{Fore.BLUE}@PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    inv["PCCG"] = "In Stock"
                    store = True
                elif j == len(
                        pccg):  # 2nd last element in list will be ignored due to array indexing from 1 instead of 0
                    if store is False:
                        print(f"{Fore.BLUE}@PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[1], callback=self.parse)


        elif i == 1:

            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()

            for stock in ple:
                j = j + 1

                if checktxt[0] in stock:

                    print(f"{Fore.BLUE}@PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")

                    MySpider.inv["PLE"] = "In Stock"
                    store = True



                elif j == len(ple):
                    if store is False:
                        print(f"{Fore.BLUE}@PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[2], callback=self.parse)


        elif i == 2:

            msy = response.xpath("//div[@class='product-specs-box']//tr[@class='odd']//td[@class='spec-value ui-table-text-center color-green']//text()").get()
            if msy:
                print(f"{Fore.BLUE}@MSY::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                inv["MSY"] = "In Stock"
            else:
                print(f"{Fore.BLUE}@MSY::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            i = i + 1
            yield scrapy.Request(urls[3], callback=self.parse)

        elif i == 3:
            umart = response.xpath("//div[@class='col-xs-12 col-sm-6 col-md-12']//div[@class='content']//text()").getall()
            for stock in umart:
                j = j + 1

                if checktxt[1] in stock:
                    print(f"{Fore.BLUE}@Umart::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    inv["Umart"] = "In Stock"
                    break

                elif j == len(umart):

                    print(f"{Fore.BLUE}@Umart::{Fore.RED}Out of Stock{Style.RESET_ALL}")
                    i = i + 1
                    yield scrapy.Request(urls[4], callback=self.parse)

        elif i == 4:

            ccom = response.xpath("//div[@class='prod_right']//text()").getall()
            for stock in ccom:
                j = j + 1

                if checktxt[1] in stock:
                    print(f"{Fore.BLUE}@Centrecom::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    inv["CCOM"] = "In Stock"
                    break
                elif checktxt[3] in stock:
                    print(f"{Fore.BLUE}@Centrecom::{Fore.YELLOW}Call{Style.RESET_ALL}")
                    break


                elif j == len(ccom):
                        break



def CheckStock():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    time.sleep(60) #check stock every 60 sec
    body.append([inv, urls])
    with open(status, 'wb') as fi:
        pickle.dump(inv, fi)
    with open(emailb, 'wb') as fi:
        pickle.dump(body, fi)


if __name__ == '__main__':
    check_time = time.strftime("%H:%M:%S", time.gmtime(1800))
    start_time = time.time()
    status = "data.pk"
    emailb = "emb.pk"

    while True:
        p = Process(target=CheckStock)
        p.start()
        p.join()

        current_time = time.time()
        elapsed_time = current_time - start_time
        t = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        print("Uptime: ", t)
        if t > check_time:  # email sent every 30 minutes when in stock
            h, m, s = check_time.split(":")
            check_time_u = int(datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)).total_seconds())
            check_time = check_time_u + 1800
            check_time = time.strftime("%H:%M:%S", time.gmtime(check_time))
            with open(status, 'rb') as fi:
                inv = pickle.load(fi)
            with open(emailb, 'rb') as fi:
                body = pickle.load(fi)
            if checktxt[1] in inv.values():
                print("email sent")
                sendemail("Product Status", body)


