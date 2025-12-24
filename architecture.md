# Final Architecture

## Cluster Overview

This document describes the final distributed architecture for the data processing pipeline.

## Architecture Diagram
```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Data Processing Cluster                          │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│     VM1      │  │     VM2      │  │     VM3      │
│  10.0.10.4   │  │  10.0.10.5   │  │  10.0.10.6   │
├──────────────┤  ├──────────────┤  ├──────────────┤
│ ZooKeeper    │  │ ZooKeeper    │  │ ZooKeeper    │
│ Kafka Broker │  │ Kafka Broker │  │ Kafka Broker │
│ Flink JM     │  │              │  │ Flink TM     │
└──────────────┘  └──────────────┘  └──────────────┘
       │                 │                 │
       └─────────────────┴─────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Kafka Cluster       │
              │  (3 Brokers)         │
              └──────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Flink Processing    │
              │  (1 JM + 1 TM)       │
              └──────────────────────┘
                         │
                         ▼
       ┌─────────────────┴─────────────────┐
       │                                   │
┌──────────────┐                    ┌──────────────┐
│     VM4      │                    │     VM5      │
│  10.0.10.7   │                    │  10.0.10.8   │
├──────────────┤                    ├──────────────┤
│ Doris FE     │◄───────────────────┤ Doris BE     │
│ Doris BE     │                    │ Superset     │
└──────────────┘                    └──────────────┘
       │
       └─────────────────┐
                         │
                         ▼
              ┌──────────────────────┐
              │  Doris Cluster       │
              │  (1 FE + 2 BE)       │
              └──────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  Superset            │
              │  (Visualization)     │
              └──────────────────────┘
```

## Node Details

### VM1 (10.0.10.4)
**Role:** Coordination & Stream Processing Manager

| Component | Version | Role | Ports |
|-----------|---------|------|-------|
| ZooKeeper | 3.8.5 | Coordination Service | 2181, 2888, 3888 |
| Kafka Broker | 3.9.1 | Message Broker (ID: 1) | 9092 |
| Flink JobManager | 1.20.3 | Stream Processing Manager | 6123, 8081 |

**Services:**
- ZooKeeper ensemble member
- Kafka broker with 3 partitions per topic
- Flink job coordination and REST API

---

### VM2 (10.0.10.5)
**Role:** Message Broker Node

| Component | Version | Role | Ports |
|-----------|---------|------|-------|
| ZooKeeper | 3.8.5 | Coordination Service | 2181, 2888, 3888 |
| Kafka Broker | 3.9.1 | Message Broker (ID: 2) | 9092 |

**Services:**
- ZooKeeper ensemble member
- Kafka broker for high availability

---

### VM3 (10.0.10.6)
**Role:** Stream Processing Worker

| Component | Version | Role | Ports |
|-----------|---------|------|-------|
| ZooKeeper | 3.8.5 | Coordination Service | 2181, 2888, 3888 |
| Kafka Broker | 3.9.1 | Message Broker (ID: 3) | 9092 |
| Flink TaskManager | 1.20.3 | Stream Processing Worker | - |

**Services:**
- ZooKeeper ensemble member
- Kafka broker for high availability
- Flink task execution with 2 task slots

---

### VM4 (10.0.10.7)
**Role:** Analytical Database - Master

| Component | Version | Role | Ports |
|-----------|---------|------|-------|
| Doris Frontend (FE) | 3.0.1 | Query Coordinator | 8030 (HTTP), 9030 (MySQL) |
| Doris Backend (BE) | 3.0.1 | Storage & Compute | 9050 (Heartbeat), 8040 (HTTP) |

**Services:**
- Doris metadata management
- SQL query planning and coordination
- Data storage and processing

---

### VM5 (10.0.10.8)
**Role:** Analytics & Visualization

| Component | Version | Role | Ports |
|-----------|---------|------|-------|
| Doris Backend (BE) | 3.0.1 | Storage & Compute | 9050 (Heartbeat), 8040 (HTTP) |
| Superset | Latest | Data Visualization | 8088 |
| PostgreSQL | Latest | Superset Metadata DB | 5432 |

**Services:**
- Doris data storage and processing
- Interactive dashboards and reports
- Superset metadata storage

---

## Data Flow
```
┌─────────────┐
│  Data       │
│  Sources    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│     Kafka Cluster (VM1-3)       │
│  • 3 Brokers                    │
│  • Replication Factor: 2        │
│  • Min In-Sync Replicas: 2     │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   Flink Processing (VM1, VM3)   │
│  • JobManager: VM1              │
│  • TaskManager: VM3             │
│  • Checkpointing enabled        │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│     Doris Cluster (VM4-5)       │
│  • Frontend: VM4                │
│  • Backends: VM4, VM5           │
│  • Replication: 2               │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│      Superset (VM5)             │
│  • Real-time dashboards         │
│  • SQL analytics                │
└─────────────────────────────────┘
```

## Component Summary

### Distributed Systems

