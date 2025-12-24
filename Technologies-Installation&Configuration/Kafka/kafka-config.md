# Installation et Configuration d'un Cluster Kafka

## A/ Prérequis
- JDK 8 compatible avec version Kafka < 4.0
- Zookeeper

## B/ Installation et Configuration Kafka sur tous les brokers

### Téléchargement et Installation
```bash
wget https://downloads.apache.org/kafka/3.9.1/kafka_2.13-3.9.1.tgz
tar -xzvf kafka_2.13-3.9.1.tgz
mv kafka_2.13-3.9.1 Kafka
```

### Ajouter Kafka dans .bashrc
```bash
nano ~/.bashrc
```

Ajouter :
```bash
## KAFKA
export KAFKA_HOME=/home/haithem/kafka
export PATH=$PATH:$KAFKA_HOME/bin
```

Appliquer les modifications :
```bash
source ~/.bashrc
```

### Créer le répertoire des logs
```bash
mkdir -p /home/haithem/kafka/logs
```

### Configuration des Brokers
```bash
nano kafka/config/server.properties
```

#### Configuration Kafka Broker 1 (vm1:10.0.10.4)
```properties
broker.id=1
listeners=PLAINTEXT://vm1:9092
advertised.listeners=PLAINTEXT://vm1:9092
log.dirs=/home/haithem/kafka/logs
zookeeper.connect=vm1:2181,vm2:2181,vm3:2181
num.partitions=3
default.replication.factor=2
min.insync.replicas=2
```

#### Configuration Kafka Broker 2 (vm2)
```properties
broker.id=2
listeners=PLAINTEXT://vm2:9092
advertised.listeners=PLAINTEXT://vm2:9092
log.dirs=/home/haithem/kafka/logs
zookeeper.connect=vm1:2181,vm2:2181,vm3:2181
num.partitions=3
default.replication.factor=2
min.insync.replicas=2
```

#### Configuration Kafka Broker 3 (vm3)
```properties
broker.id=3
listeners=PLAINTEXT://vm3:9092
advertised.listeners=PLAINTEXT://vm3:9092
log.dirs=/home/haithem/kafka/logs
zookeeper.connect=vm1:2181,vm2:2181,vm3:2181
num.partitions=3
default.replication.factor=2
min.insync.replicas=2
```

## C/ Lancer Kafka sur tous les brokers en arrière plan
```bash
kafka-server-start.sh -daemon $KAFKA_HOME/config/server.properties
```

## Tests du Cluster Kafka

### Test 1 : Vérifier les Brokers
```bash
# Via ZooKeeper shell
zookeeper-shell.sh localhost:2181 <<< "ls /brokers/ids"
```

**Sortie attendue :**
```
[1, 2, 3]
```

### Test 2 : Créer un Topic
```bash
kafka-topics.sh --create \
  --bootstrap-server 10.0.10.4:9092 \
  --topic test-topic \
  --partitions 3 \
  --replication-factor 2
```

**Sortie attendue :**
```
Created topic test-topic.
```

### Test 3 : Lister les Topics
```bash
kafka-topics.sh --list \
  --bootstrap-server 10.0.10.4:9092
```

**Sortie attendue :**
```
test-topic
```

### Test 4 : Décrire le Topic
```bash
kafka-topics.sh --describe \
  --bootstrap-server 10.0.10.4:9092 \
  --topic test-topic
```

**Sortie attendue :**
```
Topic: test-topic	TopicId: xxx	PartitionCount: 3	ReplicationFactor: 2
	Topic: test-topic	Partition: 0	Leader: 1	Replicas: 1,2	Isr: 1,2
	Topic: test-topic	Partition: 1	Leader: 2	Replicas: 2,3	Isr: 2,3
	Topic: test-topic	Partition: 2	Leader: 3	Replicas: 3,1	Isr: 3,1
```

### Test 5 : Produire des Messages
Ouvrir un producteur :
```bash
kafka-console-producer.sh \
  --bootstrap-server 10.0.10.4:9092 \
  --topic test-topic
```

Taper des messages :
```
> Message 1
> Message 2
> Message 3
```

Appuyer sur Ctrl+C pour quitter.

### Test 6 : Consommer des Messages
Ouvrir un consommateur (dans un autre broker) :
```bash
kafka-console-consumer.sh \
  --bootstrap-server 10.0.10.5:9092 \
  --topic test-topic \
  --from-beginning
```

**Sortie attendue :**
```
Message 1
Message 2
Message 3
```