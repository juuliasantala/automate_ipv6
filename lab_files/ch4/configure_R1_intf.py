from ncclient import manager

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
            <name>1</name>
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
              <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3">
                <process>
                  <id>1</id>
                  <area>0</area>
                </process>
              </ospf>
            </ipv6>
          </GigabitEthernet>
          <GigabitEthernet>
            <name>2</name>
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

    R1 = "198.18.133.101"

    # TODO: Change the address and ND below to match what you marked in your address plan for
    # R1 GigabitEthernet 2
    R1_configuration = {"address": "2001:420:4021:1a47::1/64", "nd": "2001:420:4021:1a47::/64"}

    configure_ipv6_on_intf(R1, credentials["username"], credentials["password"],
                           R1_configuration["address"], R1_configuration["nd"])
