bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic sensor-suhu-gudang --partitions 1 --replication-factor 1
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic sensor-kelembaban-gudang --partitions 1 --replication-factor 1
