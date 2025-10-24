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


def net_enable(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070179</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """
    try:
        with netconf_connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if '<ok/>' in reply.xml:
                return "Interface loopback 66070179 is enabled successfully using Netconf"
            else:
                return "Cannot enable: Interface loopback 66070179 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)
        return "Cannot enable: Interface loopback 66070179 (checked by Netconf)"

def net_disable(ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070179</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """
    try:
        with netconf_connect(ip) as m:
            reply = m.edit_config(target="running", config=netconf_config)
            if '<ok/>' in reply.xml:
                return "Interface loopback 66070179 is shutdowned successfully using Netconf"
            else:
                return "Cannot shutdown: Interface loopback 66070179 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)
        return "Cannot shutdown: Interface loopback 66070179 (checked by Netconf)"

# def netconf_edit_config(netconf_config):
#     return  m.<!!!REPLACEME with the proper Netconf operation!!!>(target="<!!!REPLACEME with NETCONF Datastore!!!>", config=<!!!REPLACEME with netconf_config!!!>)


def net_status(ip):
    netconf_filter = """
    <filter>
      <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070179</name>
        </interface>
      </interfaces-state>
    </filter>
    """
    try:
        with netconf_connect(ip) as m:
            reply = m.get(netconf_filter)
            reply_dict = xmltodict.parse(reply.xml)
            interface_data = reply_dict.get('rpc-reply', {}).get('data', {}).get('interfaces-state', {}).get('interface')
            
            if interface_data:
                admin_status = interface_data.get('admin-status')
                oper_status = interface_data.get('oper-status')
                if admin_status == "up" and oper_status == "up":
                    return "Interface loopback 66070179 is enabled (checked by Netconf)"
                elif admin_status == "down" and oper_status == "down":
                    return "Interface loopback 66070179 is disabled (checked by Netconf)"
            else:
                return "No Interface loopback 66070179 (checked by Netconf)"
    except Exception as e:
        print("Error:", e)
        return "No Interface loopback 66070179 (checked by Netconf)"