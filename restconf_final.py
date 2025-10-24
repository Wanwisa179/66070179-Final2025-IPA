import json
import requests
requests.packages.urllib3.disable_warnings()

# Router IP Address is 10.0.15.181-184
api_list = {"https://10.0.15.61/restconf", "https://10.0.15.62/restconf", "https://10.0.15.63/restconf", "https://10.0.15.64/restconf", "https://10.0.15.65/restconf"}

api_url_status = "https://10.0.15.61/restconf/data/ietf-interfaces:interfaces-state/interface=Loopback66070179"

# the RESTCONF HTTP headers, including the Accept and Content-Type
# Two YANG data formats (JSON and XML) work with RESTCONF 
headers = { "Accept": "application/yang-data+json", 
            "Content-type":"application/yang-data+json"
           }
basicauth = ("admin", "cisco")

def what_ip(ip):
    for ip_router in api_list:
        ip_api = "https://"+ip+"/restconf"
        if ip_router == ip_api:
            return ip_router

def create(ip):
    api_url = what_ip(ip)
    yangConfig = {
        "ietf-interfaces:interface": {
        "name": "Loopback66070179",
        "description": "My final2024 loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.1.79.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
        }
    } 

    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot create: Interface loopback 66070179"
    else:
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback66070179", 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070179 is created successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot create: Interface loopback 66070179"


def delete():
    api_url = what_ip(ip)
    resp = requests.delete(
        api_url + "/data/ietf-interfaces:interfaces/interface=Loopback66070179", 
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        return "Interface loopback 66070179 is deleted successfully"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot delete: Interface loopback 66070179"


def enable():
    api_url = what_ip(ip)
    yangConfig = {
        "ietf-interfaces:interface": {
        "name": "Loopback66070179",
        "description": "My final2024 loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": True,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.1.79.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
        }
    }

    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback66070179", 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
            )
        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070179 is enabled successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot enable: Interface loopback 66070179"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot enable: Interface loopback 66070179"


def disable():
    api_url = what_ip(ip)
    yangConfig = {
        "ietf-interfaces:interface": {
        "name": "Loopback66070179",
        "description": "My final2024 loopback",
        "type": "iana-if-type:softwareLoopback",
        "enabled": False,
        "ietf-ip:ipv4": {
            "address": [
                {
                    "ip": "172.1.79.1",
                    "netmask": "255.255.255.0"
                }
            ]
        },
        "ietf-ip:ipv6": {}
        }
    }

    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        resp = requests.put(
            api_url + "/data/ietf-interfaces:interfaces/interface=Loopback66070179", 
            data=json.dumps(yangConfig), 
            auth=basicauth, 
            headers=headers, 
            verify=False
            )

        if(resp.status_code >= 200 and resp.status_code <= 299):
            print("STATUS OK: {}".format(resp.status_code))
            return "Interface loopback 66070179 is shutdowned successfully"
        else:
            print('Error. Status Code: {}'.format(resp.status_code))
            return "Cannot shutdown: Interface loopback 66070179"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "Cannot shutdown: Interface loopback 66070179"


def status():
    api_url = what_ip(ip)
    resp = requests.get(
        api_url_status,
        auth=basicauth, 
        headers=headers, 
        verify=False
        )

    if(resp.status_code >= 200 and resp.status_code <= 299):
        print("STATUS OK: {}".format(resp.status_code))
        response_json = resp.json()
        admin_status = response_json["ietf-interfaces:interface"]["admin-status"]
        oper_status = response_json["ietf-interfaces:interface"]["oper-status"]
        if admin_status == 'up' and oper_status == 'up':
            return "Interface loopback 66070179 is enabled"
        elif admin_status == 'down' and oper_status == 'down':
            return "Interface loopback 66070179 is disabled"
    elif(resp.status_code == 404):
        print("STATUS NOT FOUND: {}".format(resp.status_code))
        return "No Interface loopback 66070179>"
    else:
        print('Error. Status Code: {}'.format(resp.status_code))
        return "No Interface loopback 66070179>"
