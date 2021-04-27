"""Fetcher configuration."""
from os import path

import simplejson as json

from log import LOGGER

# Set project base path
BASE_DIR = path.abspath(path.dirname(__file__))

# Location of Snapchat data dump from https://accounts.snapchat.com/accounts/welcome
SNAPCHAT_DATA_EXPORT = f"{BASE_DIR}/export"
SNAPCHAT_MEMORIES_EXPORT = f"{SNAPCHAT_DATA_EXPORT}/json/memories_history.json"
if path.exists(SNAPCHAT_MEMORIES_EXPORT):
    SNAPCHAT_MEMORIES_JSON = json.loads(open(SNAPCHAT_MEMORIES_EXPORT).read())[
        "Saved Media"
    ]
else:
    LOGGER.error(f"Snapchat data not found in `/export` folder.")
    raise Exception(f"Snapchat data not found in `/export` folder.")

# Check if media URLs have been decoded and saved from a previous run
SNAPCHAT_MEDIA_URLS = {
    "videos": None,
    "photos": None,
}

for k, v in SNAPCHAT_MEDIA_URLS.items():
    if path.exists(f"{BASE_DIR}/urls/{k}.json"):
        decoded_urls = json.loads(open(f"{BASE_DIR}/urls/{k}.json").read())
        if decoded_urls is not None and len(decoded_urls) > 0:
            SNAPCHAT_MEDIA_URLS[k] = decoded_urls


# Destination for fetched media files
MEDIA_EXPORT_FILEPATH = f"{BASE_DIR}/downloads"
if path.exists(MEDIA_EXPORT_FILEPATH) is False:
    raise Exception(f"Define a valid filepath for exported Snapchat memories.")
