from typing import override
from mininet.topo import Topo

class FrrTopo(Topo):
    # Use a name-based port system
    # name_port_map[node_name][port_name] = port_number
    name_port_mapping: dict[str, set[str]] = {}
    
    def addNode(self, name, **opts):
        self.name_port_mapping[name] = set()
        return super().addNode(name, **opts)
    
    @override
    def addLink(self, node1: str, node2: str, intf1: str | None = None, intf2: str | None = None, bw: int | None = None, delay: str | None = None, key=None, **opts):
        if intf1 is not None and intf1 in self.name_port_mapping[node1]:
            raise Exception(f"intf1 {intf1} already used in node {node1}")
        
        if intf2 is not None and intf2 in self.name_port_mapping[node2]:
            raise Exception(f"intf2 {intf2} already used in node {node2}")
        
        ans = super().addLink(node1, node2, port1=None, port2=None, key=key, intfName1=intf1, intfName2=intf2, bw=bw, delay=delay, **opts)
        self.name_port_mapping[node1].add(intf1)
        self.name_port_mapping[node2].add(intf2)
        return ans
       