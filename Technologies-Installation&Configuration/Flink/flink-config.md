# Flink Cluster Installation and Configuration

## Final Objective
Functional Flink cluster with 2 nodes (vm1, vm3) using Java 11 and Flink 1.20.3.

| VM  | Flink Role    | Services        |
|-----|---------------|-----------------|
| vm1 | JobManager    | Flink JM + REST |
| vm3 | TaskManager   | Flink TM        |

## 1. Prerequisites (ON BOTH VMs)

### 1.1 Java 11

### 1.2 Install Flink (ON BOTH VMs)
```bash
wget https://downloads.apache.org/flink/flink-1.20.3/flink-1.20.3-bin-scala_2.12.tgz
tar -xzvf flink-1.20.3-bin-scala_2.12.tgz
mv flink-1.20.3 flink
```

Add to `~/.bashrc`:
```bash
# Add java_home as well
## FLINK
export FLINK_HOME=/home/haithem/flink
export PATH=$PATH:$FLINK_HOME/bin
```
```bash
source ~/.bashrc
```

## 2. Flink Configuration

### 2.1 Edit `flink/conf/config.yaml` on vm1 and vm3
```yaml
env:
  java:
    home: /home/haithem/jdk-11.0.29/bin/java

jobmanager:
  bind-host: 0.0.0.0
  rpc:
    address: vm1
    port: 6123
  memory:
    process:
      size: 1536m

taskmanager:
  bind-host: 0.0.0.0
  numberOfTaskSlots: 2
  memory:
    process:
      size: 1024m

parallelism:
  default: 2

rest:
  address: vm1
  bind-address: 0.0.0.0
  port: 8081

state:
  backend:
    type: rocksdb
  checkpoints:
    dir: file:///home/haithem/flink-checkpoints
  savepoints:
    dir: file:///home/haithem/flink-savepoints

execution:
  checkpointing:
    interval: 60000
```

### 2.2 Create state directories on all VMs
```bash
mkdir -p ~/flink-checkpoints
mkdir -p ~/flink-savepoints
```

### 2.3 Define master/workers
**On vm1**: set the content of `flink/conf/masters`:
```
vm1
```

**On vm1 and vm3**: set the content of `flink/conf/workers`:
```
vm3
```

### 2.4 Configure passwordless SSH (MANDATORY)
On vm1:
```bash
ssh-keygen
ssh-copy-id haithem@vm3
```

Test:
```bash
ssh vm3
```

## 3. Launch the cluster (FROM vm1)
```bash
$FLINK_HOME/bin/start-cluster.sh
```

You should see:
- JobManager started on vm1
- TaskManager started on vm3

## 4. Verification

### 4.1 Flink Web UI
In your browser:
```
http://vm1:8081
```

You should see:
- 1 JobManager
- 1 TaskManager

### 4.2 Check processes
**On vm1:**
```bash
jps
```
=> `StandaloneSessionClusterEntrypoint`

**On vm3:**
```bash
jps
```
=> `TaskManagerRunner`

## 5. Quick test (optional but recommended)
```bash
flink run \
$FLINK_HOME/examples/streaming/TopSpeedWindowing.jar
```

=> You should see the job appear in the UI