from pyats import aetest, topology

class PingTestcase(aetest.Testcase):
    '''
    Simple Testcase for checking connectivity from the network devices.
    '''

    @aetest.setup
    def connect(self, testbed):
        # TODO 1: Connect to your testbed and define a loop
        # where ping test is executed against each of the testbed devices
    
    @aetest.test
    def ping(self, steps, device, destinations):
        # TODO 2: Define the actual test where a ping is attempted from the
        # network device. Test passes if ping is successful and fails if ping
        # is unsuccessful

    @aetest.cleanup
    def disconnect(self, testbed):
        # TODO 3: Disconnect from the testbed devices

if __name__ == "__main__":

    my_destinations = # TODO 4: add two IPv6 addresses to ping - one for Aliisa or Bob and one towards Internet

    my_testbed = topology.loader.load("testbed.yaml")

    aetest.main(testbed=my_testbed,destinations=my_destinations)
