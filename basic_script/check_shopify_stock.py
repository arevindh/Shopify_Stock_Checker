import requests
import re
import json
import time
from datetime import datetime,timezone
import config_handler

with open("list.txt", "r") as urlListRaw:
        urlListLines = urlListRaw.readlines()
urlList = list(map(str.strip, urlListLines))

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

in_stock_list = []

stock_delay = config_handler.read("config.cfg","stock","stock_delay")
request_fail_delay = config_handler.read("config.cfg","stock","request_fail_delay")

def stock_checker(url):
    convert_url = re.sub("(?<!\.js)$",".js",re.sub("\?.*",".js",url))
    find_variant = re.search("(?<=\?variant\=)\d+",url)
    stock_json = json.loads(requests.get(convert_url).text)
    try:
        for item in stock_json['variants']:
            utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
            if find_variant != None:
                if find_variant.group(0) == str(item['id']):
                    stock_message = utc_time_print + ", In stock: " + str(item['available']) + ", Name: " + str(item['name']) + ", SKU: " + str(item['sku'] + ", URL: " + url)
                    print(stock_message)
                    if str(item['available']) == "True":
                        in_stock_list.append(utc_time_print + ", Name: " + str(item['name']) + ", SKU: " + str(item['sku'] + ", URL: " + url))
                        
                    write_stock_record(stock_message)
            else:
                stock_message = utc_time_print + ", In stock: " + str(item['available']) + ", Name: " + str(item['name']) + ", SKU: " + str(item['sku'] + ", URL: " + url)
                print(stock_message)
                if str(item['available']) == "True":
                    in_stock_list.append(utc_time_print + ", Name: " + str(item['name']) + ", SKU: " + str(item['sku'] + ", URL: " + url))
                    
                write_stock_record(stock_message)
                    
    except Exception as e:
        print("Request failed\n")
        print(e)
        print("Request fail delay. Waiting: " + str(request_fail_delay) + " seconds")
        time.sleep(float(request_fail_delay))
        utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
        stock_message = utc_time_print + ", In stock: " + "Request failed" + ", URL: " + url
        
    print("Stock delay. Waiting: " + str(stock_delay) + " seconds")
    time.sleep(float(stock_delay))
        

def write_stock_record(stock_message):
    try:
        with open ("shopify_stock_record_" + utc_time + ".txt", "a") as stock_record:
            stock_record.write(stock_message)
            stock_record.write("\n")
    except Exception as e:
        print("Could not open or write to file\n")
        print(e)
        input()

for item in urlList:
    stock_checker(item)

print("\n\n\nItems that are in stock:")
for item in in_stock_list:
    print(item)
    if item == in_stock_list[-1]:
        input()
        
if len(in_stock_list) < 1:
    print("Nothing is in stock")
    input()
