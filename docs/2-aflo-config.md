
# Amberflo Callback Configuration
Amberflo can write meter events either to an AWS S3 bucket or Azure Blob container.

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| **Backend Selection** | | | |
| `AFLO_BACKEND_TYPE` | Yes | `s3` | Storage backend type. Valid values: `api`, `s3`, `azure-blob` |
| **Amberflo API Configuration** | | | |
| `AFLO_API_KEY` | Yes (for API) | - | Amberflo API key |
| `AFLO_API_ENDPOINT` | No | `https://ingest.amberflo.io` | Amberflo ingest API endpoint |
| **AWS S3 Configuration** | | | |
| `AWS_ACCESS_KEY_ID` | Yes (for S3) | - | AWS access key ID for S3 authentication |
| `AWS_SECRET_ACCESS_KEY` | Yes (for S3) | - | AWS secret access key for S3 authentication |
| `AWS_REGION` | Yes (for S3) | - | AWS region where the S3 bucket is located |
| `AFLO_BUCKET_NAME` | Yes (for S3) | - | Name of the S3 bucket to store logs |
| **Azure Blob Configuration** | | | |
| `AZURE_STORAGE_CONNECTION_STRING` | Yes (for Azure) | - | Azure Storage connection string for authentication |
| `AFLO_CONTAINER_NAME` | Yes (for Azure) | - | Name of the Azure Blob container to store logs |
| **Common Configuration** | | | |
| `AFLO_PATH` | No | `litellm-metering` | Path prefix for stored log files |
| `AFLO_HOSTED_ENV` | No | `prod` | Environment identifier for log categorization |
| `AFLO_JSON_LOGS` | No | `true` | Enable JSON formatted console logs (`true`/`false`) |
| `AFLO_DEBUG` | No | `false` | Enable debug logging (`true`/`false`) |
| `AFLO_BATCH_SIZE` | No | `100` | Number of events to batch before writing |
| `AFLO_FLUSH_INTERVAL` | No | `300` | Interval in seconds to flush events (5 minutes) |
| `AFLO_MAX_BUFFER_SIZE` | No | `10000` | Maximum number of events to buffer in memory |
| `AFLO_SEND_OBJECT_METADATA` | No | `false` | Creates business units and `team` virtual tags in Amberflo |

### API env file
```YAML
AFLO_BACKEND_TYPE=api
AFLO_API_KEY=...
AFLO_API_ENDPOINT=https://ingest.amberflo.io
AFLO_HOSTED_ENV=prod
AFLO_JSON_LOGS=false
AFLO_DEBUG=false
AFLO_BATCH_SIZE=100
AFLO_FLUSH_INTERVAL=300 # 5 minutes
AFLO_MAX_BUFFER_SIZE=10000 # optional
```

### AWS S3 env file
```YAML
AFLO_BACKEND_TYPE=s3
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...
AFLO_BUCKET_NAME=...
AFLO_PATH=litellm-metering
AFLO_HOSTED_ENV=prod
AFLO_JSON_LOGS=false
AFLO_DEBUG=false
AFLO_BATCH_SIZE=100
AFLO_FLUSH_INTERVAL=300 # 5 minutes
AFLO_MAX_BUFFER_SIZE=10000 # optional
```

### Azure Blob env file
```YAML
AFLO_BACKEND_TYPE=azure-blob
AZURE_STORAGE_CONNECTION_STRING=...
AFLO_CONTAINER_NAME=...
AFLO_PATH=litellm-metering
AFLO_HOSTED_ENV=prod
AFLO_JSON_LOGS=false
AFLO_DEBUG=false
AFLO_BATCH_SIZE=100
AFLO_FLUSH_INTERVAL=300 # 5 minutes
AFLO_MAX_BUFFER_SIZE=10000 # optional
```
