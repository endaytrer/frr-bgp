from frrnet import frrnet_main
from mininet.topo import Topo


class MyTopo(Topo):
    def build(self):
        h1 = self.addHost("h1", ip="1.1.1.1/24", defaultRoute="via 1.1.1.2")
        r1 = self.addSwitch("r1", daemons=["bgpd"])
        r2 = self.addSwitch("r2", daemons=["bgpd", "ospfd"])
        r3 = self.addSwitch("r3", daemons=["bgpd", "ospfd"])
        r4 = self.addSwitch("r4", daemons=["bgpd", "ospfd"])
        r5 = self.addSwitch("r5", daemons=["bgpd"])
        h5 = self.addHost("h5", ip="5.5.5.5/24", defaultRoute="via 5.5.5.2")
        
        self.addLink(r1, r2)
        self.addLink(r2, r3)
        self.addLink(r4, r3)
        self.addLink(r5, r4)
        
        self.addLink(h1, r1)
        self.addLink(h5, r5)
        
if __name__ == "__main__":
    frrnet_main(MyTopo)