from frrnet import frrnet_main
from mininet.topo import Topo


class MyTopo(Topo):
    def build(self):
        r1 = self.addSwitch("r1", daemons=["bgpd"])
        r2 = self.addSwitch("r2", daemons=["bgpd"])
        r3 = self.addSwitch("r3", daemons=["bgpd"])
        r4 = self.addSwitch("r4", daemons=["bgpd"])
        
        self.addLink(r1, r2)
        self.addLink(r1, r3)
        self.addLink(r2, r4)
        self.addLink(r3, r4)

if __name__ == "__main__":
    frrnet_main(MyTopo)