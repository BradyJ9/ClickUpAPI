import urllib.request
import urllib.error
import json
import requests
import cv2
import io

#This script creates a new task in ClickUp and appends the task ID to follow office naming conventions
#

###CONSTANTS###
JSON_HEADERS = {
    'Authorization': 'pk_6301319_S7FUWRI2ZQJPCRJPE2SPO9YZVOS3LPBF',
    'Content-Type': 'application/json'
    }

MPFORM_HEADERS = {
    'Authorization': 'pk_6301319_S7FUWRI2ZQJPCRJPE2SPO9YZVOS3LPBF',
    'Content-Type': 'multipart/form-data'
    }

LIST = '21088336' #list corresponds to "Research" section of ClickUp

TASKID = '6ja8hy' #task to retrieve for testing
###############

attachment = open("keyboard.png", "rb").read()
print(attachment)
#cont = attachment.read()

values = """
attachment: """ + attachment.decode('utf-8') + """ (file)
filename: keyboard.png (string)"""

data = values.encode("utf-8")

#req = urllib.request.Request('https://api.clickup.com/api/v2/task/' + TASKID + '/attachment', data=data, headers=MPFORM_HEADERS)

#f = urllib.request.urlopen(req, data=None)
#files = {'attachment': ('keyboard.png')}

#r = requests.post('https://api.clickup.com/api/v2/task/' + TASKID + '/attachment', data=data, headers=MPFORM_HEADERS, files=files)

#print(r.text)