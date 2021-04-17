from .decoder import export_decoded_urls
from .parse import parse_encoded_memories
from .writer import write_decoded_urls


def init_script():
    """Download Snapchat memories."""
    media_sources = parse_encoded_memories()
    photos, videos = export_decoded_urls(media_sources)
    write_decoded_urls(videos, "videos")
    write_decoded_urls(photos, "photos")
