from ncclient import manager
import xmltodict

def netconf_connect(ip):
    return manager.connect(
        host=ip,
        port=830,
        username="admin",
        password="cisco",
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False
    )

def net_create(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070179</name>
          <description>My final2024 loopback</description>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
            ianaift:softwareLoopback
          </type>
          <enabled>true</enabled>
          <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>172.1.79.1</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ipv4>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with netconf_connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if '<ok/>' in reply.xml:
                return "Interface loopback 66070179 is created successfully using Netconf"
            else:
                return "Cannot create: Interface loopback 66070179 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)
        return "Cannot create: Interface loopback 66070179 (checked by Netconf)"


def net_delete(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
          <name>Loopback66070179</name>
        </interface>
      </interfaces>
    </config>
    """
    try:
        with netconf_connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if '<ok/>' in reply.xml:
                return "Interface loopback 66070179 is deleted successfully using Netconf"
            else:
                return "Cannot delete: Interface loopback 66070179 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)
        return "Cannot delete: Interface loopback 66070179 (checked by Netconf)"


# def net_enable():
#     netconf_config = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         netconf_reply = netconf_edit_config(netconf_config)
#         xml_data = netconf_reply.xml
#         print(xml_data)
#         if '<ok/>' in xml_data:
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#         print("Error!")


# def net_disable():
#     netconf_config = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         netconf_reply = netconf_edit_config(netconf_config)
#         xml_data = netconf_reply.xml
#         print(xml_data)
#         if '<ok/>' in xml_data:
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#         print("Error!")

# def netconf_edit_config(netconf_config):
#     return  m.<!!!REPLACEME with the proper Netconf operation!!!>(target="<!!!REPLACEME with NETCONF Datastore!!!>", config=<!!!REPLACEME with netconf_config!!!>)


# def net_status():
#     netconf_filter = """<!!!REPLACEME with YANG data!!!>"""

#     try:
#         # Use Netconf operational operation to get interfaces-state information
#         netconf_reply = m.<!!!REPLACEME with the proper Netconf operation!!!>(filter=<!!!REPLACEME with netconf_filter!!!>)
#         print(netconf_reply)
#         netconf_reply_dict = xmltodict.<!!!REPLACEME with the proper method!!!>(netconf_reply.xml)

#         # if there data return from netconf_reply_dict is not null, the operation-state of interface loopback is returned
#         if <!!!REPLACEME with the proper condition!!!>:
#             # extract admin_status and oper_status from netconf_reply_dict
#             admin_status = <!!!REPLACEME!!!>
#             oper_status = <!!!REPLACEME !!!>
#             if admin_status == 'up' and oper_status == 'up':
#                 return "<!!!REPLACEME with proper message!!!>"
#             elif admin_status == 'down' and oper_status == 'down':
#                 return "<!!!REPLACEME with proper message!!!>"
#         else: # no operation-state data
#             return "<!!!REPLACEME with proper message!!!>"
#     except:
#        print("Error!")
