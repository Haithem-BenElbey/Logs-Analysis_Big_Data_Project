# Installation et Configuration de Cluster ZooKeeper

## Prérequis
- 3 machines virtuelles : vm1, vm2, vm3
- Fichiers d'installation : `jdk-11.0.29_linux-x64_bin.tar.gz` et `apache-zookeeper-3.8.5-bin.tar.gz`

---

## 1. Installation de Java et ZooKeeper

Sur **chaque VM (vm1, vm2, vm3)** :
```bash
cd ~
tar -xzvf jdk-11.0.29_linux-x64_bin.tar.gz
tar -xzvf apache-zookeeper-3.8.5-bin.tar.gz
mv apache-zookeeper-3.8.5-bin zookeeper
```

---

## 2. Configuration des Variables d'Environnement

Éditer le fichier `.bashrc` :
```bash
nano .bashrc
```

Ajouter les lignes suivantes :
```bash
## JAVA
export JAVA_HOME=/home/haithem/jdk1.8.0_92 
export PATH=$JAVA_HOME/bin:$PATH

## ZOOKEEPER
export ZOOKEEPER_HOME=/home/haithem/zookeeper
export PATH=$PATH:$ZOOKEEPER_HOME/bin
```

Appliquer les modifications :
```bash
source .bashrc
```

Vérifier l'installation de Java :
```bash
java -version
```

---

## 3. Création des Dossiers de Données et Logs

Sur **chaque VM** :
```bash
mkdir -p ~/zookeeper/data
mkdir -p ~/zookeeper/log
```

---

## 4. Configuration du Fichier zoo.cfg

Créer/éditer le fichier de configuration :
```bash
nano ~/zookeeper/conf/zoo.cfg
```

Ajouter la configuration suivante (**identique sur les 3 VMs**) :
```properties
tickTime=2000
initLimit=5
syncLimit=2

# Chemins des données et logs
dataDir=/home/haithem/zookeeper/data
dataLogDir=/home/haithem/zookeeper/log

# Port client
clientPort=2181

# Configuration du cluster
server.1=vm1:2888:3888
server.2=vm2:2888:3888
server.3=vm3:2888:3888
```

---

## 5. Définir l'ID Unique (myid) pour Chaque Nœud

### Sur vm1 :
```bash
echo 1 > ~/zookeeper/data/myid
```

### Sur vm2 :
```bash
echo 2 > ~/zookeeper/data/myid
```

### Sur vm3 :
```bash
echo 3 > ~/zookeeper/data/myid
```

---

## 6. Démarrage du Cluster ZooKeeper

Sur **chaque VM**, démarrer ZooKeeper :
```bash
~/zookeeper/bin/zkServer.sh start
```

---

## 7. Vérification de l'État du Cluster

Vérifier l'état sur chaque VM :
```bash
~/zookeeper/bin/zkServer.sh status
```

**Résultat attendu :**
- Un nœud affichera : `Mode: leader`
- Les deux autres nœuds afficheront : `Mode: follower`

---

## 8. Test de Haute Disponibilité (Failover)

### Arrêter le leader

Sur le nœud leader identifié :
```bash
~/zookeeper/bin/zkServer.sh stop
```

### Vérifier l'élection d'un nouveau leader

Sur les nœuds restants :
```bash
~/zookeeper/bin/zkServer.sh status
```

**Résultat attendu :** Un des followers sera automatiquement élu comme nouveau leader.

---

## Commandes Utiles

| Commande | Description |
|----------|-------------|
| `zkServer.sh start` | Démarrer ZooKeeper |
| `zkServer.sh stop` | Arrêter ZooKeeper |
| `zkServer.sh status` | Vérifier l'état du nœud |
| `zkServer.sh restart` | Redémarrer ZooKeeper |

---

**Ports utilisés :**
- **2181** : Port client
- **2888** : Communication entre peers
- **3888** : Élection du leader