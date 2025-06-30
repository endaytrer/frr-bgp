#!/usr/bin/env python3
from frrnet import frrnet_main
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class MyTopo(Topo):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
        leftHost = self.addHost('h1', ip="192.168.1.2/24", defaultRoute="via 192.168.1.1")
        leftSwitch = self.addSwitch('s1', daemons=["bgpd"])
        rightSwitch = self.addSwitch('s2', daemons=["bgpd"])
        rightHost = self.addHost('h2', ip="192.168.2.2/24", defaultRoute="via 192.168.2.1")

        # Add links
        self.addLink(leftSwitch, rightSwitch)
        self.addLink(leftHost, leftSwitch)
        self.addLink(rightHost, rightSwitch)

    
if __name__ == "__main__":
    frrnet_main(MyTopo)