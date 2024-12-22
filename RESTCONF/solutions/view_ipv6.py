#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for viewing IPv6 configuration with RESTCONF.

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

import pprint # for prettier JSON indentation
import requests
import urllib3
import yaml

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def view_ipv6(device_ip:str, username:str, password:str, port:int=443, verify:bool=False)->None:
    '''
    Function to view IPv6 configuration on an IOS XE device using RESTCONF.
    '''
    print(f"Retrieving IPv6 configuration from device {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/ipv6/"
    header = {"Accept": "application/yang-data+json"}

    response = requests.get(url, headers=header,
                            auth=(username, password),
                            verify=verify, timeout=10)
    if response.status_code == 200:
        print("IPv6 configured!")
        print("Configuration:")
        pprint.pprint(response.json())
    elif response.status_code == 204:
        print("No IPv6 configuration present!")
    else:
        print("Error in retrieving IPv6 configuration!")
        print(response.text)

def get_inventory(inventory_file:str = "devices.yaml"):

    with open(inventory_file, encoding="utf-8") as my_inventory:
        inventory = yaml.safe_load(my_inventory.read())

    user, pw, devices = (
        inventory["default_creds"]["username"],
        inventory["default_creds"]["password"],
        inventory["devices"])
    
    return user, pw, devices

def main():
    user, pw, devices = get_inventory()

    print("# Retrieving IPv6 configuration from devices")
    for name, ip in devices.items():
        print("\n#######\n")
        print(f"Device: {name}, ip: {ip}")
        view_ipv6(ip, user, pw)

if __name__ == "__main__":
    main()