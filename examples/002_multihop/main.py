#!/usr/bin/env python3
from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):

    def build( self ):

        # Add hosts and switches
        h1 = self.addHost("h1", ip="1.1.1.2/24", defaultRoute="via 1.1.1.1")
        r1 = self.addSwitch('r1', daemons=["bgpd"])
        r2 = self.addSwitch('r2')
        r3 = self.addSwitch('r3', daemons=["bgpd"])
        h3 = self.addHost("h3", ip="3.3.3.2/24", defaultRoute="via 3.3.3.3")

        # Add links
        self.addLink(r1, r2)
        self.addLink(r2, r3)
        self.addLink(h1, r1)
        self.addLink(h3, r3)


    
if __name__ == "__main__":
    frrnet_main(MyTopo)