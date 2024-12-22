#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing interface configuration with RESTCONF.

------------

Copyright (c) 2024 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import requests
import urllib3
import yaml

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def get_interface_oper(device_ip:str, username:str, password:str,
                          port:int=443, verify:bool=False,
                          interface_type:str="GigabitEthernet")->dict:

    print(f"Retrieving interface operational data from device {device_ip}...", end=" ")

    header = {"Accept": "application/yang-data+json"}
    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-interfaces-oper:interfaces/interface"
    response = requests.get(url, headers=header,
                            auth=(username, password),
                            verify=verify, timeout=10)

    operational_interfaces = {}
    if response.status_code == 200:
        print("Success!")
        for interface in response.json()["Cisco-IOS-XE-interfaces-oper:interface"]:
            operational_interfaces[interface["name"]] = {
                "ipv4": interface["ipv4"] if "ipv4" in interface else None,
                "ipv6": interface["ipv6-addrs"] if "ipv6-addrs" in interface else None
            }

    else:
        print("Error in retrieving operational interface configuration!")
        print(response.text)
    
    return operational_interfaces


def get_interface_config(device_ip:str, username:str, password:str,
                          port:int=443, verify:bool=False,
                          interface_type:str="GigabitEthernet")->list:
    '''
    Function to view interface configuration on an IOS XE device using RESTCONF.
    '''
    print(f"Retrieving interface configuration from device {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface/{interface_type}"
    header = {"Accept": "application/yang-data+json"}

    response = requests.get(url, headers=header,
                                auth=(username, password),
                                verify=verify, timeout=10)

    if response.status_code == 200:
        print("Success!")
        return response.json()[f"Cisco-IOS-XE-native:{interface_type}"]
    else:
        print("Error in retrieving configured interface configuration!")
        print(response.text)

def view_interface_config(interface_configuration:list,
                          interface_oper:dict,
                          interface_type:str="GigabitEthernet")->None:
    '''
    Function to view interface configuration on an IOS XE device using RESTCONF.
    '''
    for interface in interface_configuration:
        interface_number = interface['name']
        print(f"\n{interface_type} {interface_number} (Description: '{interface.get('description')}')")
        if "ip" in interface:
            print("- IPv4 address present!")
            print(f"  - Configured address: {interface.get('ip').get('address')}")
            print(f"  - Actual address: {interface_oper[f'{interface_type}{interface_number}']['ipv4']}")
        else:
            print("- No IPv4 address configured!")

        if "ipv6" in interface:
            ipv6_addresses = interface_oper[f'{interface_type}{interface_number}']['ipv6']
            print("- IPv6 enabled!")
            print(f'  - Configured address: {interface.get("ipv6").get("address")}')
            print(f'  - Configured neighbor discovery: {interface.get("ipv6").get("nd")}')
            print(f'  - Configured OSPFv3: {interface.get("ipv6").get("Cisco-IOS-XE-ospfv3:ospf")}')
            print(f"  - Actual address: {', '.join(ipv6_addresses) if ipv6_addresses else None}")
            
        else:
            print("- No IPv6 address configured!")

def get_inventory(inventory_file:str = "devices.yaml"):

    with open(inventory_file, encoding="utf-8") as my_inventory:
        inventory = yaml.safe_load(my_inventory.read())

    user, pw, devices = (
        inventory["default_creds"]["username"],
        inventory["default_creds"]["password"],
        inventory["devices"])
    
    return user, pw, devices

if __name__ == "__main__":

    user, pw, devices = get_inventory()

    print("# Retrieving interface configuration from devices")
    for name, ip in devices.items():
        print("\n#######\n")
        print(f"Device: {name}, ip: {ip}")
        oper = get_interface_oper(ip, user, pw)
        config = get_interface_config(ip, user, pw)
        view_interface_config(config, oper)
