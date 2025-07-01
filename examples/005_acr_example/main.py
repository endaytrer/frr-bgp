from mininet.topo import Topo
from frrnet import frrnet_main

class MyTopo(Topo):
    def build(self):
        a    = self.addSwitch("a",    dpid="51", daemons=["bgpd"])
        s    = self.addSwitch("s",    dpid="41", daemons=["bgpd"])
        c    = self.addSwitch("c",    dpid="31", daemons=["bgpd"])
        b    = self.addSwitch("b",    dpid="21", daemons=["bgpd"])
        
        popa = self.addHost("h1", ip="10.70.0.2/16", defaultRoute="via 10.70.0.1")
        dcn  = self.addHost("h2", ip="20.0.0.2/16",  defaultRoute="via 20.0.0.1")
        popb = self.addHost("h3", ip="10.0.0.2/16",  defaultRoute="via 10.0.0.1")
        
        self.addLink(a, popa)
        self.addLink(a, s)
        self.addLink(dcn, s)
        self.addLink(s, c)
        self.addLink(b, popb)
        self.addLink(b, c)

if __name__ == "__main__":
    frrnet_main(MyTopo)
    