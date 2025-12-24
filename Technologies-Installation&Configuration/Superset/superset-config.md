# Apache Superset Installation and Configuration

## Objective
Install and configure Apache Superset (vm5) and connect it to your cluster.

## 1. Install Superset

### 1.1 Install Python 3 and pip
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv build-essential libssl-dev libffi-dev libsasl2-dev
```

### 1.2 Create a virtual environment
```bash
python3 -m venv superset-env
source superset-env/bin/activate
```

### 1.3 Install Superset
```bash
pip install apache-superset
```

## 2. Superset Configuration

### 2.0 Secret Key Configuration

#### 2.0.1 Generate a strong key
```bash
openssl rand -base64 42
```

#### 2.0.2 Create superset_config.py
```bash
nano ~/superset_config.py
```
```python
SECRET_KEY = "put_the_generated_key_here"
```

### 2.1 Configure PostgreSQL as metadata DB

#### 2.1.1 Install PostgreSQL
```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

#### 2.1.2 Create database and Superset user
Connect to PostgreSQL as superuser:
```bash
sudo -u postgres psql
```

Create the database:
```sql
CREATE DATABASE superset;
```

Create the Superset user:
```sql
CREATE USER superset WITH PASSWORD 'superset';
```
**Note:** In production, use a strong password.

Recommended settings for Superset:
```sql
ALTER ROLE superset SET client_encoding TO 'utf8';
ALTER ROLE superset SET default_transaction_isolation TO 'read committed';
ALTER ROLE superset SET timezone TO 'UTC';
```

Grant privileges on the database:
```sql
GRANT ALL PRIVILEGES ON DATABASE superset TO superset;
```

Connect to the superset database:
```sql
\c superset
```

Grant privileges on the public schema:
```sql
GRANT ALL ON SCHEMA public TO superset;
ALTER SCHEMA public OWNER TO superset;
```

Allow creation of tables, sequences, functions:
```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO superset;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO superset;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO superset;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON TABLES TO superset;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON SEQUENCES TO superset;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT ALL ON FUNCTIONS TO superset;
```

Quick verification:
```bash
psql -h localhost -U superset -d superset
```

Then:
```sql
CREATE TABLE test_permission(id INT);
DROP TABLE test_permission;
```
→ If it works → PostgreSQL is correctly configured

#### 2.1.3 Install Python PostgreSQL driver
In your virtualenv (superset-env):
```bash
pip install psycopg2-binary
```

#### 2.1.4 Configure Superset (superset_config.py)
```bash
nano ~/superset_config.py
```

Add:
```python
SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://superset:superset@localhost:5432/superset"
)
```

#### 2.1.5 Tell Superset to use this file
```bash
echo 'export SUPERSET_CONFIG_PATH=~/superset_config.py' >> ~/.bashrc
source ~/.bashrc
```

#### 2.1.6 Initialize Superset's internal database
```bash
superset db upgrade
```

### 2.2 Create an admin user
```bash
superset fab create-admin \
  --username admin \
  --firstname Haithem \
  --lastname BenElbey \
  --email benelbey.haithem@gmail.com \
  --password Superset123
```

### 2.3 Initialize Superset
```bash
superset init
```

## 3. Launch Superset
```bash
# Launch Superset in server mode
superset run -h 10.0.10.8 -p 8088 --with-threads --reload --debugger
```

Superset will be accessible from the browser at:
```
http://vm5:8088
```