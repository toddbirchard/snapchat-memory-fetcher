"""Fetcher configuration."""
from os import path

import simplejson as json

from log import LOGGER

# Set project base path
BASE_DIR = path.abspath(path.dirname(__file__))

# Location of Snapchat data dump from https://accounts.snapchat.com/accounts/welcome
if path.exists(f"{BASE_DIR}/export/json/memories_history.json"):
    SNAPCHAT_MEMORIES_JSON = json.loads(
        open(f"{BASE_DIR}/export/json/memories_history.json").read()
    )["Saved Media"]
else:
    LOGGER.error(f"Snapchat data not found in `/export` folder.")
    raise Exception(f"Snapchat data not found in `/export` folder.")

# Check if media URLs have been decoded and saved from a previous run
SNAPCHAT_DECODED_MEMORIES_JSON = {
    "videos": None,
    "photos": None,
}

for k, v in SNAPCHAT_DECODED_MEMORIES_JSON.items():
    if path.exists(f"{BASE_DIR}/urls/{k}.json"):
        decoded_urls = json.loads(open(f"{BASE_DIR}/urls/{k}.json").read())
        if decoded_urls is not None and len(decoded_urls) > 0:
            SNAPCHAT_DECODED_MEMORIES_JSON[k] = decoded_urls


# Destination for fetched media files
MEDIA_EXPORT_FILEPATH = f"{BASE_DIR}/downloads"
if path.exists(MEDIA_EXPORT_FILEPATH) is False:
    raise Exception(f"Define a valid filepath for exported Snapchat memories.")
