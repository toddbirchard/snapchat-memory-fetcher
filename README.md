# Snapchat "Memories" Fetcher

![Python](https://img.shields.io/badge/Python-~3.9-blue.svg?logo=python&longCache=true&logoColor=white&colorB=5e81ac&style=flat-square&colorA=4c566a)
![AsyncIO](https://img.shields.io/badge/asyncio-^v3.4.3-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![AioFiles](https://img.shields.io/badge/aiofiles-^v3.5.0-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![AioHTTP](https://img.shields.io/badge/aiohttp-^v3.7.4-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![AioFiles](https://img.shields.io/badge/aiofiles-^v3.5.0-blue.svg?longCache=true&logo=python&style=flat-square&logoColor=white&colorB=5e81ac&colorA=4c566a)
![GitHub Last Commit](https://img.shields.io/github/last-commit/google/skia.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=a3be8c)
[![GitHub Issues](https://img.shields.io/github/issues/toddbirchard/snapchat-memory-fetcher.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/snapchat-memory-fetcher/issues)
[![GitHub Stars](https://img.shields.io/github/stars/toddbirchard/snapchat-memory-fetcher.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/snapchat-memory-fetcher/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/toddbirchard/snapchat-memory-fetcher.svg?style=flat-square&colorA=4c566a&logo=GitHub&colorB=ebcb8b)](https://github.com/toddbirchard/snapchat-memory-fetcher/network)

In compliance with the [California Consumer Privacy Act of 2018 (“CCPA”)](https://oag.ca.gov/privacy/ccpa), businesses which collect and store user data must allow customers the ability to request data the company has collected about the requesting user:

> "... you may ask businesses to disclose what personal information they have about you and what they do with that information, to delete your personal information and not to sell your personal information. You also have the right to be notified, before or at the point businesses collect your personal information, of the types of personal information they are collecting and what they may do with that information."

Many businesses (such as Snapchat) begrudgingly comply by "technically" allowing users to do this, but in such as way that is impossible for a human to parse. While Snapchat _technically_ allows users to request photos and videos Snapchat has stored (dubbed "Memories"), they do so in a way which is unusable by human beings. Sparing the technical details, exporting your account's memories is hidden behind a convoluted process of clicking individual URLs, which serve as proxies to reveal _actual_ URLs containing your data. 

The workflow Snapchat is intending to implement is unreasonable. To claim a single media file _which belongs to you_, users are expected to individually click URLs one-by-one. In reality, these URLs simply link to other URls, which will eventually fetch a single media file of the user. For context, by account has over 3500 media files.

Snapchat's practice of intentionally complicating this process is of questionable legality, and surely an act of defiance. This script automates the process of max-exporting media from Snapchat data exports to resolve this issue in the meantime while the questionable legality of Snapchat's practices are persued.

## Getting Started

### Requesting your data

1. User data can be requested from Snapchat [here](https://accounts.snapchat.com/accounts/welcome).
2. Under **Manage My Account**, select  *My Data*.
3. Your data export will be emailed to you as a **.zip** file containing the following:

```shell
/mydata_1618592678039
├── index.html
├── /html
│   └── *.html
└── /json
    └── *.json
```

### Running this script

1. Clone this repo (`git clone https://github.com/toddbirchard/snapchat-memory-fetcher.git`).
2. Drop the contents of your export to the `/export` directory of this repo.
3. Initialize project with requirements via  `make install`.
4. Run script via `make run`.

### Result

* The first time this script is run, it will export decoded URLs extracted from your data into JSON files as `/urls/photos.json` and `/urls/videos.json`. Urls only need to be decoded once and can be reused for future fetching.
* The script will then save all photos and videos associated with your account to `/downloads/photos` and `/downloads/videos`, respectively.

This script utilizes Python concurrency in both decoding URLS and fetching media, and therefore should run quickly. Note your hard drive space available as you may be downloading thousands of uncompressed videos.
