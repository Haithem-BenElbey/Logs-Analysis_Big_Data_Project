# Data Pipeline Setup - Kafka Producers

## Overview
Configure Kafka topics and create Python-based data generators for streaming logs and metrics.

---

## PHASE 1 - Prepare Kafka (from vm1)

### 1. Verify Kafka
On vm1:
```bash
jps
```

**Expected output:**
```
Kafka
QuorumPeerMain (Zookeeper)
```

If Kafka is not running:
```bash
kafka/bin/kafka-server-start.sh -daemon /kafka/config/server.properties
```

### 2. Create Kafka Topics
On vm1:

#### 🔹 Application logs
```bash
kafka/bin/kafka-topics.sh --create \
  --topic app-logs \
  --bootstrap-server vm1:9092 \
  --partitions 3 \
  --replication-factor 2
```

#### 🔹 System metrics
```bash
kafka/bin/kafka-topics.sh --create \
  --topic system-metrics \
  --bootstrap-server vm1:9092 \
  --partitions 3 \
  --replication-factor 2
```

#### 🔹 Anomaly alerts (Flink output)
```bash
kafka/bin/kafka-topics.sh --create \
  --topic anomaly-alerts \
  --bootstrap-server vm1:9092 \
  --partitions 3 \
  --replication-factor 2
```

### Verification
```bash
kafka/bin/kafka-topics.sh --list --bootstrap-server vm1:9092
```

**Expected output:**
```
app-logs
system-metrics
anomaly-alerts
```

---

## PHASE 2 - Prepare vm2 for Python Execution

### 1. Install Python & Dependencies (vm2)
On vm2:
```bash
sudo apt update
sudo apt install -y python3-pip python3-full python3-venv
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv kafka-env
source kafka-env/bin/activate
```

### 3. Install Required Libraries
```bash
pip3 install kafka-python faker
```

### Verification
```bash
python3 -c "import kafka, faker; print('OK')"
```

**Expected output:**
```
OK
```

---

## PHASE 3 - Create Python Log Generator (vm2)

### 1. Create Python File
On vm2:
```bash
mkdir -p ~/log-generator
cd ~/log-generator
nano log_generator.py
```

### 2. Make Script Executable
```bash
chmod +x log_generator.py
```

---

## PHASE 4 - Test Python → Kafka Pipeline

### 1. Start Kafka Consumer (vm1)
In a terminal on vm1:
```bash
kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server vm1:9092 \
  --topic app-logs \
  --from-beginning
```

### 2. Start Python Generator (vm2)
On vm2:
```bash
python3 log_generator.py
```

**Expected behavior:**
- ✅ Logs appear in Python output
- ✅ Messages arrive in Kafka consumer 

### Test Other Topics
```bash
# On vm1 - test system-metrics topic
kafka/bin/kafka-console-consumer.sh \
  --bootstrap-server vm1:9092 \
  --topic system-metrics \
  --from-beginning
```