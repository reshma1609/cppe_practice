import pandas as pd
import boto3
import psycopg2
from io import StringIO

# ---------- 1. EXTRACT: Load data from S3 ----------
s3 = boto3.client(
    's3',
    aws_access_key_id='YOUR_ACCESS_KEY',
    aws_secret_access_key='YOUR_SECRET_KEY',
    region_name='ap-south-1'
)

bucket_name = "etl-data-bucket-samiksha"
file_key = "data.csv"

print("📥 Extracting data from S3...")
obj = s3.get_object(Bucket=bucket_name, Key=file_key)
df = pd.read_csv(obj['Body'])
print("✅ Data extracted successfully!")

# ---------- 2. TRANSFORM ----------
print("🔧 Transforming data...")
if 'height_in' in df.columns:
    df['height_cm'] = df['height_in'] * 2.54
print("✅ Data transformed successfully!")

# ---------- 3. LOAD INTO POSTGRES ----------
print("📤 Loading data into PostgreSQL...")

try:
    conn = psycopg2.connect(
        host="etl-postgres-db.cja0ku64kco3.ap-south-1.rds.amazonaws.com",
        database="ClusterKL1",
        user="postgres",
        password="Praveen2kiran.",
        port="5432"
    )
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS people (
            name VARCHAR(50),
            height_in FLOAT,
            height_cm FLOAT
        );
    """)

    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False, header=False)
    csv_buffer.seek(0)

    cur.copy_from(csv_buffer, 'people', sep=',')
    conn.commit()

    print("✅ Data loaded successfully!")

except Exception as e:
    print("❌ Error loading data:", e)

finally:
    if conn:
        cur.close()
        conn.close()
