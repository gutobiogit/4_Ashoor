#!/usr/bin/python3

import os
import requests
import json

ROOT_DIR = '/home/smokey/Videos'

HEADERS = {'Authorization': 'Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXX','Content-Type': 'application/json'}
HEADERS_NO_JSON = {'Authorization': 'Bearer XXXXXXXXXXXXXXXXXXXXXXXXXXX'}
 

class colors:
    RED = '\033[31m'
    ENDC = '\033[m'
    BLUE = '\033[34m'

def create_folder(folder_name)->str:
    URL = "https://api.vimeo.com/me/projects"
    PAYLOAD = "{\"name\" : \""+folder_name+"\"}"
    try:
        response = requests.request("POST", URL, headers=HEADERS, data=PAYLOAD)
        response_dict = json.loads(response.text)
        folder_num = response_dict['uri'].split('/')[-1]
        return folder_num
    except:
        return False

def upload_video(video_size,video_place,video_name,folder_num)->str:
    URL = "https://api.vimeo.com/me/videos"
    payload="{\n  \"upload\": {\n    \"approach\": \"post\",\n    \"size\": "+str(video_size)+"\n  },\n  \"name\": \""+video_name+"\"\n}"
    try:
        response = requests.request("POST", URL, headers=HEADERS, data=payload)
        response_dict = json.loads(response.text)
        video_num = response_dict['uri'].split('/')[-1]
        video_URL = response_dict['upload']['upload_link']
        payload={}
        name1= video_place.split("/")[-1]
        files_open=[('file_data',(name1,open(video_place,'rb'),'application/octet-stream'))]
        response = requests.request("POST", video_URL, headers=HEADERS_NO_JSON, data=payload, files=files_open)
        payload={}
        url = f"https://api.vimeo.com/me/projects/{folder_num}/videos/{video_num}"
        response = requests.request("PUT", url, headers=HEADERS_NO_JSON, data=payload)
    except:
        return False

if __name__ == "__main__":
    for root, subdirs, files in os.walk(ROOT_DIR):
        if subdirs ==[]:
            folder_num=create_folder(root.split('/')[-1])
            print(f"{colors.RED}{root.split('/')[-1]}{colors.ENDC}")
        for file in files:
            print(f"{colors.BLUE}|_ {root}/{file}{colors.ENDC}")
            upload_video(os.path.getsize(root+"/"+file),root+"/"+file,file,folder_num)
        print(" ")
