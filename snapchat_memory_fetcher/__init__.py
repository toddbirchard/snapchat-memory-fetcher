"""Bulk download `Snapchat Memories` from a Snapchat data export."""
import simplejson as json

from config import BASE_DIR, SNAPCHAT_MEDIA_URLS
from log import LOGGER

from .decoder import decode_urls
from .fetcher import download_snapchat_memories
from .parse import parse_urls_from_export
from .writer import save_decoded_media_urls


def init_script():
    """Batch download all Snapchat memories."""
    for media_type in SNAPCHAT_MEDIA_URLS.keys():
        if SNAPCHAT_MEDIA_URLS[media_type] is None:
            parse_and_decode_urls(media_type)
        download_snapchat_memories(SNAPCHAT_MEDIA_URLS[media_type], media_type)
    LOGGER.success(f"Completed downloading all Snapchat memories.")


def parse_and_decode_urls(media_type: str):
    """
    Decode Snapchat memory URLs and save to local JSON file.

    :param media_type: Resource URLs to fetch.
    :type media_type: str
    :returns: dict
    """
    encoded_urls = parse_urls_from_export(media_type)
    media_urls = decode_urls(encoded_urls, media_type)
    save_decoded_media_urls(media_urls, media_type)
    return json.loads(open(f"{BASE_DIR}/urls/{media_type}.json").read())
