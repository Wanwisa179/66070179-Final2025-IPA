from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
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
