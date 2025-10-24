from netmiko import ConnectHandler
from pprint import pprint
import re


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

def read_motd(ip):
    device_params = {
        "device_type": "cisco_ios",
        "ip": ip,
        "username": "admin",
        "password": "cisco",
    }

    try:
        with ConnectHandler(**device_params) as ssh:
            # ✅ ดึงทั้ง config เลย ไม่ใช้ section/begin
            output = ssh.send_command("show running-config")
            print("DEBUG RAW OUTPUT:\n", repr(output))

            # ✅ หาส่วน banner motd แบบแน่นอน
            match = re.search(
                r"banner motd\s*\^C\s*([\s\S]*?)\s*\^C",
                output,
                re.MULTILINE
            )

            if match:
                motd_text = match.group(1).strip()
                if motd_text:
                    return motd_text
                else:
                    return "Error: No MOTD Configured"
            else:
                return "Error: No MOTD Configured"

    except Exception as e:
        print("Error:", e)
        return "Error: Cannot read MOTD"
