from ncclient import manager

def enable_ipv6(device_ip, username, password, port=830, verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = """
        <config>
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <ipv6>
                    <unicast-routing/>
                    <router>
                        <ospf>
                            <id>1</id>
                        </ospf>
                    </router>
                </ipv6>
            </native>
        </config>
    """

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":
    devices = [
        "198.18.133.101",
        "198.18.11.2",
        "198.18.12.2"
    ]

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    for device in devices:
        enable_ipv6(device, credentials["username"], credentials["password"])
