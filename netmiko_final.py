from netmiko import ConnectHandler
from pprint import pprint

username = "admin"
password = "cisco"

def gigabit_status(ip):
    device_params = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": username,
        "password": password,
    }


    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("sh ip int br", use_textfsm=True)
        print(result)
        for intf in result:
            if "GigabitEthernet" in intf["interface"]:
                if ans == "" :
                    ans = intf["interface"]
                else:
                    ans += ", " + intf["interface"]
                if intf["status"] == "up":
                    up += 1
                    ans += " up"
                elif intf["status"] == "administratively down":
                    admin_down += 1
                    ans += " administratively down"
                elif intf["proto"] == "down":
                    down += 1
                    ans += " down"
        ans = ans + " -> " + str(up) + " up, " + str(down) + " down, " + str(admin_down) + " administratively down"
        pprint(ans)
        return ans
