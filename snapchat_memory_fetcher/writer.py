"""Write decoded media URLs to local JSON."""
from typing import List

import simplejson as json

from config import basedir


def write_decoded_urls(decoded_urls: List[dict], media_type: str):
    """
    Write results to local JSON file.

    :param decoded_urls: List of decoded URLs.
    :type decoded_urls: List[dict]
    :param media_type: Type of media that URLs were generated for.
    :type media_type: str
    """
    filepath = f"{basedir}/urls/{media_type}.json"
    with open(filepath, "w") as f:
        json.dump(
            decoded_urls,
            f,
            indent=4,
            sort_keys=True,
        )
        f.close()
