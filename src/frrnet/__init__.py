from mininet.topo import Topo
from mininet.log import setLogLevel
from frrnet.cli import FrrCLI
from frrnet.net import FrrNet
from typing import Type, TypeVar

T = TypeVar("T", bound=Topo)
def frrnet_main(TopoClass: Type[T]):
    setLogLevel("info")
    topo = TopoClass()
    
    net = FrrNet(topo)
    
    net.start()
    FrrCLI(net)
    net.stop()
    