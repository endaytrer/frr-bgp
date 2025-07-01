from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        r1 = self.addSwitch("r1", daemons=["ospfd", "bgpd"])
        r2 = self.addSwitch("r2", daemons=["ospfd", "bgpd"])
        r3 = self.addSwitch("r3", daemons=["ospfd", "bgpd"])
        
        self.addLink(r1, r2)
        self.addLink(r2, r3)

if __name__ == "__main__":
    frrnet_main(MyTopo)