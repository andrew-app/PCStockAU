import scrapy
import time
from colorama import Fore, Style, init
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from em_service import sendemail
import datetime
import pickle

#init(convert=True) 
#if no coloured font with output working uncomment above line

urls = ["https://www.pccasegear.com/products/53564/powercolor-radeon-rx-6800-xt-liquid-devil-16gb-rdna-2",
        "https://www.ple.com.au/Products/643561/AMD-Ryzen-5-5600X-37Ghz-6-Core-12-Thread-AM4---With-Wraith-Stealth-Cooler",
        "https://www.msy.com.au/online/graphic-cards/3931-asus-radeon-tuf-gaming-oc-rx-6800-xt-16gb-tuf-rx6800xt-o16g-gaming-.html",
        "https://www.umart.com.au/Sapphire-Radeon-RX-6800-XT-Pulse-OC-16G-Graphics-Card_59424G.html",
        "https://www.centrecom.com.au/sapphire-pulse-amd-radeon-rx-6800-xt-16gb-graphics-card",
        ]
i = 0

checktxt = ["In stock", "In Stock", "in stock", "Call", "Yes"]
stores = ["Online", "Bundoora"]
inv = {}

body = []



class MySpider(scrapy.Spider):
    name = "PCStockAU"
    start_urls = [urls[0]]


    custom_settings = {
        'LOG_ENABLED': 'False',

    }

    def parse(self, response):

        global i, checktxt, stores, inv

        store = False
        j = 0

        if i == 0: #PCCG Instance

            pccg = response.xpath("//div[@class='price-box']//text()").getall()
            title = response.xpath("//div[@class='title']//text()").getall()
            key = f"{title[1]} @PCCG"
            inv[key] = {}
            for stock in pccg:
                j = j + 1

                if checktxt[0] in stock:
                    inv[key] = "In Stock"
                    print(f"{Fore.BLUE}{title[1]} @PCCG::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    store = True

                elif j == len(pccg):  # 2nd last element in list will be ignored due to array indexing from 1 instead of 0
                    if store is False:
                        inv[key] = "Out of Stock"

                        print(f"{Fore.BLUE}{title[1]} @PCCG::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            i = i + 1
            yield scrapy.Request(urls[1], callback=self.parse)


        elif i == 1: #PLE Instance

            ple = response.xpath("//div[@class='viewItemAvailabilityStatusWrapper']//text()").getall()
            title = response.xpath("//div[@class='itemName']//text()").getall()

            key = f"{title[0]} @PLE"
            inv[key] = {}
            for stock in ple:
                j = j + 1

                if checktxt[0] in stock and store is False:
                    inv[key] = "In Stock"
                    print(f"{Fore.BLUE}{title[0]} @PLE::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    store = True



                elif j == len(ple):
                    if store is False:
                        inv[key] = "Out of Stock"
                        print(f"{Fore.BLUE}@PLE::{Fore.RED}Out of Stock{Style.RESET_ALL}")

            i = i + 1
            yield scrapy.Request(urls[2], callback=self.parse)


        elif i == 2: #MSY Instance

            msy = response.xpath("//div[@class='product-specs-box']//tr[@class='odd']//td[@class='spec-value ui-table-text-center color-green']//text()").get()
            title = response.xpath("//h1[@itemprop='name']//text()").getall()
            title = title[0]

            title = title.replace("\r\n", "")
            title = title.strip()

            key = f"{title} @MSY"
            inv[key] = {}
            if msy:
                inv[key] = "In Stock"
                print(f"{Fore.BLUE}{title} @MSY::{Fore.GREEN}In Stock{Style.RESET_ALL}")
            else:
                inv[key] = "Out of Stock"
                print(f"{Fore.BLUE}{title} @MSY::{Fore.RED}Out of Stock{Style.RESET_ALL}")
            i = i + 1
            yield scrapy.Request(urls[3], callback=self.parse)

        elif i == 3: #Umart Instance
            umart = response.xpath("//div[@class='col-xs-12 col-sm-6 col-md-12']//div[@class='content']//text()").getall()
            title = response.xpath("/html/body/div[6]/div[1]/div/div/div/div[2]/h1//text()").getall()
            for stock in umart:
                j = j + 1

                if checktxt[1] in stock:
                    print(f"{Fore.BLUE}{title[0]} @Umart::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    break

                elif j == len(umart):

                    print(f"{Fore.BLUE}{title[0]} @Umart::{Fore.RED}Out of Stock{Style.RESET_ALL}")
            i = i + 1
            yield scrapy.Request(urls[4], callback=self.parse)

        elif i == 4: #CCOM Instance

            ccom = response.xpath("//div[@class='prod_right']//text()").getall()
            title = response.xpath("//div[@class='prod_top']//text()").getall()
            for stock in ccom:
                j = j + 1

                if checktxt[1] in stock:
                    print(f"{Fore.BLUE}{title[1]} @Centrecom::{Fore.GREEN}In Stock{Style.RESET_ALL}")
                    break
                elif checktxt[3] in stock:
                    print(f"{Fore.BLUE}{title[1]} @Centrecom::{Fore.YELLOW}Call{Style.RESET_ALL}")
                    break


                elif j == len(ccom):
                    print(f"{Fore.BLUE}@CCOM::{Fore.RED}Out of Stock{Style.RESET_ALL}")
    





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
                print(inv)
                sendemail("Product Status", body)


