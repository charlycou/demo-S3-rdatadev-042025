import fsspec
import pandas as pd
import logging
from fsspec.core import url_to_fs

# Enable debug-level logging for fsspec to monitor HTTP communication
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("fsspec")
logger.setLevel(logging.DEBUG)

# Define your storage options for MinIO/S3
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


# Wrap the S3-compatible filesystem with a data size tracker
class DataSizeTrackerFileSystem:
    def __init__(self, original_fs):
        self.fs = original_fs
        self.total_downloaded = 0

    def open(self, path, mode="rb", **kwargs):
        # Open the file as a wrapped file object
        file_obj = self.fs.open(path, mode, **kwargs)
        tracker = self
        return self._wrap_file(tracker, file_obj)

    def _wrap_file(self, tracker, file_obj):
        # Override the read method to track downloaded sizes
        class WrappedFile:
            def __init__(self, tracker, wrapped):
                self._wrapped = wrapped
                self._tracker = tracker

            def read(self, size=-1):
                data = self._wrapped.read(size)
                self._tracker.total_downloaded += len(data)
                return data

            def __enter__(self):
                # Handle the context management protocol
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                # Ensure file is closed when exiting the context
                self._wrapped.close()

            def __getattr__(self, attr):
                # Fallback for all other attributes/methods
                return getattr(self._wrapped, attr)

        return WrappedFile(tracker,file_obj)


fs = fsspec.filesystem('s3', key=access_key, secret=secret_key, endpoint_url=minio_endpoint)

# # Get the filesystem object for S3
# fs, path = url_to_fs(minio_endpoint)

# Wrap the filesystem to track downloaded data sizes
tracker_fs = DataSizeTrackerFileSystem(fs)

# Read the Parquet file from the wrapped filesystem
with tracker_fs.open(file_path) as f:
    # Define your time range of interest
    start_time = pd.Timestamp("2005-07-09 00:00:00").timestamp() * 1000  # 1120942500000
    end_time = pd.Timestamp("2005-07-19 00:00:00").timestamp() * 1000  # 1121724000000

    # Read only needed columns (optional: saves bandwidth if you specify)
    columns = ["dateEnd", "value"]
    df = pd.read_parquet(f, engine="pyarrow", columns=columns, filters=[("dateEnd",">",start_time),(("dateEnd"),"<",end_time)])



# Show the DataFrame
print(df)

# Print the total size of data downloaded
print(f"\nTotal data downloaded: {tracker_fs.total_downloaded / (1024 * 1024):.2f} MB")