from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        h1 = self.addHost("h1", ip="11.11.11.11/24", defaultRoute="via 11.11.11.1")
        r1 = self.addSwitch("r1", daemons=["bgpd"])
        r2 = self.addSwitch("r2", daemons=["ospfd", "bgpd"])
        r3 = self.addSwitch("r3", daemons=["ospfd", "bgpd"])
        r4 = self.addSwitch("r4", daemons=["ospfd", "bgpd"])
        r5 = self.addSwitch("r5", daemons=["ospfd", "bgpd"])
        h5 = self.addHost("h5", ip="55.55.55.55/24", defaultRoute="via 55.55.55.1")
        
        self.addLink(r1, r2)
        self.addLink(r2, r3)
        self.addLink(r2, r4)
        self.addLink(r3, r5)
        self.addLink(r4, r5)
        
        self.addLink(r1, h1)
        self.addLink(r5, h5)

if __name__ == "__main__":
    frrnet_main(MyTopo)