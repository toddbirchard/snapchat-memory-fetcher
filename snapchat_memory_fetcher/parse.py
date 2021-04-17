"""Parse exported Snapchat dump for encoded memory URLs."""
from typing import Dict, List

from config import SNAPCHAT_MEMORIES_JSON
from log import LOGGER


def parse_encoded_memories() -> Dict[str, List[Dict[str, str]]]:
    """
    Filter and return saved Snapchat memories.

    :return: Dict[str, List[Dict[str, str]]]
    """
    videos = [
        create_memory_pair(m)
        for m in SNAPCHAT_MEMORIES_JSON
        if m["Media Type"] == "VIDEO"
    ]
    photos = [
        create_memory_pair(m)
        for m in SNAPCHAT_MEMORIES_JSON
        if m["Media Type"] == "PHOTO"
    ]
    LOGGER.success(
        f"Found {len(videos)} videos and {len(photos)} photos from saved Snapchat memories."
    )
    return {"videos": videos, "photos": photos}


def create_memory_pair(memory: Dict[str, str]):
    """
    Create a dictionary containing the URL and date of a single memory.

    :param memory: Dictionary containing data for a single Snapchat memory.
    :type memory: Dict[str, str]
    :return: Dict[str, str]
    """
    return {"date": memory["Date"].split(" ")[0], "url": memory["Download Link"]}
