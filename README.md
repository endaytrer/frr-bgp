# frrnet

> [!WARNING]
> This is only for learning purposes, not ready for production.

`frrnet` is a network emulation tool that uses [Mininet](https://github.com/mininet/mininet) and [FRRouting](https://frrouting.org/). 

### Get started

First, install FRR and Mininet locally.

```bash
# Fedora / RHEL
sudo dnf install frr mininet

# Debian / Ubuntu
curl -s https://deb.frrouting.org/frr/keys.gpg | sudo tee /usr/share/keyrings/frrouting.gpg > /dev/null
FRRVER="frr-stable"
echo deb '[signed-by=/usr/share/keyrings/frrouting.gpg]' https://deb.frrouting.org/frr \
     $(lsb_release -s -c) $FRRVER | sudo tee -a /etc/apt/sources.list.d/frr.list
sudo apt update && sudo apt install frr mininet

# Archlinux
yay -S frr mininet
```

This project uses `uv` to manage python packages:
```bash
uv sync
```

Run an example:
```bash
# Use 001_two_switches as example
sudo uv run examples/001_two_switches/main.py
```

