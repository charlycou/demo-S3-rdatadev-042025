# demo-S3-rdatadev-042025
Demo repository for hands-on session to get into object sotrage and S3

# Learn S3 with MinIO 🪣

This project provides a hands-on environment to learn how S3 object storage works using [MinIO](https://min.io/) – a high-performance, self-hosted S3-compatible storage service.

---

## 🚀 Getting Started

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







