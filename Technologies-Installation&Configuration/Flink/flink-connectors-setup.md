# Flink Connectors Setup

## 1. Kafka Connector Installation

### 1.1 Download Kafka Connector
```bash
cd $FLINK_HOME/lib

# Download Flink Kafka Connector 3.3.0 (compatible with Kafka 3.9.1 and Flink 1.20.3)
wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-kafka/3.4.0-1.20/flink-connector-kafka-3.4.0-1.20.jar

# Download kafka-clients.jar
wget https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.4.0/kafka-clients-3.4.0.jar

```

### 1.2 Copy to TaskManager (vm2, vm3)
```bash
scp flink-connector-kafka-3.3.0-1.19.jar haithem@vm3:$FLINK_HOME/lib/
```

## 2. Doris JDBC Connector Installation

### 2.1 Download Required Connectors
```bash
cd $FLINK_HOME/lib

# Download Flink JDBC Connector
wget https://repo1.maven.org/maven2/org/apache/flink/flink-connector-jdbc/3.2.0-1.19/flink-connector-jdbc-3.2.0-1.19.jar

# Download MySQL Driver
wget wget https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar
```

### 2.2 Copy to TaskManager (vm2, vm3)
```bash
scp flink-connector-jdbc-3.2.0-1.19.jar haithem@vm3:$FLINK_HOME/lib/
scp mysql-connector-j-8.0.33.jar haithem@vm3:$FLINK_HOME/lib/
```

### 2.3 Restart Flink Cluster
```bash
$FLINK_HOME/bin/stop-cluster.sh
$FLINK_HOME/bin/start-cluster.sh
```