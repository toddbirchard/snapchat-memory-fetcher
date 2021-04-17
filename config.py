from os import path

import simplejson as json

# Set project base path
basedir = path.abspath(path.dirname(__file__))

SNAPCHAT_MEMORIES_JSON = json.loads(open("data/json/memories_history.json").read())[
    "Saved Media"
]
