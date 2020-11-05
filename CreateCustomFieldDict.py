import urllib.request
import json



####CONSTANTS####

#This is to be located in a separate workspace in a separate task.  Fill a task full of every single custom field you have created, this will provide the program
#the ability to access and reference the unique IDs of each custom field that (to my knowledge) is only accessible through a response body of an API request. 
DICT_ID = '' #task where all custom field data can be retrieved from (Currently located in 'Brady Bess - Essential Onboarding' list)

JSON_HEADERS = {
    'Authorization': '',
    'Content-Type': 'application/json'
    }
#################

def create_Dict():
    cust_field_dict = {}
    url = 'https://api.clickup.com/api/v2/task/' + DICT_ID

    request = urllib.request.Request(url, headers=JSON_HEADERS)

    with urllib.request.urlopen(request, data=None) as f:
        resp = f.read()
        js = json.loads(resp)

        all_cust_fields = js['custom_fields']

        for field in all_cust_fields:
            cust_field_dict[field['name']] = field['id']
    
    #print(cust_field_dict)
    return cust_field_dict


