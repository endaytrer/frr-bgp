from mininet.node import UserSwitch
from mininet.node import Controller
from typing import Literal, NamedTuple
import pathlib
import os
import subprocess
Daemon = Literal["bgpd"]

def chown_recursive(dir: pathlib.Path, user: str, group: str):
    subprocess.run(["chown", "-R", f"{user}:{group}", str(dir)])
    
class FrrSwitch(UserSwitch):
    daemons: list[Daemon]
    config_path: pathlib.Path
    
    def __init__(self, name, config_dir: str | None = None, daemons: list[Daemon] = [], **params):
        if config_dir == None:
            config_path = pathlib.Path("config").joinpath(name)
        else:
            config_path = pathlib.Path(config_dir)
            
        if not config_path.exists():
            raise Exception(f"config path of {name} ({str(config_path)}) not exist!")
        self.config_path = config_path
        chown_recursive(config_path, "frr", "frr")
        super().__init__(name, privateDirs=[("/etc/frr", str(config_path)), "/run/frr"], **params)
        self.daemons = daemons
        self.controlIntf = None
        
    def start(self, controllers: list[Controller]):
        super().start(controllers)
        
        for daemon in ["zebra", "mgmtd", "staticd"]:
            self.cmd(f"/usr/libexec/frr/{daemon} -d")
            
        for daemon in self.daemons:
            self.cmd(f"/usr/libexec/frr/{daemon} -d")
    
        self.cmd("vtysh -b")
                
    def terminate(self):
        super().terminate()
        chown_recursive(self.config_path, "1000", "1000")
        
        
    
    def stop(self, deleteIntfs=True):
        for daemon in self.daemons:
            self.cmd(f"killall {daemon}")
            
        super().stop(deleteIntfs)
