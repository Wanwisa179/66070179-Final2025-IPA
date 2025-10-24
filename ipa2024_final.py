#######################################################################################
# Yourname: Wanwisa Sathitooukuthai
# Your student ID: 66070179
# Your GitHub Repo: https://github.com/Wanwisa179/IPA2024-Final-66070179.git

#######################################################################################
# 1. Import libraries for API requests, JSON formatting, time, os, (restconf_final or netconf_final), netmiko_final, and ansible_final.
import requests
import json
import time
import os

from dotenv import load_dotenv
from requests_toolbelt import MultipartEncoder
from ansible_final import showrun, set_motd
from netmiko_final import gigabit_status, read_motd
from restconf_final import create, status, enable, disable, delete
from netconf_final import net_create, net_delete, net_enable, net_disable, net_status

#######################################################################################
# 2. Assign the Webex access token to the variable ACCESS_TOKEN using environment variables.

# ACCESS_TOKEN = os.environ."<!!!REPLACEME with os.environ method and environment variable!!!>"

load_dotenv()

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

if ACCESS_TOKEN is None:
    raise ValueError("ACCESS_TOKEN not found. Please set it in .env or environment variables.")
#######################################################################################
# 3. Prepare parameters get the latest message for messages API.

# Defines a variable that will hold the roomId
roomIdToGetMessages = os.getenv("room_id")

last_message_id = None

method = ""

is_busy = False

while True:
    time.sleep(0.1)
    if is_busy:
        continue
    try:
        is_busy = True

        # the Webex Teams GET parameters
        #  "roomId" is the ID of the selected room
        #  "max": 1  limits to get only the very last message in the room
        getParameters = {"roomId": roomIdToGetMessages, "max": 1}

        # the Webex Teams HTTP header, including the Authoriztion
        getHTTPHeader = {"Authorization": 'Bearer {}'.format(ACCESS_TOKEN)}

        postHTTPHeader = {"Authorization": 'Bearer {}'.format(ACCESS_TOKEN),"Content-Type": "application/json"}

        # 4. Provide the URL to the Webex Teams messages API, and extract location from the received message.
        
        # Send a GET request to the Webex Teams messages API.
        # - Use the GetParameters to get only the latest message.
        # - Store the message in the "r" variable.
        r = requests.get(
            "https://webexapis.com/v1/messages",
            params=getParameters,
            headers=getHTTPHeader
        )
        # verify if the retuned HTTP status code is 200/OK
        if not r.status_code == 200:
            raise Exception(
                "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
            )

        # get the JSON formatted returned data
        json_data = r.json()

        # check if there are any messages in the "items" array
        if len(json_data["items"]) == 0:
            print("There are no messages in the room.")
            continue

        # store the array of messages
        messages = json_data["items"]
        message_id = messages[0]["id"]

        if message_id == last_message_id:
            continue
        else:
            last_message_id = message_id  # จำ ID ไว้


        # store the text of the first message in the array
        message = messages[0]["text"]
        print("Received message: " + message)

        # check if the text of the message starts with the magic character "/" followed by your studentID and a space and followed by a command name
        #  e.g.  "/66070123 create"
        if message.startswith("/66070179"):
            is_busy = True
            try:
            # extract the command
                parts = message.split()
                if len(parts) < 2:
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : "Error: No command found."
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue

                ip = parts[1]

                if ip == "restconf":
                    method = ip

                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : "Ok: Restconf"
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue
                elif ip == "netconf":
                    method = ip
                
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : "Ok: Netconf"
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue
                elif method == "" and ip != "netconf" and ip != "restconf":
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : "Error: No method specified"
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue
                elif ip not in ["10.0.15.61", "10.0.15.62", "10.0.15.63", "10.0.15.64", "10.0.15.65"]:
                    print(ip)
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : " Error: No IP specified"
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue

                if len(parts) < 3:
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : "Error: No command found."
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
                    continue

                command = parts[2]
                print(command)

                if method == "restconf":
                    if command == "create":
                        re_data = create(ip)   
                    elif command == "delete":
                        re_data = delete(ip)
                    elif command == "enable":
                        re_data = enable(ip)
                    elif command == "disable":
                        re_data = disable(ip)
                    elif command == "status":
                        re_data = status(ip)
                    elif command == "gigabit_status":
                        re_data = gigabit_status(ip)
                    elif command == "showrun":
                        re_data = showrun(ip)
                    elif command == "motd":
                        if len(parts) > 3:
                            motd_message = " ".join(parts[3:])
                            re_data = set_motd(ip, motd_message)
                        else:
                            re_data = read_motd(ip)
                    else:
                        re_data = "Error: No command or unknown command"
                else:
                    if command == "create":
                        re_data = net_create(ip)   
                    elif command == "delete":
                        re_data = net_delete(ip)
                    elif command == "enable":
                        re_data = net_enable(ip)
                    elif command == "disable":
                        re_data = net_disable(ip)
                    elif command == "status":
                        re_data = net_status(ip)
                    elif command == "gigabit_status":
                        re_data = gigabit_status(ip)
                    elif command == "showrun":
                        re_data = showrun(ip)
                    elif command == "motd":
                        if len(parts) > 3:
                            motd_message = " ".join(parts[3:])
                            re_data = set_motd(ip, motd_message)
                        else:
                            re_data = read_motd(ip)
                    else:
                        re_data = "Error: No command or unknown command"

                if command == "showrun" and not re_data.startswith("Error"):
                    filename = re_data
                    fileobject = open(filename, 'rb')
                    filetype = "text/plain"

                    postData = MultipartEncoder({
                    "roomId": roomIdToGetMessages,
                    "text": "show running config",
                    "files": (os.path.basename(filename), fileobject, filetype)
                    })

                    HTTPHeaders = {
                        "Authorization": f"Bearer {ACCESS_TOKEN}",
                        "Content-Type": postData.content_type
                    }
           
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=postData,
                        headers=HTTPHeaders,
                    )

                    fileobject.close()

                    if r.status_code == 200:
                        print("File sent successfully to Webex room")
                    else:
                        print("Failed to send file. Status: {r.status_code}")
                        print(r.text)

                if command != "showrun":
                    sent_back = {
                        "roomId": roomIdToGetMessages,
                        "text" : re_data
                    }
            
                    r = requests.post(
                        "https://webexapis.com/v1/messages",
                        data=json.dumps(sent_back),
                        headers=postHTTPHeader,
                    )
                    if not r.status_code == 200:
                        raise Exception(
                            "Incorrect reply from Webex Teams API. Status code: {}".format(r.status_code)
                        )
                    else:
                        print("Message sent successfully!")
                    is_busy = False
            except Exception as e:
                print("Error:", e)
    finally:
        is_busy = False
