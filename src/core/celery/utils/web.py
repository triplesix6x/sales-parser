import httpx
import logging

logger = logging.getLogger(__name__)


async def fetch_xml(url):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            logger.error(f"HTTP error fetching XML: {e}")
            return None


async def post_request(url, json):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"HTTP error in POST request: {e}")
            raise


async def patch_request(url, json):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url, json=json)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"HTTP error in PATCH request: {e}")
            raise
