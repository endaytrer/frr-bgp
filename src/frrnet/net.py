from mininet.net import Mininet
from mininet.node import Host
from mininet.link import Link, Intf
from frrnet.node import FrrSwitch


class FrrNet(Mininet):
    def __init__(self, topo=None, switch=FrrSwitch, host=Host, controller=None, link=Link, intf=Intf, build=True, xterms=False, cleanup=False, ipBase='10.0.0.0/8', inNamespace=True, autoSetMacs=True, autoStaticArp=False, autoPinCpus=False, listenPort=None, waitConnected=False):
        super().__init__(topo, switch, host, controller, link, intf, build, xterms, cleanup, ipBase, inNamespace, autoSetMacs, autoStaticArp, autoPinCpus, listenPort, waitConnected)
        
    def configureControlNetwork(self):
        pass