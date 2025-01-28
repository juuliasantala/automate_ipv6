from ncclient import manager

def configure_ipv6_on_intf(device_ip, username, password, port=830, verify=False):

    print(f"\nConnecting to device {device_ip}...", end=" ")

    device = {
        "host": device_ip,
        "port": port,
        "username": username,
        "password": password,
        "hostkey_verify": verify
    }

    payload = """

    TODO 1: ADD YOUR PAYLOAD HERE!

    """

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = #TODO 2: send the configuration payload to running datastore using edit_config
        print(response)

if __name__ == "__main__":
    device = "198.18.7.2" #R2

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    configure_ipv6_on_intf(device, credentials["username"], credentials["password"])
