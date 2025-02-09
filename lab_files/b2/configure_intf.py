from ncclient import manager
import yaml
import jinja2

def read_configuration_template(config_file):
    with open(config_file, encoding="utf-8") as my_values:
        config = yaml.safe_load(my_values.read())
    return config

def render_template(interfaces, template_name):
    with open(template_name, encoding="utf-8") as my_template:
        template = jinja2.Template(my_template.read())

    configuration = template.render(interfaces=interfaces)
    return configuration

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

    config_values = read_configuration_template("sot.yaml")

    for values in config_values.values():
        config = render_template(values["interfaces"], "interface_template.j2")
        configure_ipv6_on_intf(values["mgmt"], credentials["username"], credentials["password"],
                               config)