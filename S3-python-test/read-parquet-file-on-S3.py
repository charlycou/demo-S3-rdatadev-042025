import pandas as pd
import matplotlib.pyplot as plt

# MinIO settings
minio_endpoint = "http://localhost:9000"
access_key = "test"
secret_key = "testtest"
bucket_name = "test"
object_name = "rain.gzip.parquet"

file_path = f"s3://{bucket_name}/{object_name}"

storage_options = {"s3":{
    "endpoint_url":minio_endpoint,
    "key": access_key,
    "secret": secret_key
}}

# Define your time range of interest
start_time = pd.Timestamp("2005-07-09 00:00:00").timestamp()*1000 #1120942500000
end_time = pd.Timestamp("2005-07-19 00:00:00").timestamp()*1000  #1121724000000

# Read only needed columns (optional: saves bandwidth if you specify)
columns = ["dateEnd", "value"]

# Read from Parquet over HTTP with lazy loading
df = pd.read_parquet(
    file_path,
    engine="pyarrow",
    columns=columns,  # Optional: load only these columns
    storage_options=storage_options,
    filters=[("dateEnd",">",start_time),(("dateEnd"),"<",end_time)]
)

# ✅ Output result
print(df.head())
print(df.tail())
df.plot(x='dateEnd')
plt.show()
