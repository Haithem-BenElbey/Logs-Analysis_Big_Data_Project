# Linking Backend with Frontend

This guide documents the steps to link Apache Doris Backend nodes with the Frontend.

## 1. Connect to Frontend (on VM4)

Connect to the Frontend using MySQL client:
```bash
mysql -h 10.0.10.7 -P 9030 -uroot
```

## 2. Add Backend Nodes

Add each Backend node to the cluster using their heartbeat service port (9050):
```sql
-- Add BE from VM4
ALTER SYSTEM ADD BACKEND "10.0.10.7:9050";

-- Add BE from VM5
ALTER SYSTEM ADD BACKEND "10.0.10.8:9050";
```

## 3. Verify Backend Registration

Check that the Backend nodes are properly registered and alive:
```sql
SHOW BACKENDS;
```

**Expected result:**

| Column | Expected Value |
|--------|---------------|
| **Alive** | `true` |
| **LastHeartbeat** | Recent timestamp |

### Sample Output
```
+-------+--------------+---------------+--------+----------+----------+---------------------+
| BackendId | Host      | HeartbeatPort | Alive  | ...      | ...      | LastHeartbeat       |
+-------+--------------+---------------+--------+----------+----------+---------------------+
| 10001 | 10.0.10.7    | 9050          | true   | ...      | ...      | 2024-01-15 10:30:45 |
| 10002 | 10.0.10.8    | 9050          | true   | ...      | ...      | 2024-01-15 10:30:46 |
+-------+--------------+---------------+--------+----------+----------+---------------------+
```

## Troubleshooting

### Backend shows as not Alive

If `Alive = false`:

1. **Check BE service status:**
```bash
   jps  # Should show DorisBE process
```

2. **Verify network connectivity:**
```bash
   # From VM3, test connection to BE
   telnet 10.0.10.7 9050
   telnet 10.0.10.8 9050
```

3. **Check BE logs:**
```bash
   tail -f ~/doris/be/log/be.INFO
```

4. **Verify BE configuration:**
   - Ensure `priority_networks = 10.0.10.0/24` is set correctly
   - Ensure `heartbeat_service_port = 9050` is configured

### Remove a Backend (if needed)
```sql
-- Remove a specific backend
ALTER SYSTEM DROP BACKEND "10.0.10.7:9050";
```

## Important Notes

- Use the **heartbeat port** (9050) when adding backends, not the service port (9060)
- All Backend nodes must be running before adding them to the cluster
- The `LastHeartbeat` should update every few seconds if the connection is healthy
- Backend IPs must match the subnet configured in `priority_networks`
