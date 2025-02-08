import ipaddress
from pyats import aetest
import yaml

class CommonSetup(aetest.CommonSetup):
    """
    Common setup is ran once during the test execution.
    """

    @aetest.subsection
    def read_configuration(self, config_file):
        """
        This method reads configuration from a YAML file, and then
        marks the returned devices for looping.
        """

        with open(config_file, encoding="utf-8") as my_values:
            config = yaml.safe_load(my_values.read())

        aetest.loop.mark(InterfaceConfigAnalysis, device=config.items())

class InterfaceConfigAnalysis(aetest.Testcase):

    @aetest.setup()
    def mark_interfaces_for_looping(self, device):
        """
        This setup method takes the device's interfaces and marks those for
        looping for the validation tasks.
        """    
        aetest.loop.mark(self.validate_address, interface=device[1]["interfaces"])

    @aetest.test
    def validate_address(self, steps, device, interface):

        # TO DO 3: If the interface does not have IPv6 address configured, mark the test skipped with
        # self.skipped("my message")
        addresses = interface["ipv6_address"]
        subnet = interface["nd_prefix"]

        for address in addresses:
            with  steps.start(f"Validating IP address {address} for {interface}", continue_=False) as step:

                # TO DO 1: Try creating an ipaddress.IPv6Address object out of the interface's IPv6 address.
                # If the creation of the object fails, the address is not valid and the step should be failed
                # with an appropriate message.

            with  steps.start(f"Validating subnet for IP address {address}", continue_=True) as step:
                # TO DO 2: Check if the IPv6Address object in the IPv6Network(subnet) object.
                # If the result is True, the address is in the subnet and the step should be passed.
                # If the result is False, the step should be failed with an appropriate message.

if __name__ == "__main__":

    aetest.main(config_file="sot.yaml")
