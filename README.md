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

### 3. Intéragir avec Minio

#### Créer un bucket et stocker des fichiers avec l'UI Minio
Se logger sur l'UI : `http://localhost:9001` et créer un bucket puis uploader un fichier dans le bucket.


#### Créer un bucket et stocker des fichiers avec le client Minio
- Utiliser la commande `mc ls` pour lister le bucket créé.
- Puis, utiliser la commande `mc mb` pour créer un nouveau bucket.
- AJouter un nouveau fichier avec la commande `mc put`.
- Jouer avec la commande `mc cp` pour copier un fichier, depuis un bucket vers le système local, depuis votre système local vers un bucket, entre deux buckets.
- Supprimer un fichier avec la commande `mc rm`
- Supprimer un bucket avec la commande `mc rb`

Regarder les possibilités qu'offre les commandes du client `mc`: https://min.io/docs/minio/linux/reference/minio-mc/mc-rm.html

### 4. L'API S3

L'API S3 est une API basée sur HTTP pour interagir avec le stockage, et cette API suit les principes REST (Representational State Transfer). L'API utilise des méthodes HTTP standard telles que GET, PUT, POST et DELETE.






