from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        r1 = self.addSwitch("r1", daemons=["ospfd", "bgpd"])
        r2 = self.addSwitch("r2", daemons=["ospfd", "bgpd"])
        r3 = self.addSwitch("r3", daemons=["ospfd", "bgpd"])
        r4 = self.addSwitch("r4", daemons=["ospfd", "bgpd"])
        r5 = self.addSwitch("r5", daemons=["ospfd", "bgpd"])
        r6 = self.addSwitch("r6", daemons=["bgpd"])
        
        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r2, r3)
        self.addLink(r4, r5)
        self.addLink(r2, r4)
        self.addLink(r3, r5)
        self.addLink(r4, r6)
        self.addLink(r5, r6)


if __name__ == "__main__":
    frrnet_main(MyTopo)