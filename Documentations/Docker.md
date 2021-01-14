# Docker

下载
https://download.docker.com/linux/ubuntu/dists/focal/pool/stable/amd64/

```bash
# Uninstall old versions
sudo apt-get remove docker docker-engine docker.io containerd runc

sudo dpkg -i docker-ce-cli_20.10.2_3-0_ubuntu-focal_amd64.deb
sudo dpkg -i containerd.io_1.4.3-1_amd64.deb
sudo dpkg -i docker-ce_20.10.2_3-0_ubuntu-focal_amd64.deb


# 卸载
sudo apt-get purge docker-ce docker-ce-cli containerd.io
```









