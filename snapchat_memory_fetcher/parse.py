"""Parse `Snapchat Memories` URLs from exported Snapchat data dump."""
from typing import Dict, List

from config import SNAPCHAT_MEMORIES_JSON
from log import LOGGER


def collect_encoded_urls(media_type: str) -> List[Dict[str, str]]:
    """
    Parse `Snapchat memories` URLs into convenient dictionary for a given data type.

    :param media_type: Resource URLs to fetch (either photos or videos).
    :type media_type: str
    :return: List[Dict[str, str]]
    """
    media_type_key = media_type.upper().replace("S", "")
    encoded_urls = [
        create_url_pair(m)
        for m in SNAPCHAT_MEMORIES_JSON
        if m["Media Type"] == media_type_key
    ]
    LOGGER.success(
        f"Found {len(encoded_urls)} {media_type} from Snapchat export export."
    )
    return encoded_urls


def create_url_pair(memory: Dict[str, str]):
    """
    Create a dictionary containing the URL and date of a single `Snapchat Memory`.

    :param memory: Dictionary of encoded media URLs.
    :type memory: Dict[str, str]
    :return: Dict[str, str]
    """
    memory_date = memory["Date"].replace(" UTC", "").replace(" ", "T").replace(":", ".")
    return {"date": memory_date, "url": memory["Download Link"]}
