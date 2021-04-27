"""Write decoded media URLs to local JSON."""
from typing import List

import simplejson as json

from config import BASE_DIR


def save_decoded_media_urls(decoded_urls: List[dict], media_type: str):
    """
    Write decoded URLs to a local JSON file for future use.

    :param decoded_urls: List of decoded URLs.
    :type decoded_urls: List[dict]
    :param media_type: Type of media that URLs were generated for.
    :type media_type: str
    """
    filepath = f"{BASE_DIR}/urls/{media_type}.json"
    with open(filepath, "w") as f:
        json.dump(
            decoded_urls,
            f,
            indent=4,
            sort_keys=True,
        )
        f.close()
