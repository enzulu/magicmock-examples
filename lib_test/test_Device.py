import unittest
import sys
from IPy import IP
from context import Device

class TestDeviceIpAddresses(unittest.TestCase):
    def isIPValid(self,IP_string):
        try:
           IP(IP_string)
        except ValueError:
            raise
            return False
        except:
            print "Unexpected Error:", sys.exc_info()[0]
            raise
        else:
            return True
    
    def test_TT_IP_LIST(self):
        for each_IP in Device.TT_IP_LIST:
            self.assertTrue(self.isIPValid(each_IP))
    
    def test_FSM_FSP_IP(self):
        self.assertTrue(self.isIPValid(Device.IP_FSM_FSP1))
        self.assertTrue(self.isIPValid(Device.IP_FSM_FSP2))
        self.assertTrue(self.isIPValid(Device.IP_FSM_FSP3))
        
    def test_FBIP_LIST(self):
        for each_IP in Device.FBIP_LIST:
            self.assertTrue(self.isIPValid(each_IP))
    
    def test_PORTS(self):
        ALL_THE_PORTS = [Device.PORT_15001,
                         Device.PORT_15002,
                         Device.PORT_15003,
                         Device.PORT_16008,
                         Device.PORT_12005,
                         Device.PORT_12006,
                         Device.PORT_12007,
                         Device.PORT_12008,
                         Device.PORT_12009,
                         Device.PORT_12010,
                         Device.PORT_5001,
                         Device.PORT_SSH,
                         Device.PORT_FTP,
                         Device.PORT_TELNET]
    
        # check if all ports are unique (no duplicate ports)
        self.assertTrue(len(ALL_THE_PORTS) == len(set(ALL_THE_PORTS)),
                        msg="Not all ports are unique")
        
        for each_PORT in ALL_THE_PORTS:
            self.assertTrue(0 < each_PORT < 65535)
