import urllib.request
import json

####CONSTANTS####
DICT_ID = 'awkpfk' #task where all custom field data can be retrieved from (Currently located in 'Brady Bess - Essential Onboarding' list)

JSON_HEADERS = {
    'Authorization': 'pk_6301319_S7FUWRI2ZQJPCRJPE2SPO9YZVOS3LPBF',
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


