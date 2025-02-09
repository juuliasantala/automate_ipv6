from ncclient import manager

def delete_ipv6_from_intf(device_ip,
                           username,
                           password,
                           interface,
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
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
          <GigabitEthernet>
            <name>{interface}</name>
            <ipv6 nc:operation="delete" />
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

    import sys

    try:
        device = sys.argv[1]
        interface_number = sys.argv[2]
    except:
        print("Please provide the cli arguments 'device' and 'interface' number.")
        print("For example:")
        print("python delete_ipv6_from_interface.py R3 5")
        sys.exit(1)

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    devices = {
        "R2": "198.18.7.2",
        "R3": "198.18.11.2",
        "R4": "198.18.12.2"
    }

    try:
        target_device = devices[device]
    except:
        print("Device must be R2, R3 or R4")
        sys.exit(1)


    delete_ipv6_from_intf(target_device, credentials["username"], credentials["password"],
                           interface=interface_number)
