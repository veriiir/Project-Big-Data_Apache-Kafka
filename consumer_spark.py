from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window
from pyspark.sql.types import StructType, StringType, IntegerType

spark = SparkSession.builder \
    .appName("Gudang Monitoring") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Schema
suhu_schema = StructType() \
    .add("gudang_id", StringType()) \
    .add("suhu", IntegerType())

kelembaban_schema = StructType() \
    .add("gudang_id", StringType()) \
    .add("kelembaban", IntegerType())

# Stream suhu
suhu_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
    .option("subscribe", "sensor-suhu-gudang") \
    .load()

suhu_parsed = suhu_df.selectExpr("CAST(value AS STRING)", "timestamp") \
    .select(from_json(col("value"), suhu_schema).alias("data"), "timestamp") \
    .select("data.*", "timestamp") \
    .withWatermark("timestamp", "10 seconds")

# Stream kelembaban
kelembaban_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "127.0.0.1:9092") \
    .option("subscribe", "sensor-kelembaban-gudang") \
    .load()

kelembaban_parsed = kelembaban_df.selectExpr("CAST(value AS STRING)", "timestamp") \
    .select(from_json(col("value"), kelembaban_schema).alias("data"), "timestamp") \
    .select("data.*", "timestamp") \
    .withWatermark("timestamp", "10 seconds")

# Buat window 20 detik untuk join berdasarkan waktu dan gudang_id
suhu_windowed = suhu_parsed.withColumn("window", window("timestamp", "20 seconds"))
kelembaban_windowed = kelembaban_parsed.withColumn("window", window("timestamp", "20 seconds"))

# Join berdasarkan gudang_id dan window
join_df = suhu_windowed.join(
    kelembaban_windowed,
    on=["gudang_id", "window"]
).select(
    suhu_windowed.gudang_id,
    suhu_windowed.suhu,
    kelembaban_windowed.kelembaban,
    suhu_windowed.timestamp.alias("suhu_timestamp"),
    kelembaban_windowed.timestamp.alias("kelembaban_timestamp"),
    suhu_windowed.window
)

# Output fungsi
def handle_output(df, batch_id):
    data = df.collect()
    for row in data:
        suhu = row['suhu']
        kelembaban = row['kelembaban']
        gudang = row['gudang_id']

        if suhu > 80 and kelembaban > 70:
            print(f"[PERINGATAN KRITIS]\nGudang {gudang}:\n- Suhu: {suhu}°C\n- Kelembaban: {kelembaban}%\n- Status: Bahaya tinggi! Barang berisiko rusak\n")
        elif suhu > 80:
            print(f"[Peringatan Suhu Tinggi] Gudang {gudang}: Suhu {suhu}°C")
        elif kelembaban > 70:
            print(f"[Peringatan Kelembaban Tinggi] Gudang {gudang}: Kelembaban {kelembaban}%")

# Mulai stream dengan foreachBatch
query = join_df.writeStream \
    .outputMode("append") \
    .foreachBatch(handle_output) \
    .start()

query.awaitTermination()
