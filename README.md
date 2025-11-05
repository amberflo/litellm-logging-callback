# Amberflo's LiteLLM logging callback

Logging callback for LiteLLM in order to meter your LLM usage and monitor your costs in Amberflo.

## How to Use

First, make sure you can run LiteLLM without the Amberflo callback.

Add the [amberflo](./amberflo) folder to your LiteLLM container instance and configure the callback in your LiteLLM config:
- You can download it from a [release](https://github.com/amberflo/litellm-logging-callback/releases).

```yaml
litellm_settings:
  callbacks:
    - "amberflo.litellm.callback"
```

Then set the environment variables following the templates in order to configure secrets and other options:
- [azure-blob.env.template](./azure-blob.env.template)
- [s3.env.template](./s3.env.template)

Sample docker command:
```sh
docker run \
    --env-file .env \
    --volume ./amberflo:/app/amberflo:ro \
    --volume ./litellm-config.yaml:/app/config.yaml \
    --publish 4000:4000 \
    ghcr.io/berriai/litellm:v1.79.0-stable --config /app/config.yaml
```

## Development

Configure the secrets in the `.env` file:
```
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...

AZURE_STORAGE_CONNECTION_STRING=...

AFLO_BACKEND_TYPE=s3

AFLO_BUCKET_NAME=...
AFLO_PATH=...
AFLO_CONTAINER_NAME=...
```

Install dependencies and run common tasks:
- `make setup`
- `make fix`
- `make lint`
- `make test`

Run a local database and LiteLLM container:
- `docker compose up -d postgres`
- `docker compose up --build litellm`
    - Press `w` to automatically restart LiteLLM upon code changes

Adjust configurations and environment variables in:
- `litellm-config.yaml`
- `docker-compose.yml`
