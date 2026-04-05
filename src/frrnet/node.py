from mininet.node import Switch
from mininet.node import Controller
from typing import Literal
import pathlib
import os
import sys
import subprocess
Daemon = Literal["bgpd"]

FRR_SEARCH_PATH = ["/usr/libexec/frr", "/usr/lib/frr", "/usr/lib64/frr", "/usr/local/libexec/frr", "/usr/local/lib/frr", "/usr/local/lib64/frr"]

def find_frr_daemons() -> pathlib.Path:
    for path in FRR_SEARCH_PATH:
        if os.path.exists(pathlib.Path(path) / "zebra"):
            return pathlib.Path(path)
    raise Exception("frr daemons not found")

def chown_recursive(dir: pathlib.Path, user: str, group: str):
    subprocess.run(["chown", "-R", f"{user}:{group}", str(dir)])

class FrrSwitch(Switch):
    daemons: list[Daemon]
    config_path: pathlib.Path
    
    def __init__(self, name, config_file: str | None = None, daemons: list[Daemon] = [], **params):
        if config_file == None:
            config_dir = pathlib.Path(sys.argv[0]).parent.joinpath("config")
            if os.path.exists(os.path.join(config_dir, name + ".cfg")):
                config_file = config_dir.joinpath(name + ".cfg")
            else:
                config_file = config_dir.joinpath(name + ".conf")
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
        self.daemons = ["zebra", "mgmtd", "staticd", *daemons]
        self.controlIntf = None
        
    def start(self, _controllers: list[Controller]):
        prefix = find_frr_daemons()
            
        for daemon in self.daemons:
            daemon_exe = prefix / daemon
            self.cmd(f"{daemon_exe} -d")
        
        # To increase throughput, enable multipath hash policy for ipv4 and ipv6
        self.cmd("sysctl -w net.ipv4.fib_multipath_hash_policy=1")
        self.cmd("sysctl -w net.ipv6.fib_multipath_hash_policy=1")
    
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
