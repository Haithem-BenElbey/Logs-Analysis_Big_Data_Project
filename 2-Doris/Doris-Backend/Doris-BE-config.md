# Apache Doris Backend Installation and Configuration

This guide documents the installation and configuration of Apache Doris 3.0.1 Backend on virtual machines (VM4 and VM5).

## 1. Prerequisites on VM4 and VM5

### 1.1 Java Installation
```bash
sudo apt update
sudo apt install -y openjdk-17-jdk
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### 1.2 System Dependencies (REQUIRED)
```bash
sudo apt install -y \
  curl wget unzip \
  libsnappy1v5 \
  libatomic1 \
  libaio-dev \
  libc6 \
  libgcc-s1 \
  libstdc++6
```

These dependencies ensure that Doris Backend can start, store, process, and serve analytical data efficiently without crashes.

| Package | Why? (Summary) |
|---------|----------------|
| **libsnappy1v5** | Fast compression for columnar data and network exchanges |
| **libatomic1** | Support for atomic operations (thread safety, parallelism) |
| **libaio1** | Asynchronous I/O for high-performance disk reads/writes |
| **libc6** | Standard C library required for any Linux binary |
| **libgcc-s1** | Exception handling and GCC runtime for C++ |
| **libstdc++6** | C++ standard library (Doris BE is written in C++) |
| **curl / wget / unzip** | Data download, ingestion, and administration |

### 1.3 Kernel Parameters (CRITICAL)
```bash
sudo sh -c "echo 'vm.max_map_count=2000000' >> /etc/sysctl.conf"
sudo sysctl -p
```

> Doris BE uses mmap intensively (columnar storage).

### 1.4 Open File Limits
```bash
sudo sh -c "echo '* soft nofile 1000000' >> /etc/security/limits.conf"
sudo sh -c "echo '* hard nofile 1000000' >> /etc/security/limits.conf"
```

## 2. Doris BE Installation

**Note:** Use the same version as FE
```bash
cd ~
wget https://apache-doris-releases.oss-accelerate.aliyuncs.com/apache-doris-3.0.1-bin-x64.tar.gz
tar -xvf apache-doris-3.0.1-bin-x64.tar.gz
mv apache-doris-3.0.1-bin-x64 doris
```

## 3. BE Configuration
```bash
nano ~/doris/be/conf/be.conf
```

**Recommended configuration:**
```bash
# Set your own JAVA_HOME
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# BE IP (vm4 or vm5)
priority_networks = 10.0.10.0/24

# Ports
be_port = 9060
webserver_port = 8040
heartbeat_service_port = 9050
brpc_port = 8060

# Storage 
storage_root_path = /home/haithem/doris/storage

# Memory
mem_limit = 1800000000
```

### 3.1 Create Storage Directory
```bash
mkdir -p ~/doris/storage
```

## 4. Start BE (FE must already be running)
```bash
~/doris/be/bin/start_be.sh --daemon
```

**Verify:**
```bash
jps
```

You should see:
```
DorisBE
```

## 5. Issues Encountered and Solutions

### 5.1 Problem

**Error message:** `Disable swap memory before starting be`

Doris BE intentionally refuses to start if swap is enabled.

**Why does Doris BE prohibit swap?**

Apache Doris BE is:
- Memory-intensive
- Latency-sensitive

If swap is enabled:
- Linux can move memory pages to disk
- ➜ Huge latency
- ➜ Timeouts
- ➜ BE crashes under load
- ➜ Slow analytical results

=> Doris therefore applies strict safety measures.

### 5.2 Solution

#### 5.2.1 Edit /etc/fstab
```bash
sudo nano /etc/fstab
```

#### 5.2.2 Comment out any line containing swap

Example:
```bash
# /swapfile none swap sw 0 0
```

#### 5.2.3 Reboot the VM
```bash
sudo reboot
```

## Important Notes

- Ensure the same Doris version is used across all nodes (FE and BE)
- Memory limit is set to ~1.8GB (`mem_limit = 1800000000`)
- All BEs must be on the same network subnet configured in `priority_networks`
- Swap must be completely disabled before starting BE
- Storage path must exist and have proper permissions
