# Connecting Superset to Doris

Superset uses SQLAlchemy to connect to SQL databases.

## 1. Install MySQL driver (on vm5 where Superset is located)

In the Superset virtual environment (superset-env):
```bash
pip install pymysql
```

## 2. Configure the connection in Superset

### Doris ↔ Superset Connection (Superset UI)

**In Superset UI:**
1. Go to: **Settings → Database Connections → + Database**

2. Choose:
```
   MySQL
```

3. Choose to connect with **SQLAlchemy URI** (or you can fill in the fields manually):
```
   mysql+pymysql://<user>:<password>@<Doris_FE_IP>:9030/<database_name>
```

   Where:
   - `<user>` → Doris user (e.g., root or the one you created)
   - `<password>` → corresponding password
   - `<Doris_FE_IP>` → FE VM IP (10.0.10.7)
   - `<database_name>` → Doris database you want to use

**Example:**
```
mysql+pymysql://root:@10.0.10.7:9030/test
```

**Notes:**
- 10.0.10.7 = IP of your Doris FE (it's always the FE that handles SQL queries)
- Default port for Doris FE = 9030
- Database `test` must exist in Doris

## 3. Test the connection

→ Superset should display **"Test succeeded"** if everything is correct.