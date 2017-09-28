0.3.2 (2017-09-24)
******************

- Future-proofed XML utils for Django 2.0 compatibility
- Added false permalink to GUIDs because the GUIDs aren't URLs
- Added ``<itunes:new-feed-url>`` and old feed 301 redirect options
- iTunes show subtitles are stripped of HTML, making them consistent with episode summaries
- Removed legacy iTunes episode subtitles in favor of episode summaries
- Added filter by show in episode change list in the admin

0.3.1 (2017-09-23)
******************

- Hot-fixed old migration that was breaking the schema

0.3.0 (2017-09-23)
******************

- Added automatic detection of media file duration without needing MIME type
- Added iTunes season number tags
- Added iTunes episode number tags
- Added iTunes show type tags
- Added iTunes episode type tags
- Added iTunes episode title tags
- Converted iTunes episode summaries to episode show notes/``<content:encoded>`` tags
- Converted iTunes episode subtitles to episode summaries
- Added Bleach to strip HTML from show subtitles and summaries, and episode summaries and notes
- Added ``PODCAST_ALLOWED_TAGS`` setting to override iTunes-recommended tags with Bleach
- Converted GUIDs from enclosure URLs to SHA-256 hash of primary keys
- Redesigned default templates

0.2.2 (2017-07-17)
******************

- Added 404s for installs without shows or episodes
- Added demo
- Added iTunes badge and icon to documentation

0.2.1 (2017-07-17)
******************

- Hot-fixed include of tests in manifest

0.2.0 (2017-07-17)
******************

- Renamed project from Django iTunes Podcast to Django Apple Podcast
- Added iTunes badge and icon

0.1.9 (2017-07-17)
******************

- Added support for wheels
- Fixed over-escaped ampersand in category fixture
- Added template tag for single podcast check

0.1.8 (2017-04-05)
******************

- Exposed direct URL of media file enclosures
- Removed single podcast check mixin to simplify
- Made the logo better (or was that bigger?)
- Added old-school RSS link tags to default templates

0.1.7 (2017-04-03)
******************

- Added ``PODCAST_EPISODE_LIMIT`` setting to control number of episodes in feed

0.1.6 (2017-03-31)
******************

- Updated copyright year

0.1.5 (2016-11-06)
******************

- Internationalized title tag in default templates

0.1.4 (2016-11-02)
******************

- Removed pytz dependency

0.1.4 (2016-10-12)
******************

- Changed utils for Python 2/3 compatibility
- Removed six dependency
- Added namespacing to URLs
