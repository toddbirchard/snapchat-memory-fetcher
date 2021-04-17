"""Bulk download `Snapchat Memories` from a Snapchat data export (https://accounts.snapchat.com/accounts/welcome)"""
import simplejson as json

from config import SNAPCHAT_MEDIA_URLS, basedir
from log import LOGGER

from .decoder import decode_urls
from .fetcher import fetch_snapchat_memories
from .parse import collect_encoded_urls
from .writer import write_decoded_urls


def init_script():
    """Download Snapchat memories."""
    for media_type in SNAPCHAT_MEDIA_URLS.keys():
        if SNAPCHAT_MEDIA_URLS[media_type] is None:
            decoded_memory_urls = parse_and_decode_urls(media_type)
            fetch_snapchat_memories(decoded_memory_urls, media_type)
        else:
            fetch_snapchat_memories(SNAPCHAT_MEDIA_URLS[media_type], media_type)
    LOGGER.success(f"Completed downloading all Snapchat memories.")


def parse_and_decode_urls(media_type: str):
    """
    Parse Snapchat memory URLs from exported export & save decoded URLs to local JSON.

    :param media_type: Resource URLs to fetch.
    :type media_type: str
    :returns: dict
    """
    encoded_urls = collect_encoded_urls(media_type)
    encoded_urls = decode_urls(encoded_urls, media_type)
    write_decoded_urls(encoded_urls, media_type)
    return json.loads(open(f"{basedir}/urls/{media_type}.json").read())
