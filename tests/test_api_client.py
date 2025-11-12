import unittest
from unittest.mock import AsyncMock, patch
from tenacity import wait_none

from amberflo.api_client import ApiClient


class TestApiClient(unittest.IsolatedAsyncioTestCase):
    """
    Test class for the ApiClient.
    """

    @patch("aiohttp.ClientSession.post")
    async def test_valid_request(self, mock_post):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(return_value="Ingested 2 events")
        mock_response.status = 200
        mock_response.ok = True

        mock_post.return_value.__aenter__.return_value = mock_response

        endpoint = "https://localhost/ingest"
        data = bytes()

        client = ApiClient(api_key="test", endpoint=endpoint)
        try:
            await client.put_object("key-123", data)
        finally:
            await client.session.close()

        mock_post.assert_called_once_with(endpoint, data=data)

    @patch("aiohttp.ClientSession.post")
    async def test_invalid_request(self, mock_post):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(
            return_value='{"errorMessage": "Validation error..."}'
        )
        mock_response.status = 400
        mock_response.ok = False

        mock_post.return_value.__aenter__.return_value = mock_response

        endpoint = "https://localhost/ingest"
        data = bytes()

        client = ApiClient(api_key="test", endpoint=endpoint)
        try:
            await client.put_object("key-123", data)
        finally:
            await client.session.close()

        mock_post.assert_called_once_with(endpoint, data=data)

    @patch("aiohttp.ClientSession.post")
    async def test_server_error(self, mock_post):
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(
            return_value='{"message": "Internal server error"}'
        )
        mock_response.status = 500
        mock_response.ok = False

        mock_post.return_value.__aenter__.return_value = mock_response

        endpoint = "https://localhost/ingest"
        data = bytes()

        client = ApiClient(api_key="test", endpoint=endpoint)

        client._send_with_retry.retry.wait = wait_none()  # type: ignore

        try:
            with self.assertRaises(RuntimeError):
                await client.put_object("key-123", data)
        finally:
            await client.session.close()

        mock_post.assert_called_with(endpoint, data=data)
