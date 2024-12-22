#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python sample script for updating interface configuration with RESTCONF.

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
import jinja2

__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"
__copyright__ = "Copyright (c) 2024 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Following line disables warnings of the unverified certificate. Do not use in production!
urllib3.disable_warnings()

def render_template(interfaces:list, template_name:str):
    with open(f"templates/{template_name}", encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())
    configuration = template.render(interfaces=interfaces)
    print(f"Configuration to be sent: \n {configuration}")
    return configuration

def configure_interfaces(device_ip:str, username:str, password:str,
                        configuration:list,
                        port:int=443, verify:bool=False)->None:
    '''
    Function to configure interface on an IOS XE device using RESTCONF.
    '''
    print(f"Configuring interfaces on {device_ip}...", end=" ")

    url = f"https://{device_ip}:{port}/restconf/data/Cisco-IOS-XE-native:native/interface"
    header = {"Content-Type": "application/yang-data+json"}
    payload = render_template(interfaces=configuration, template_name="interface_ipv6.j2")

    response = requests.patch(url, headers=header, auth=(username, password),
                              data=payload, verify=verify)

    if response.ok:
        print("Success!")
    else:
        print("Error!")
        print(response.text)

def get_inventory(inventory_file:str = "devices.yaml"):

    with open(inventory_file, encoding="utf-8") as my_inventory:
        inventory = yaml.safe_load(my_inventory.read())

    user, pw, devices = (
        inventory["default_creds"]["username"],
        inventory["default_creds"]["password"],
        inventory["devices"])
    
    return user, pw, devices

def read_configuration_template(config_file: str="ipv6_config.yaml"):
    with open(config_file, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    return config["devices"]

def main():
    user, pw, devices = get_inventory()
    devices_config = read_configuration_template()

    print("# Enabling IPv6 for devices")
    for device, config in devices_config.items():
        if config.get("ipv6").get("enabled"):
            print("\n#######\n")
            configure_interfaces(
                device_ip=devices[device],
                username=user,
                password=pw,
                configuration=config["interfaces"]
            )

if __name__ == "__main__":
    main()