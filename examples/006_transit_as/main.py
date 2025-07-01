from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        r1 = self.addSwitch("r1", daemons=["bgpd"])
        isp1 = self.addSwitch("isp1", daemons=["bgpd"])
        isp2 = self.addSwitch("isp2", daemons=["bgpd"])
        
        self.addLink(r1, isp1)
        self.addLink(r1, isp2)
        

if __name__ == "__main__":
    frrnet_main(MyTopo)