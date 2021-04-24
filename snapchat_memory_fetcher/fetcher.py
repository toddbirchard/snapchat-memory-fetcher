"""Fetch `Snapchat Memories` media files and save to local drive."""
import asyncio
from os import mkdir, path
from typing import Dict, List

import aiofiles
from aiohttp import ClientError, ClientSession, InvalidURL

from config import MEDIA_EXPORT_FILEPATH
from log import LOGGER


def fetch_snapchat_memories(decoded_memories: List[Dict[str, str]], media_type: str):
    """
    Fetch media files and save to local drive.

    :param decoded_memories: Resource URLs to fetch.
    :type decoded_memories: List[Dict[str, str]]
    :param media_type: Type of media to fetch (photo or video).
    :type media_type: str
    """
    if path.exists(f"{MEDIA_EXPORT_FILEPATH}/{media_type}") is False:
        mkdir(f"{MEDIA_EXPORT_FILEPATH}/{media_type}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(decoded_memories, media_type))
    LOGGER.success(f"Completed downloading {len(decoded_memories)} {media_type}.")


async def run(decoded_memory_urls: List[Dict[str, str]], media_type):
    """
    Create async HTTP session and fetch media from URLs.

    :param decoded_memory_urls: Resource URLs to fetch.
    :type decoded_memory_urls: List[Dict[str, str]]
    :param media_type: Type of media to fetch (photo or video).
    :type media_type: str
    """
    headers = {
        "connection": "keep-alive",
        "host": "sc-prod-memories-dmd-us-east-2.s3.us-east-2.amazonaws.com",
        "accept": "*/*",
    }
    decoded_memories = decoded_memory_urls
    async with ClientSession(headers=headers) as session:
        decoded_urls = await download_all(session, decoded_memories, media_type)
        return decoded_urls


async def download_all(session, decoded_memory_urls, media_type):
    """
    Concurrently download all photos/videos.

    :param session: Async HTTP requests session.
    :type session: ClientSession
    :param decoded_memory_urls: Resource URLs to fetch.
    :type decoded_memory_urls: List[Dict[str, str]]
    :param media_type: Type of media to fetch (photo or video).
    :type media_type: str
    """
    tasks = []
    for i, memory in enumerate(decoded_memory_urls):
        task = asyncio.create_task(
            fetch_snapchat_memory(
                session, memory, i, len(decoded_memory_urls), media_type
            )
        )
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetch_snapchat_memory(
    session, memory: dict, count: int, total_count: int, media_type: str
):
    """
    Download single media file and write to local directory.

    :param session: Async HTTP requests session.
    :type session: ClientSession
    :param memory: Resource URL to fetch with date as filename.
    :type memory: List[Dict[str, str]]
    :param count: Current URL count.
    :type count: int
    :param total_count: Total URL count.
    :type total_count: int
    :param media_type: Type of media to fetch (photo or video).
    :type media_type: str
    """
    if media_type == "photos":
        filepath = f"{MEDIA_EXPORT_FILEPATH}/{media_type}/{memory['date']}.jpg"
    else:
        filepath = f"{MEDIA_EXPORT_FILEPATH}/{media_type}/{memory['date']}.mp4"
    try:
        async with session.get(memory["url"]) as response:
            if response.status == 200:
                data = await response.read()
                async with aiofiles.open(filepath, mode="wb+") as f:
                    await f.write(data)
                    LOGGER.info(
                        f"Fetched {media_type} {count} of {total_count}: {memory['date']}"
                    )
                    await f.close()
    except InvalidURL as e:
        LOGGER.error(f"Unable to decode invalid URL `{memory['url']}`: {e}")
    except ClientError as e:
        LOGGER.error(f"Error while decoding URL `{memory['url']}`: {e}")
    except Exception as e:
        LOGGER.error(f"Unexpected error while decoding URL `{memory['url']}`: {e}")
