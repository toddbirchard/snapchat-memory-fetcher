"""Project configuration."""
from os import path

import simplejson as json

# Set project base path
basedir = path.abspath(path.dirname(__file__))

# Location of Snapchat data dump (exported from https://accounts.snapchat.com/accounts/welcome)
SNAPCHAT_MEMORIES_JSON = json.loads(
    open(f"{basedir}/export/json/memories_history.json").read()
)["Saved Media"]

# Checks if URLs have been fetched/decoded from previous runs
SNAPCHAT_DECODED_PHOTO_URLS = None
if path.exists(f"{basedir}/urls/photos.json"):
    photo_urls = json.loads(open(f"{basedir}/urls/photos.json").read())
    if photo_urls is not None and len(photo_urls) > 0:
        SNAPCHAT_DECODED_PHOTO_URLS = photo_urls

SNAPCHAT_DECODED_VIDEO_URLS = None
if path.exists(f"{basedir}/urls/videos.json"):
    video_urls = json.loads(open(f"{basedir}/urls/videos.json").read())
    if video_urls is not None and len(video_urls) > 0:
        SNAPCHAT_DECODED_VIDEO_URLS = video_urls

SNAPCHAT_MEDIA_URLS = {
    "videos": SNAPCHAT_DECODED_VIDEO_URLS,
    "photos": SNAPCHAT_DECODED_PHOTO_URLS,
}
