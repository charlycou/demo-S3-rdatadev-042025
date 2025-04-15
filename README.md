# demo-S3-rdatadev-042025
Demo repository for hands-on session to get into object sotrage and S3

# Learn S3 with MinIO 🪣

This project provides a hands-on environment to learn how S3 object storage works using [MinIO](https://min.io/) – a high-performance, self-hosted S3-compatible storage service.

---

## Getting Started

### 1. Run MinIO via Docker

```bash
bash scripts/run-minio.sh
```

### 2. Install and configure MinIO client (mc)

Intall `mc`

```bash
curl -O https://dl.min.io/client/mc/release/linux-amd64/mc
    chmod +x mc
    sudo mv mc /usr/local/bin/
```

Add a MinIO alias called `local` to interact with the server running in docker.

```bash
mc alias set local http://localhost:9000 minioadmin minioadmin
```

### 3. Interact with Minio

#### Create a bucket and store files with Minio UI
Loggin to MionIO UI : `http://localhost:9001` and create a bucket. Then upload a file in the bucket.


#### Create a Bucket and Store Files with the MinIO Client
- Use the mc ls command to list the created bucket.
- Then, use the mc mb command to create a new bucket.
- Add a new file with the mc put command.
- Play around with the mc cp command to copy a file:
    - from a bucket to your local system,
    - from your local system to a bucket,
    - or between two buckets.
- Delete a file with the mc rm command.
- Delete a bucket with the mc rb command.

Check out the full capabilities of the mc client commands here: https://min.io/docs/minio/linux/reference/minio-mc/mc-rm.html

### 4. S3 (Simple Storage Service) API

The S3 API is an HTTP-based API for interacting with storage, and follows REST (Representational State Transfer) principles. The API uses standard HTTP methods such as GET, PUT, POST and DELETE.
The authorization mechanism supported is AWS4-HMAC-SHA256.

![AWS_SIG_V4](https://docs.aws.amazon.com/images/AmazonS3/latest/API/images/sigV4-using-query-params.png)

BUGGED AWS-SIG-V4 PutObject request in `./S3-API-curl-test`! 
Reférences: https://docs.aws.amazon.com/AmazonS3/latest/API/sig-v4-header-based-auth.html

### 5. Interact with S3 API using Python client

Install dependencies in a virtual environement of your choice and run `put-to-s3.py` script.

```bash
cd S3-python-test
pip install boto3`
python put-to-s3.py
```

### 6. User and file management

#### User identity and access management

https://min.io/docs/minio/linux/administration/identity-access-management/minio-user-management.html

A MinIO user consists of a unique access key (username) and corresponding secret key (password). Clients must authenticate their identity by specifying both a valid access key (username) and the corresponding secret key (password) of an existing MinIO user.

Each user can have one or more assigned policies that explicitly list the actions and resources to which that user has access. Users can also inherit policies from the groups in which they have membership. MinIO by default denies access to all actions or resources not explicitly allowed by a user’s assigned or inherited policies. 

- Create a new user:

```bash
mc admin user add local newuser newpassword
```

- List existing users:

```bash
mc admin user list local
```

- Enable, disable, remove user

```bash
mc admin user enable local newuser
mc admin user disable local newuser
mc admin user remove local newuser
```

- view built-in policies

```bash
mc admin policy list local
```

- assign policy to a user
```bash
mc admin policy set local readwrite user=newuser
```

- Create a custom policy
This policy allow "GetObject" S3 request only on "test" bucket

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["s3:GetObject"],
      "Effect": "Allow",
      "Resource": ["arn:aws:s3:::mybucket/*"]
    }
  ]
}
```

Save this policy in a file `custom-policy.json` and apply it:

```bash
mc admin policy add local custom-policy custom-policy.json
mc admin policy set local custom-policy user=newuser
```

A User can create "Access Key" to enable access to a subset of the actions and resources explicitly allowed for him. Access Keys automatically inherit permissions from the parent user by default. If the parent user belongs to any groups, and those groups have policies (like read-only, read-write), the Access Key will get those too. However, you can add an inline policy (a policy directly on the Access Key) that says. To get available policy conditions: https://min.io/docs/minio/linux/administration/identity-access-management/policy-based-access-control.html.

The `mc admin accesskey` command and its subcommands create and manage Access Keys for internally managed users on a MinIO deployment. You can also create new access key through UI : http://localhost:9001/access-keys.

#### File management

MinIO supports S3-compatible lifecycle policies, which allow you to automatically manage the expiration of objects (files) based on age, prefix, or tags. This is useful for cleaning up old backups, temporary files, or logs without manual intervention.


- Create a Lifecycle policy json file `lifecycle.json`

``` json
{
  "Rules": [
    {
      "ID": "expire-temp-files",
      "Status": "Enabled",
      "Prefix": "",
      "Expiration": {
        "Days": 1
      }
    }
  ]
}
```

- Apply the lifecycle policy to a bucket and check that the rule has been applied

```bash
mc ilm import local/test < lifecycle.json
mc ilm export local/test
```

Another lifecycle policy using tag-based rule
```bash
mc ilm rule add local/test --expire-days 30 --tags "temporary30d=true"
```

#### Bucket versionning

https://min.io/docs/minio/linux/administration/object-management/object-versioning.html

### 7. Benefits of using "analysis-ready" file formats with S3

**What are analysis-ready file formats?** These are formats optimized for querying, reading, and analysis, not just storage. (Parquet, ROC, Arrow, Zarr, COG...). Dessimate one of the major drawback of S3 storage which is the need of downloading the file locally to process it!

Modern data tools (like DuckDB, Spark, Pandas, etc.) can query files directly on S3, without downloading the entire file first. These tools use HTTP Range Requests to fetch only the needed parts of a file stored remotely.

> An HTTP Range request asks the server to send parts of a resource back to a client. Range requests are useful for various clients, including media players that support random access, data tools that require only part of a large file, and download managers that let users pause and resume a download.

It is a way for client to is a way for clients to ask the server: "Please send me only the bytes from position 10,000 to 12,000 of this file."

Benefits:
- Save bandwidth (only transfer needed data).
- Speed up analysis (skip irrelevant data).
- Work efficiently over remote S3 URLs — no temp files needed.


### Read only a part of a parquet file (Column oriented format)

Put `rain.gzip.parquet` file in a bucket and query only a subset of the file using python script `read-parquet-file-on-S3.py`.

What is happening? 
- PyArrow loads parquet file metadata via an HTTP Range Request (Parquet metadata are stored on a footer).
- Then it fetches only the required row groups/columns.
- You still need to filter timestamps in memory, but only the minimal subset is read.

More info on Parquet (in French) : https://www.casd.eu/wp/wp-content/uploads/WebinaireParquet-DuckDB-CASD_20250204d.mp4

### Read only a part of a Cloud-Optimized GeoTiff (COG)

Query only a subset of a cloud-optimized geotiff using python script `read-cog-file-on-S3.py`.

What is happening? 
- rioxarray lazy load the raster file
- Then it fetches only the required tiles according to the slice selected (Using HTTP Range Request again)





