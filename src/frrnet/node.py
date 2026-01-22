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
    
    def __init__(self, name, config_file: str | None = None, daemons: list[Daemon] = [], **params):
        if config_file == None:
            if os.path.exists(os.path.join("config", name + ".cfg")):
                config_file = pathlib.Path("config").joinpath(name + ".cfg")
            else:
                config_file = pathlib.Path("config").joinpath(name + ".conf")
        else:
            config_file = pathlib.Path(config_file)
            
        if not config_file.exists():
            raise Exception(f"config path of {name} ({str(config_file)}) not exist!")
        
        # create a temp directory for each switch
        config_path = pathlib.Path("/tmp").joinpath("frrnet").joinpath(name)
        config_path.mkdir(parents=True, exist_ok=True)
        subprocess.run(["cp", str(config_file), str(config_path.joinpath("frr.conf"))])
        subprocess.run(["touch", str(config_path.joinpath("vtysh.conf"))])
        
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
        # remove the temp directory
        if self.config_path.exists():
            subprocess.run(["rm", "-rf", str(self.config_path)])
        
        
    
    def stop(self, deleteIntfs=True):
        for daemon in self.daemons:
            self.cmd(f"killall {daemon}")
            
        super().stop(deleteIntfs)