| System | Nodes | Purpose |
|--------|-------|---------|
| **ZooKeeper Ensemble** | 3 (VM1, VM2, VM3) | Distributed coordination |
| **Kafka Cluster** | 3 (VM1, VM2, VM3) | Message streaming platform |
| **Flink Cluster** | 2 (VM1, VM3) | Stream processing engine |
| **Doris Cluster** | 3 (1 FE + 2 BE) | Analytical database |

### Software Versions

| Software | Version | Java Version |
|----------|---------|--------------|
| ZooKeeper | 3.8.5 | Java 11 |
| Kafka | 3.9.1 (Scala 2.13) | Java 11 |
| Flink | 1.20.3 (Scala 2.12) | Java 11 (JDK 11.0.29) |
| Doris | 3.0.1 | Java 11 |
| Superset | Latest | Python 3 |

### Network Configuration

| Service | Protocol | Port | Access |
|---------|----------|------|--------|
| ZooKeeper Client | TCP | 2181 | Internal |
| ZooKeeper Peer | TCP | 2888 | Internal |
| ZooKeeper Leader Election | TCP | 3888 | Internal |
| Kafka Broker | TCP | 9092 | Internal |
| Flink JobManager RPC | TCP | 6123 | Internal |
| Flink JobManager REST | HTTP | 8081 | External |
| Doris FE HTTP | HTTP | 8030 | Internal |
| Doris FE MySQL | TCP | 9030 | Internal/External |
| Doris BE Heartbeat | TCP | 9050 | Internal |
| Doris BE HTTP | HTTP | 8040 | Internal |
| Superset Web UI | HTTP | 8088 | External |
| PostgreSQL | TCP | 5432 | Local (VM5) |

## High Availability Features

### ZooKeeper
- ✅ 3-node ensemble (quorum: 2)
- ✅ Leader election support
- ✅ Automatic failover

### Kafka
- ✅ 3 brokers for redundancy
- ✅ Replication factor: 2
- ✅ Min in-sync replicas: 2
- ✅ Automatic leader election

### Flink
- ✅ Checkpointing enabled (60s interval)
- ✅ State backend: RocksDB
- ✅ Savepoints support
- ✅ Job recovery on failure

### Doris
- ✅ 1 Frontend (metadata master)
- ✅ 2 Backends (data replication)
- ✅ Automatic replica management
- ✅ Query load balancing

## Storage Configuration

### Kafka
- **Log Directory:** `/home/haithem/kafka/logs`
- **Partitions per Topic:** 3 (default)
- **Replication:** 2 replicas per partition

### Flink
- **Checkpoints:** `/home/haithem/flink-checkpoints`
- **Savepoints:** `/home/haithem/flink-savepoints`
- **State Backend:** RocksDB

### Doris
- **Storage Path:** `/home/haithem/doris/be/storage`
- **Replication:** 2 replicas per tablet

## Access Points

### Web UIs

| Service | URL | Credentials |
|---------|-----|-------------|
| Flink Dashboard | http://vm1:8081 | None |
| Superset | http://vm5:8088 | admin / Superset123 |

### Command Line Access
```bash
# Kafka
kafka-topics.sh --bootstrap-server vm1:9092 --list

# Flink
flink list -m vm1:8081

# Doris
mysql -h vm4 -P 9030 -u root

# Superset
# Access via web browser
```

## Resource Allocation

### Memory Configuration

| VM | Component | Memory Allocation |
|----|-----------|-------------------|
| VM1 | Flink JobManager | 1536 MB |
| VM3 | Flink TaskManager | 1024 MB |
| VM3 | Task Slots | 2 slots |

### Parallelism

- **Flink Default Parallelism:** 2
- **Kafka Partitions:** 3 per topic
- **Doris Buckets:** 3 per table (default)

## Integration Points

### Flink → Kafka
- **Connector:** flink-connector-kafka-3.3.0
- **Bootstrap Servers:** vm1:9092,vm2:9092,vm3:9092
- **Format:** JSON

### Flink → Doris
- **Connector:** flink-connector-jdbc-3.2.0
- **Driver:** mysql-connector-j-8.0.33
- **URL:** jdbc:mysql://vm4:9030/test

### Superset → Doris
- **Connection:** MySQL Protocol
- **Driver:** PyMySQL
- **URL:** mysql+pymysql://root:@vm4:9030/test

## Deployment Summary

| VM | Role | Components | Resource Impact |
|----|------|------------|-----------------|
| VM1 | Master | ZK + Kafka + Flink JM | High (coordination) |
| VM2 | Worker | ZK + Kafka | Medium (streaming) |
| VM3 | Worker | ZK + Kafka + Flink TM | High (processing) |
| VM4 | Database Master | Doris FE + BE | High (storage/query) |
| VM5 | Database Worker + Viz | Doris BE + Superset | Medium (storage/viz) |

## Notes

- All VMs are running **Java 11 (JDK 11.0.29)**
- ZooKeeper ensemble provides coordination for Kafka
- Kafka cluster handles message streaming with fault tolerance
- Flink processes streams from Kafka and writes to Doris
- Doris stores analytical data with replication
- Superset provides visualization layer on top of Doris
- All components are configured for high availability
```
