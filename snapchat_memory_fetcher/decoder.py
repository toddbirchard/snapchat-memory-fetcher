"""Decode hidden URLs which host Snapchat memories & save URLs to local JSON."""
import asyncio
from typing import Dict, List

from aiohttp import ClientError, ClientSession, InvalidURL

from log import LOGGER


def decode_urls(
    encoded_urls: List[Dict[str, str]], media_type: str
) -> List[Dict[str, str]]:
    """
    Decode video and photo URLs.

    :param encoded_urls: Resource URLs to fetch.
    :type encoded_urls: List[Dict[str, str]]
    :param media_type: Resource URLs to fetch.
    :type media_type: str
    :returns: List[Dict[str, str]]
    """
    loop = asyncio.get_event_loop()
    urls = loop.run_until_complete(run(encoded_urls, media_type))
    LOGGER.success(f"Decoded {len(urls)} {media_type} URLs.")
    return urls


async def run(encoded_urls: List[Dict[str, str]], media_type) -> List[dict]:
    """
    Create async HTTP session and decode all URLs.

    :param encoded_urls: Resource URLs to decode.
    :type encoded_urls: Dict[str, List[Dict[str, str]]]
    :param media_type: Type of media urls to generate.
    :type media_type: str
    """
    headers = {
        "authority": "app.snapchat.com",
        "content-type": "application/x-www-form-urlencoded",
        "accept": "*/*",
    }
    async with ClientSession(headers=headers) as session:
        decoded_urls = await fetch_all(session, encoded_urls, media_type)
        return decoded_urls


async def fetch_all(
    session: ClientSession, media_urls: List[Dict[str, str]], media_type: str
) -> List[Dict[str, str]]:
    """
    Asynchronously decode all URLs.

    :param session: Async HTTP requests session.
    :type session: ClientSession
    :param media_urls: Resource URLs to fetch.
    :type media_urls: List[Dict[str, str]]
    :param media_type: Type of media urls to generate.
    :type media_type: str
    :returns: List[Dict[str, str]]
    """
    tasks = []
    for i, media_source in enumerate(media_urls):
        task = asyncio.create_task(
            fetch_decoded_url(session, media_source, i, len(media_urls), media_type)
        )
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def fetch_decoded_url(
    session, media_source: Dict[str, str], count: int, total_count: int, media_type: str
) -> Dict[str, str]:
    """
    Fetch URL and create a dictionary representing the resource.

    :param session: Async HTTP requests session.
    :type session: ClientSession
    :param media_source: Single resource to fetch.
    :type media_source: Dict[str, str]
    :param count: Current URL count.
    :type count: int
    :param total_count: Total URL count.
    :type total_count: int
    :param media_type: Type of media urls to generate.
    :type media_type: str
    :returns: Dict[str, str]
    """
    try:
        async with session.post(media_source["url"]) as response:
            decoded_url = await response.text()
            if decoded_url == "":
                raise Exception(
                    f"Decoded URL returned empty string; export may have expired."
                )
            resource = {"url": decoded_url, "date": media_source["date"]}
            LOGGER.info(f"Decoded {count} of {total_count} {media_type}: {decoded_url}")
            return resource
    except InvalidURL as e:
        LOGGER.error(f"Unable to decode invalid URL `{media_source['date']}`: {e}")
        raise e
    except ClientError as e:
        LOGGER.error(f"Error while decoding URL `{media_source['date']}`: {e}")
        raise e
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        raise e
