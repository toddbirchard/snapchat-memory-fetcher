"""Bulk download `Snapchat Memories` from a Snapchat data export."""
import simplejson as json

from config import BASE_DIR, SNAPCHAT_DECODED_MEMORIES_JSON
from log import LOGGER

from .decoder import decode_urls
from .fetcher import fetch_snapchat_memories
from .parse import collect_encoded_urls
from .writer import write_decoded_urls


def init_script():
    """Batch download all Snapchat memories."""
    for media_type in SNAPCHAT_DECODED_MEMORIES_JSON.keys():
        if SNAPCHAT_DECODED_MEMORIES_JSON[media_type] is None:
            decoded_memory_urls = parse_and_decode_urls(media_type)
            fetch_snapchat_memories(decoded_memory_urls, media_type)
        else:
            fetch_snapchat_memories(
                SNAPCHAT_DECODED_MEMORIES_JSON[media_type], media_type
            )
    LOGGER.success(f"Completed downloading all Snapchat memories.")


def parse_and_decode_urls(media_type: str):
    """
    Decode Snapchat memory URLs and save to local JSON file.

    :param media_type: Resource URLs to fetch.
    :type media_type: str
    :returns: dict
    """
    encoded_urls = collect_encoded_urls(media_type)
    encoded_urls = decode_urls(encoded_urls, media_type)
    write_decoded_urls(encoded_urls, media_type)
    return json.loads(open(f"{BASE_DIR}/urls/{media_type}.json").read())
