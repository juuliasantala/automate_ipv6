# TODO 1: add the import for ncclient manager

def configure_ipv6_on_intf(device_ip,
                           username,
                           password,
                           ipv6_address,
                           nd_prefix,
                           port=830,
                           verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = f"""
    <config>
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>4</name>
            <ipv6>
              <enable/>
              <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3">
                <process>
                  <id>1</id>
                  <area>0</area>
                </process>
              </ospf>
            </ipv6>
          </GigabitEthernet>
          <GigabitEthernet>
            <name>5</name>
            <ipv6>
              <enable/>
              <address>
                <prefix-list>
                  <prefix>{ipv6_address}</prefix>
                </prefix-list>
              </address>
              <nd>
                <prefix xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-nd">
                  <ipv6-prefix-list>
                    <ipv6-prefix>{nd_prefix}</ipv6-prefix>
                  </ipv6-prefix-list>
                </prefix>
              </nd>
              <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3">
                <process>
                  <id>1</id>
                  <area>0</area>
                </process>
              </ospf>
            </ipv6>
          </GigabitEthernet>
        </interface>
      </native>
    </config>
    """

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    # TODO 2: Define the variable(s) R3 and R4 IPv4 address (for NETCONF connection) and the configuration
    # details for IPv6 address and ND prefix. You can do this in your preferred way - for example, with
    # separate variable for each, or with a structure such as list and/or dictionary

    # TODO 3: Call the configure_ipv6_on_intf function two times - once for R3 and once for R4. You can do this
    # in your preferred way - for example, by literally calling the function two times with different
    # arguments, or for example by using a for loop