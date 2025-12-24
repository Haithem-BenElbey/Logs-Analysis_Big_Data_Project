log_generator.py
#!/usr/bin/env python3
"""
Multi-Source Log Generator for Kafka
Simulates application logs and system metrics with anomalies
"""

import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer
from faker import Faker

fake = Faker()

# Kafka Producer Configuration
producer = KafkaProducer(
    bootstrap_servers=['vm1:9092', 'vm2:9092', 'vm3:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3
)

# Log levels and types
LOG_LEVELS = ['INFO', 'WARNING', 'ERROR', 'CRITICAL']
APP_COMPONENTS = ['AuthService', 'PaymentAPI', 'DatabasePool', 'CacheLayer', 'LoadBalancer']
ERROR_MESSAGES = [
    'Connection timeout',
    'Null pointer exception',
    'Out of memory',
    'Database deadlock',
    'Rate limit exceeded',
    'Invalid authentication token',
    'Service unavailable'
]

def generate_app_log():
    """Generate application log entry"""
    is_anomaly = random.random() < 0.15  # 15% anomaly rate
    
    if is_anomaly:
        level = random.choice(['ERROR', 'CRITICAL'])
        response_time = random.uniform(3000, 8000)  # Slow response
    else:
        level = random.choices(LOG_LEVELS, weights=[70, 20, 8, 2])[0]
        response_time = random.uniform(50, 500)
    
    log = {
        'timestamp': datetime.now().isoformat(),
        'log_type': 'application',
        'level': level,
        'component': random.choice(APP_COMPONENTS),
        'message': random.choice(ERROR_MESSAGES) if level in ['ERROR', 'CRITICAL'] else 'Request processed',
        'response_time_ms': round(response_time, 2),
        'user_id': fake.uuid4(),
        'ip_address': fake.ipv4(),
        'is_anomaly': is_anomaly
    }
    return log

def generate_system_metrics():
    """Generate system metrics"""
    is_anomaly = random.random() < 0.12  # 12% anomaly rate
    
    if is_anomaly:
        cpu_usage = random.uniform(85, 99)
        memory_usage = random.uniform(90, 98)
        disk_io = random.uniform(800, 1000)
    else:
        cpu_usage = random.uniform(20, 70)
        memory_usage = random.uniform(40, 75)
        disk_io = random.uniform(100, 400)
    
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'log_type': 'system_metrics',
        'server_id': f'server-{random.randint(1, 5)}',
        'cpu_usage_percent': round(cpu_usage, 2),
        'memory_usage_percent': round(memory_usage, 2),
        'disk_io_mbps': round(disk_io, 2),
        'network_in_mbps': round(random.uniform(10, 200), 2),
        'network_out_mbps': round(random.uniform(10, 150), 2),
        'active_connections': random.randint(50, 500),
        'is_anomaly': is_anomaly
    }
    return metrics

def main():
    print(" Starting Multi-Source Log Generator...")
    print(" Sending to Kafka topics: app-logs, system-metrics")
    print(" Anomaly injection rate: ~15% for apps, ~12% for metrics\n")
    
    msg_count = 0
    
    try:
        while True:
            # Generate and send application log
            app_log = generate_app_log()
            producer.send('app-logs', value=app_log)
            
            # Generate and send system metrics (every 2 seconds)
            if msg_count % 2 == 0:
                sys_metrics = generate_system_metrics()
                producer.send('system-metrics', value=sys_metrics)
                
                print(f" [{msg_count}] APP: {app_log['level']:8} | {app_log['component']:15} | "
                      f"{' ANOMALY' if app_log['is_anomaly'] else ' Normal'}")
                print(f" [{msg_count}] SYS: CPU={sys_metrics['cpu_usage_percent']:5.1f}% | "
                      f"MEM={sys_metrics['memory_usage_percent']:5.1f}% | "
                      f"{' ANOMALY' if sys_metrics['is_anomaly'] else ' Normal'}\n")
            
            msg_count += 1
            time.sleep(1)  # 1 message per second
            
    except KeyboardInterrupt:
        print(f"\n Stopped. Total messages sent: {msg_count}")
    finally:
        producer.close()

if __name__ == '__main__':
    main()