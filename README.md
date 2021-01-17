# PCStockAU
Keep track of store inventory from Australian tech retailers and send email alerts when product is in stock. Currently configured to track stock of AMD Ryzen 5600X. Ideal for use on raspberry pi.

## Requirements
Python 3.7+ <br />
Scrapy <br />
g-mail account with less secure app access enabled 


## Usage/Installation
NOTE: Recommended to be used in python virtual environment.
1. Download/Clone files from master branch.
2. In terminal pip install requirements.txt
3. Edit the script em_service.py with your sender and receiver email
4. run python script mtask.py (on rpi: python3.x mtask.py)

## Config
- To change the product to check stock status edit the urls list in mtask.py.(currently congifured with index [pccg,ple,msy,umart,ccom]). Make sure to insert the specific product page). <br />

-Time interval between each pass can be altered by changing value of sleep function in mtask.py default is 60 seconds. <br />

-Email time interval can be changed by modifing check_time variable. Default 1800sec/30min. 

### Notes

Tested on raspberry pi 3 and manjaro linux kde plasma 20.2.1
