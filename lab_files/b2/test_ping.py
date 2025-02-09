import sys
from pyats import aetest, topology
import yaml

class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''

    @aetest.setup
    def connect(self, testbed, destinations_file):

        with open(destinations_file, encoding="utf-8") as file:
            self.destinations = yaml.safe_load(file.read())

        testbed.connect(log_stdout=False)
        aetest.loop.mark(self.ping, device=testbed)
    
    @aetest.test
    def ping(self, steps, device):
        for destination in self.destinations:
            with steps.start(
                f"Checking Ping from {device.hostname} to {destination}", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    step.failed(f'Ping {destination} from device {device.hostname} unsuccessful')
                else:
                    step.passed(f'Ping {destination} from device {device.hostname} successful')

    @aetest.cleanup
    def disconnect(self, testbed):
        testbed.disconnect()

if __name__ == "__main__":

    my_testbed = topology.loader.load("testbed.yaml")

    result = aetest.main(testbed=my_testbed, destinations_file="ping_destinations.yaml")
    if str(result) != "passed":
        sys.exit(1)

