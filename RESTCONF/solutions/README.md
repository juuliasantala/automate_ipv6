# Instructions for running the scripts

1. install requirements from parent folder
    ```bash
    pip install -r requirements.txt
    ```
1. review whether IPv6 is currently enabled in the environment:
    ```bash
    $ python view_ipv6.py 
    # Retrieving IPv6 configuration from devices

    #######

    Device: R1, ip: 198.18.133.101
    Retrieving IPv6 configuration from device 198.18.133.101... IPv6 configured!
    Configuration:
    {'Cisco-IOS-XE-native:ipv6': {'router': {'ospf': [{'id': 1}]},
                                'unicast-routing': [None]}}

    #######

    Device: R2, ip: 198.18.7.2
    <output omitted>
    ```
1. Enable IPv6 in all devices:
    ```bash
    $ python enable_ipv6.py 
    # Enabling IPv6 for devices

    #######

    Enabling IPv6 on device 198.18.133.101... Configuration to be sent: 
    
    {
        "Cisco-IOS-XE-native:ipv6": {
            "unicast-routing": [null]
        }
    }
    Device configured successfully!

    #######

    Enabling IPv6 on device 198.18.7.2... Configuration to be sent: 
    
    {
        "Cisco-IOS-XE-native:ipv6": {
            "unicast-routing": [null]
        }
    }
    Device configured successfully!

    #######

    <output omitted>
    ```
1. View current interface IPv6 configuration:
    ```bash
    $ python view_interface_config.py 
    # Retrieving interface configuration from devices

    #######

    Device: R1, ip: 198.18.133.101
    Retrieving interface operational data from device 198.18.133.101... Success!
    Retrieving interface configuration from device 198.18.133.101... Success!

    GigabitEthernet 1 (Description: 'VLAN-PRIMARY')
    - IPv4 address present!
    - Configured address: {'primary': {'address': '198.18.133.101', 'mask': '255.255.192.0'}}
    - Actual address: 198.18.133.101
    - IPv6 enabled!
    - Configured address: {'link-local-address': [{'address': 'fe80::66', 'link-local': [None]}]}

    <output omitted>
    ```

1. Enable IPv6 on interfaces (all except R1 G1! Need to add rest of that configuration to the environment...)
    ```bash
    $ python update_interface_config.py 
    # Enabling IPv6 for devices

    #######

    Configuring interfaces on 198.18.133.101... Configuration to be sent: 
    
    {
        "Cisco-IOS-XE-native:interface": {

    <output omitted>
    ```

1. Enable OSPFv3 on the routers
    ```bash
    $ python update_ospfv3_config.py
    # Enabling Ospfv3 for devices

    #######

    Configuring ospfv3 on 198.18.133.101... Configuration to be sent: 
    
    {
        "Cisco-IOS-XE-native:ipv6": {
            "router": {
                "ospf": [
                    {
                        "id": 1
                    }
                ]
            }
        }
    }
    Success!

    #######

    <output omitted>
    ```

1. Enable OSPFv3 on the interfaces
    ```bash
    $ python update_interface_ospfv3.py 
    # Enabling OSPFv3 for interfaces
    Device: R1 198.18.133.101

    #######

    Configuring interfaces GigabitEthernet 5... Configuration to be sent: 
    

    {
        "Cisco-IOS-XE-ospfv3:ospf": {
            "process": {
                "id": 1,
                "area": 0
            },
            "priority": 0
        }
    }
    Success!
    Device: R2 198.18.7.2

    #######

    <output omitted>
    ```