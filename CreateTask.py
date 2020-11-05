import urllib.request
import urllib.error
import json
import requests
import cv2
from csv import DictReader
from colorama import Fore
from colorama import Style
import CreateCustomFieldDict
import ctypes

kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


#This script creates a new task in ClickUp and appends the task ID to follow office naming conventions
#Written by Brady Bess, PandA Tech Office

#INSERT CLICKUP AUTHORIZATION HEADER INTO CONSTANT FIELD BELOW

###CONSTANTS###
JSON_HEADERS = {
    'Authorization': '',
    'Content-Type': 'application/json'
    }

LIST = '21088336' #list corresponds to "Research" section of ClickUp

CUSTOM_FIELD_IDS = CreateCustomFieldDict.create_Dict() #dictionary of key (plain text custom field name) and value (ClickUp generated ID for custom field) pairs for referencing custom fields

ADD_THESE_CUST_FIELDS = [] #plain text titles of custom fields to be added 

#COLORS#
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[m'
###############

def initialize_Cust_Field_To_Add(column_names):
    for title in column_names:
        if title in CUSTOM_FIELD_IDS: #custom field is listed in .csv file to add, store in list to reference later
            ADD_THESE_CUST_FIELDS.append(title)

def create_Task(row): 
    values = """
    {
        "name": \"""" + row['Name'] + """\",
        "description": \"""" + row['Description'] + """\",
        "assignees": [ 
            
        ],
        "tags": [],
        "status": "Backlog",
        "priority": 3,
        "due_date": null,
        "due_date_time": false,
        "time_estimate": null,
        "start_date": null,
        "start_date_time": false,
        "notify_all": true,
        "parent": null,
        "links_to": null,
        "custom_fields": [ """ + get_custom_fields_to_add(row) + """
        ]
    }
    """
    data = values.encode("utf-8")

    print(values)

    reqCreate = urllib.request.Request('https://api.clickup.com/api/v2/list/' + LIST + '/task', data=data, headers=JSON_HEADERS)
    
    with urllib.request.urlopen(reqCreate,data=None) as f:
        if f.getcode() == 200:
            resp = f.read()
            js = json.loads(resp)
            taskID = js['id']
            taskName = js['name']
            oldStatus = js['status']['status']
            updatedName = taskName + " #" + taskID

            rename_new_task(taskID, updatedName, oldStatus)

        else:
            print (RED + 'FAILED\nPROBLEM CREATING TASK: ' + taskID + '\nCheck ClickUp to troubleshoot' + RESET) 


def get_custom_fields_to_add(row):
    json_str = ''
    for field in ADD_THESE_CUST_FIELDS:
        if len(row[field]) != 0:
            json_str += "{ \"id\":\"" + CUSTOM_FIELD_IDS[field] + "\",\n" + "\"value\":\"" + row[field] + "\"},"
    
    return json_str[:len(json_str) - 1] #deletes closing comma

def rename_new_task(taskID, updatedName, oldStatus):
    #print("INSIDE FUNCTION\n" + updatedName + ", " + oldStatus)
    updatedValues = """
    {
        "name": \"""" + updatedName + """\" ,
        "description": "Updated Task Content",
        "status": \"""" + oldStatus + """\",
        "priority": 1,
        "time_estimate": null,
        "assignees": {
            "add": [],
            "rem": []
        },
        "archived": false
    } """

    updatedData = updatedValues.encode("utf-8")

    url = 'https://api.clickup.com/api/v2/task/' + taskID

    r = requests.put(url, data=updatedData, headers=JSON_HEADERS)
    print(r.status_code)
    if r.status_code == 200:
        print (GREEN + '\nSUCCESS\nTask ' + BLUE + taskID + GREEN + ' created and named ' + BLUE + updatedName + GREEN + '\n\t' +
        BLUE + str(len(ADD_THESE_CUST_FIELDS)) + GREEN + ' Custom Fields Added\n' + RESET)
    else:
        print (RED + 'FAILED\nPROBLEM RENAMING TASK: ' + taskID + '\nCheck ClickUp to troubleshoot' + RESET) 

def main():
    with open('tasksInfo.csv', 'r', encoding="utf-8-sig") as read_obj: #iterate thru .csv adding tasks
        info_dict = DictReader(read_obj)
        column_names = info_dict.fieldnames
        initialize_Cust_Field_To_Add(column_names)

        for row in info_dict:
            if len(row['Name']) != 0:  #valid rows only
                create_Task(row)

if __name__ == "__main__":
    main()
