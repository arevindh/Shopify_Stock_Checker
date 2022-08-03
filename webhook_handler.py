import re
import requests
import config_handler
import error_logger

def fix_nonetypes(json_item):
    try:
        return str(json_item)
    except TypeError:
        return ""

def webhook_sender(item,stock_state,link,url):
    try:
        if stock_state == True:
            
            content = config_handler.read("config.cfg","webhook","content")

            variable_dict = {
                "{Name}" : fix_nonetypes(item['name']),
                "{Title}" : fix_nonetypes(item['title']),
                "{SKU}" : fix_nonetypes(item['sku']),
                "{Public Title}" : fix_nonetypes(item['public_title']),
                "{Option1}" : fix_nonetypes(item['option1']),
                "{Option2}" : fix_nonetypes(item['option2']),
                "{Option3}" : fix_nonetypes(item['option3']),
                "{Link}" : link,
            }

            for key in variable_dict.keys():
                content = re.sub(key, variable_dict[key], content)

            content = content.replace(r'\n', '\n')

            data = {
                "content" : content
            }
            
            requests.post(url,json=data)
    except Exception as e:
        print("!! SENDING WEBHOOK FAILED !!")
        error_logger.error_log("!! SENDING WEBHOOK FAILED !!",e)
        
def verify_webhook():
    try:
        url = config_handler.read("config.cfg","webhook","url")

        try:
            webhook_test = requests.get(url)
            if webhook_test.status_code != 200:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg.")
                print("Status code returned: " + str(webhook_test.status_code) + ". Expected 200")
                input()
            
            check_url = re.search("https://(canary\\.|ptb\\.|)discord(app)*\\.com/api/webhooks/\\d+/(\\w|-|_)*(/?)",url)
            if check_url == None:
                print("Webhook URL not valid. Check that you put the correct URL in config.cfg")
                print("Regex validation failed. If you believe this is incorrect, contact the devs or edit verify_webhook in webhook_handler.py")
                input()
            
        except Exception as e:
            error_logger.error_log("Webhook URL not valid. Check that you put the correct URL in config.cfg:",e)
            input()
        
    except Exception as e:
        error_logger.error_log("Webhook URL not found. Add the URL in config.cfg:",e)
        input()
    

