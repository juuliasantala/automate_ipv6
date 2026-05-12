from netmiko import ConnectHandler

R1 = {
    "device_type": "cisco_xe",
    "host": "198.18.133.101",
    "username": "developer",
    "password": "C1sco12345",
}


def main():
    print(f"Connecting to R1 ({R1['host']})...", end=" ")
    with ConnectHandler(**R1) as connection:
        print("success!")

        # TODO 1 - read the running config and confirm IPv6 unicast routing
        # is enabled. Use connection.send_command("show running-config | "
        # "include ipv6 unicast-routing"), then check the returned string.

        # TODO 2 - push a harmless change (snmp-server location) using
        # connection.send_config_set([...]) and then re-read the running
        # config to verify it landed.


if __name__ == "__main__":
    main()
