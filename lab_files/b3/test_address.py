import ipaddress
from pyats import aetest
import yaml

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def read_configuration(self, config_file):

        with open(config_file, encoding="utf-8") as my_values:
            config = yaml.safe_load(my_values.read())

        aetest.loop.mark(InterfaceConfigAnalysis, device=config.items())

class InterfaceConfigAnalysis(aetest.Testcase):

    @aetest.setup()
    def mark_interfaces_for_looping(self, device):
    
        aetest.loop.mark(self.validate_address, interface=device[1]["interfaces"])

    @aetest.test
    def validate_address(self, steps, device, interface):

        try:
            addresses = interface["ipv6_address"]
            subnet = interface["nd_prefix"]
        except KeyError:
            self.skipped(f"No IPv6 address configured on {device[0]} {interface}")

        for address in addresses:
            with  steps.start(f"Validating IP address {address} for {interface}", continue_=False) as step:
                try:
                    address_without_prefix = address.split("/")[0]
                    ipaddress.IPv6Address(address_without_prefix)
                except Exception as err:
                    step.failed(f"{address} is not a valid ip address: {err}")
                else:
                    step.passed(f"{address} is a valid ip address")

            with  steps.start(f"Validating subnet for IP address {address}", continue_=True) as step:

                is_in_network = ipaddress.IPv6Address(address_without_prefix) in ipaddress.IPv6Network(subnet)

                if is_in_network:
                    step.passed(f"{address} is in {subnet}")
                else:
                    step.failed(f"{address} NOT in {subnet}")

if __name__ == "__main__":

    aetest.main(config_file="sot.yaml")
