import requests
import re
import itertools
import time
import json
from datetime import datetime,timezone
import webhook_handler
import config_handler
import stock_state_tracker

utc_time = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

stock_delay = config_handler.read("config.cfg","stock","stock_delay")
batch_delay = config_handler.read("config.cfg","stock","batch_delay")
request_fail_delay = config_handler.read("config.cfg","stock","request_fail_delay")

def find_variants(url):
    convert_url = re.sub("(?<!\.js)$",".js",re.sub("\?.*",".js",url))
    find_variant = re.search("(?<=\?variant\=)\d+",url)
    stock_json = json.loads(requests.get(convert_url).text)
        
    if find_variant != None:
        return [find_variant.group(0), stock_json]
        
    else:
        return ["", stock_json]

def stock_info_handling(stock_info,stock_message,stock_state_id,item_info,link):
    if stock_info == "True":
        stock_state = stock_state_tracker.find_item_state(stock_state_id,"True")
        webhook_handler.webhook_sender(item_info,stock_state,link)
        
    else:
        stock_state_tracker.find_item_state(stock_state_id,"False")
            
    utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")

    try:
        with open ("shopify_stock_record_" + utc_time + ".txt", "a") as stock_record:
            stock_record.write(stock_message)
            stock_record.write("\n")
                
    except Exception as e:
        print("Could not open or write to file:")
        print(e)
        
def stock_check_runner(request_data):
    try:
        variant_check = find_variants(request_data)
        
        stock_json = variant_check[1]
        find_variant = variant_check[0]

        for item in stock_json['variants']:
            correct_item = False
            #filter out variants which are not specified in the url list
            if find_variant != "" and find_variant == str(item['id']):
                correct_item = True
                
            elif find_variant == "":
                correct_item = True

            if correct_item == True:
                utc_time_print = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
                stock_message = utc_time_print + ", In stock: " + str(item['available']) + ", Name: " + str(item['name']) + ", Title: " + str(item['title']) + ", SKU: " + str(item['sku'] + ", Link: " + request_data)
                print(stock_message)
                stock_info_handling(str(item['available']),stock_message,request_data + "_" + str(item['id']),item,request_data)
                
        print("Stock delay. Waiting: " + str(stock_delay) + " seconds")
        time.sleep(float(stock_delay))
        
    except Exception as e:
        print("Stock check failed:")
        print(e)
        print("Request fail delay. Waiting: " + str(request_fail_delay) + " seconds")
        time.sleep(float(request_fail_delay))
        
#verify that the webhook url is set and valid
webhook_handler.verify_webhook()
try:
    with open("list.txt", "r") as urlListRaw:
        urlListLines = urlListRaw.readlines()
    urlList = list(map(str.strip, urlListLines))

except Exception as e:
    print("list.txt not found or cannot be opened. Make sure you've made the file correctly.")
    print(e)
    input()

while True:
    for item in urlList:
        stock_check_runner(item)
    print("Batch delay. Waiting: " + str(batch_delay) + " seconds")
    time.sleep(float(batch_delay))
