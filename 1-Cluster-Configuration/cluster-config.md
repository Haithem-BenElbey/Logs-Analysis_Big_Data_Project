# Cluster Configuration - Installation Guide

## Cluster Preparation

### 1. NAT Network Creation
Create a NAT network ( Exp: with the address range `10.0.10.0/24`)

### 2. Main VM Creation (vm1)
Specifications:
- RAM: 3 GB
- CPU: 3 cores
- OS: lubuntu-24.04.1-desktop-amd64

### 3. VM1 Preparation
```bash
sudo apt-get update
sudo apt upgrade -y 
sudo apt install openssh-server -y
```

### 4. Cloning and Creating Additional VMs
Create vm2, vm3, vm4, and vm5 by cloning vm1

> **⚠️ Important Note**: During cloning, keep the default configurations but **modify the MAC Address Policy parameter** to generate new MAC addresses.

### 5. Cloned VMs Modification

Change the hostname of each VM:
```bash
sudo nano /etc/hostname
sudo reboot
```

### 6. Configuring Connection Between VMs

#### Hosts File Configuration (on each VM)
```bash
sudo nano /etc/hosts
```

Add the following entries (adapt according to your IPs):
```
<ip_vm1> vm1
<ip_vm2> vm2
<ip_vm3> vm3
<ip_vm4> vm4
<ip_vm5> vm5
```
Exemple
```
10.0.10.4  vm1
10.0.10.5  vm2
10.0.10.6  vm3
10.0.10.7  vm4
10.0.10.8  vm5
```
#### SSH Service Activation
```bash
sudo systemctl enable ssh
sudo systemctl start ssh
sudo systemctl status ssh
```

---

## SSH Troubleshooting

### Encountered Issues

**Issue 1**: `sshd: no hostkeys available -- exiting`
- Host keys exist but have a size of 0 bytes

**Issue 2**: `Missing privilege separation directory: /run/sshd`
- The runtime directory `/run/sshd` does not exist

### Possible Causes

- Incomplete installation of the `openssh-server` package
- Cloning or restoring a virtual machine without regenerating keys
- Interruption during SSH key generation (reboot, etc.)

### Solutions

#### Solution for Issue 1
```bash
sudo rm -f /etc/ssh/ssh_host_*
sudo ssh-keygen -A
```

#### Solution for Issue 2
```bash
sudo mkdir -p /run/sshd
sudo chown root:root /run/sshd
sudo chmod 755 /run/sshd
```

After applying these fixes, restart the SSH service:
```bash
sudo systemctl restart ssh
sudo systemctl status ssh
```