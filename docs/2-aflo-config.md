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

## Sample Configuration

```yaml
# for api
AFLO_BACKEND_TYPE=api
AFLO_API_KEY=...

# for aws s3
AFLO_BACKEND_TYPE=s3
AFLO_BUCKET_NAME=...

AFLO_PATH=litellm-metering

AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...

# for azure blob
AFLO_BACKEND_TYPE=azure-blob
AFLO_CONTAINER_NAME=...

AFLO_PATH=litellm-metering

AZURE_STORAGE_CONNECTION_STRING=...

# common configs
AFLO_HOSTED_ENV=testing
AFLO_BATCH_SIZE=10
AFLO_FLUSH_INTERVAL=30
AFLO_SEND_OBJECT_METADATA=true
```
