from .utils import get_env, positive_int
from .events_buffer import EventsBuffer
from .events_writer import AsyncEventsWriter
from .logging import get_logger


logger = get_logger(__name__)


def build_writer() -> AsyncEventsWriter:
    """
    Simple factory that chooses the blob backend based on an environment
    variable.
    """

    storage_type = get_env("AFLO_BACKEND_TYPE", default="s3").lower()

    logger.info("Building writer for: %s", storage_type)

    if storage_type == "s3":
        from .s3_client import S3Client

        client = S3Client()

    elif storage_type in ("azure", "azure-blob"):
        from .azure_blob_client import AzureBlobClient

        client = AzureBlobClient()

    else:
        raise ValueError(f"Unsupported 'storage type': {storage_type}")

    max_buffer_size = int(get_env("AFLO_MAX_BUFFER_SIZE", 10000, validate=positive_int))

    return AsyncEventsWriter(client, EventsBuffer(max_buffer_size=max_buffer_size))
