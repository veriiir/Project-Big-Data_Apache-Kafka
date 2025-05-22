from kafka import KafkaProducer
import json, time, random

producer = KafkaProducer(
    bootstrap_servers='127.0.0.1:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

gudang_ids = ['G1', 'G2', 'G3']

while True:
    data = {
        "gudang_id": random.choice(gudang_ids),
        "kelembaban": random.randint(60, 80)
    }
    producer.send('sensor-kelembaban-gudang', value=data)
    print("[Kelembaban Producer] Sent:", data)
    time.sleep(1)