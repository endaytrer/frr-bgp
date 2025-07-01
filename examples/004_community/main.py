from frrnet import frrnet_main
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        
        h1 = self.addHost("h1", ip="10.10.10.10/24", defaultRoute="via 10.10.10.1")
        
        customer = self.addSwitch("customer", dpid="10", daemons=["bgpd"])
        isp1 = self.addSwitch("isp1", daemons=["bgpd"])
        isp2 = self.addSwitch("isp2", daemons=["bgpd"])
        isp3 = self.addSwitch("isp3", daemons=["bgpd"])
        
        self.addLink(isp1, isp2)
        self.addLink(isp1, isp3)
        self.addLink(customer, isp1)
        self.addLink(h1, customer)


if __name__ == "__main__":
    frrnet_main(MyTopo)
        