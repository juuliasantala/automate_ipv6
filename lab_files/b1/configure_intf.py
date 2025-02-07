from ncclient import manager
import yaml
import jinja2

def read_configuration(config_file):
    # TODO 1: Read the contents of your YAML SoT file and return from the function a Python dictionary

def render_template(interfaces, template_name):
    # TODO 2: Open the Jinja2 template and read the contents to a jinja2.Template objects

    # TODO 3: Render the jinja2.Template object by passing the interfaces argument to the Jinja2
    # variable interfaces. Return the created configuration.

def configure_ipv6_on_intf(device_ip,
                           username,
                           password,
                           configuration,
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

    payload = configuration

    with manager.connect(**device, device_params={"name":"iosxe"},timeout=10) as connection:
        print("success!")
        response = connection.edit_config(target="running", config=payload)
        print(response)

if __name__ == "__main__":

    credentials = {
        "password": "C1sco12345",
        "username": "developer"
    }

    devices = read_configuration("sot.yaml")

    for device in devices.values():
        config = render_template(device["interfaces"], "interface_template.j2")
        configure_ipv6_on_intf(device["mgmt"], credentials["username"], credentials["password"],
                               config)