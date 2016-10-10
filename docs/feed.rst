.. _feed:

Feed
****

Sample
======

The show feed is optimized for submission to the iTunes Store by adding additional `iTunes-specific tags <https://help.apple.com/itc/podcasts_connect/#/itcb54353390>`_.

The following is the direct output of a show feed following the `RSS feed sample <https://help.apple.com/itc/podcasts_connect/#/itcbaf351599>`_ in the Podcasts Connect documentation as closely as possible.

.. code-block:: xml

   <?xml version="1.0" encoding="utf-8"?>
   <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">
       <channel>
           <title>All About Everything</title>
           <link>http://127.0.0.1:8000/podcasts/all-about-everything/</link>
           <description>All About Everything is a show about everything. Each week we dive into any subject known to man and talk about it as much as we can. Look for our podcast in the Podcasts app or in the iTunes Store</description>
           <atom:link rel="self" href="http://127.0.0.1:8000/podcasts/all-about-everything/feed/" />
           <language>en-us</language>
           <category>Arts</category>
           <category>Arts / Food</category>
           <category>TV &amp; Film</category>
           <category>Technology</category>
           <category>Technology / Gadgets</category>
           <lastBuildDate>Fri, 11 Mar 2016 01:15:00 +0000</lastBuildDate>
           <ttl>1440</ttl>
           <copyright>&#x2117; &amp; &#xA9; 2016 John Doe &amp; Family</copyright>
           <image>
               <url>http://127.0.0.1:8000/static/podcast/img/no_artwork.png</url>
               <title>All About Everything</title>
               <link>http://127.0.0.1:8000/podcasts/all-about-everything/</link>
           </image>
           <itunes:subtitle><![CDATA[A show about everything]]></itunes:subtitle>
           <itunes:summary><![CDATA[All About Everything is a show about everything. Each week we dive into any subject known to man and talk about it as much as we can. Look for our podcast in the Podcasts app or in the iTunes Store]]></itunes:summary>
           <itunes:author>John Doe</itunes:author>
           <itunes:owner>
               <itunes:name>John Doe</itunes:name>
               <itunes:email>john.doe@example.com</itunes:email>
           </itunes:owner>
           <itunes:image href="http://127.0.0.1:8000/static/podcast/img/no_artwork.png" />
           <itunes:category text="Arts">
               <itunes:category text="Food" />
           </itunes:category>
           <itunes:category text="TV &amp; Film" />
           <itunes:category text="Technology">
               <itunes:category text="Gadgets" />
           </itunes:category>
           <itunes:explicit>no</itunes:explicit>
           <itunes:block>no</itunes:block>
           <itunes:complete>no</itunes:complete>
           <item>
               <title>Red, Whine, &amp; Blue</title>
               <link>http://127.0.0.1:8000/podcasts/all-about-everything/red-whine-blue/</link>
               <description>This week we talk about surviving in a Red state if you are a Blue person. Or vice versa.</description>
               <pubDate>Fri, 11 Mar 2016 01:15:00 +0000</pubDate>
               <guid>http://127.0.0.1:8000/podcasts/all-about-everything/red-whine-blue/</guid>
               <enclosure length="16021583" url="http://127.0.0.1:8000/media/podcast/enclosures/files/04_S01_Episode_04__Inconsistencies.mp3" type="audio/mpeg" />
               <category>Arts</category>
               <category>Arts / Food</category>
               <category>TV &amp; Film</category>
               <category>Technology</category>
               <category>Technology / Gadgets</category>
               <author>john.doe@example.com</author>
               <itunes:subtitle><![CDATA[Red + Blue != Purple]]></itunes:subtitle>
               <itunes:summary><![CDATA[This week we talk about surviving in a Red state if you are a Blue person. Or vice versa.]]></itunes:summary>
               <itunes:author>John Doe</itunes:author>
               <itunes:image href="http://127.0.0.1:8000/media/podcast/episodes/episode-4.png" />
               <itunes:explicit>no</itunes:explicit>
               <itunes:block>no</itunes:block>
               <itunes:isClosedCaptioned>no</itunes:isClosedCaptioned>
               <itunes:duration>33:10</itunes:duration>
           </item>
           <item>
               <title>The Best Chili</title>
               <link>http://127.0.0.1:8000/podcasts/all-about-everything/best-chili/</link>
               <description>This week we talk about the best Chili in the world. Which chili is better?</description>
               <pubDate>Thu, 10 Mar 2016 02:00:00 +0000</pubDate>
               <guid>http://127.0.0.1:8000/podcasts/all-about-everything/best-chili/</guid>
               <enclosure length="13469034" url="http://127.0.0.1:8000/media/podcast/enclosures/files/03_S01_Episode_03__Leakin_Park.mp3" type="audio/mpeg" />
               <category>Arts</category>
               <category>Arts / Food</category>
               <category>TV &amp; Film</category>
               <category>Technology</category>
               <category>Technology / Gadgets</category>
               <author>john.doe@example.com</author>
               <itunes:subtitle><![CDATA[Jane and Eric]]></itunes:subtitle>
               <itunes:summary><![CDATA[This week we talk about the best Chili in the world. Which chili is better?]]></itunes:summary>
               <itunes:author>John Doe</itunes:author>
               <itunes:image href="http://127.0.0.1:8000/media/podcast/episodes/episode-3.png" />
               <itunes:explicit>no</itunes:explicit>
               <itunes:block>no</itunes:block>
               <itunes:isClosedCaptioned>no</itunes:isClosedCaptioned>
               <itunes:duration>27:45</itunes:duration>
           </item>
           <item>
               <title>Socket Wrench Shootout</title>
               <link>http://127.0.0.1:8000/podcasts/all-about-everything/socket-wrench-shootout/</link>
               <description>This week we talk about metric vs. Old English socket wrenches. Which one is better? Do you really need both? Get all of your answers here.</description>
               <pubDate>Wed, 09 Mar 2016 13:00:00 +0000</pubDate>
               <guid>http://127.0.0.1:8000/podcasts/all-about-everything/socket-wrench-shootout/</guid>
               <enclosure length="17244194" url="http://127.0.0.1:8000/media/podcast/enclosures/files/02_S01_Episode_02__The_Breakup.mp3" type="audio/mpeg" />
               <category>Arts</category>
               <category>Arts / Food</category>
               <category>TV &amp; Film</category>
               <category>Technology</category>
               <category>Technology / Gadgets</category>
               <author>john.doe@example.com</author>
               <itunes:subtitle><![CDATA[Comparing socket wrenches is fun!]]></itunes:subtitle>
               <itunes:summary><![CDATA[This week we talk about metric vs. Old English socket wrenches. Which one is better? Do you really need both? Get all of your answers here.]]></itunes:summary>
               <itunes:author>John Doe</itunes:author>
               <itunes:image href="http://127.0.0.1:8000/media/podcast/episodes/episode-2.png" />
               <itunes:explicit>no</itunes:explicit>
               <itunes:block>no</itunes:block>
               <itunes:isClosedCaptioned>no</itunes:isClosedCaptioned>
               <itunes:duration>35:45</itunes:duration>
           </item>
           <item>
               <title>Shake Shake Shake Your Spices</title>
               <link>http://127.0.0.1:8000/podcasts/all-about-everything/shake-shake-shake-your-spices/</link>
               <description>This week we talk about &lt;a href="https://itunes/apple.com/us/book/antique-trader-salt-pepper/id429691295?mt=11"&gt;salt and pepper shakers&lt;/a&gt;, comparing and contrasting pour rates, construction materials, and overall aesthetics. Come and join the party!</description>
               <pubDate>Tue, 08 Mar 2016 12:00:00 +0000</pubDate>
               <guid>http://127.0.0.1:8000/podcasts/all-about-everything/shake-shake-shake-your-spices/</guid>
               <enclosure length="25775366" url="http://127.0.0.1:8000/media/podcast/enclosures/files/01_S01_Episode_01__The_Alibi.mp3" type="audio/mpeg" />
               <category>Arts</category>
               <category>Arts / Food</category>
               <category>TV &amp; Film</category>
               <category>Technology</category>
               <category>Technology / Gadgets</category>
               <author>john.doe@example.com</author>
               <itunes:subtitle><![CDATA[A short primer on table spices]]></itunes:subtitle>
               <itunes:summary><![CDATA[This week we talk about <a href="https://itunes/apple.com/us/book/antique-trader-salt-pepper/id429691295?mt=11">salt and pepper shakers</a>, comparing and contrasting pour rates, construction materials, and overall aesthetics. Come and join the party!]]></itunes:summary>
               <itunes:author>John Doe</itunes:author>
               <itunes:image href="http://127.0.0.1:8000/media/podcast/episodes/episode-1.png" />
               <itunes:explicit>no</itunes:explicit>
               <itunes:block>no</itunes:block>
               <itunes:isClosedCaptioned>no</itunes:isClosedCaptioned>
               <itunes:duration>53:31</itunes:duration>
           </item>
       </channel>
   </rss>

Sample differences
==================

Although every effort was made to recreate the `RSS feed sample <https://help.apple.com/itc/podcasts_connect/#/itcbaf351599>`_ on Podcasts Connnect as closely as possible, the limitations of the way in which Django creates feeds and the occassional stray error in the feed sample itself required small changes:

* The ``RssFeed`` class in Django's deep syndication class hierarchy |adds an <atom:link>|_ to the ``<channel>`` element that would require a significant code duplication and rewrite to eliminate. It does not affect iTunes Store compatibility and thus remains in the show feed.
* The ``<atom:link>`` previously mentioned can only exist in a correponding XML namespace; i.e. the attribute ``xmlns:atom="http://www.w3.org/2005/Atom"`` in the ``<rss>`` element. The attribute could be easily removed, but would prevent the feed from achieving XML validation. The Atom XML namespace thus remains in the show feed.
* The ``RssFeed`` class |adds a <lastBuildDate>|_ to the ``<channel>`` element that corresponds to the ``<pubDate>`` of the latest ``<item>``. Due to Django's deep syndication class hierarchy, it remains in the show feed.
* In the RSS feed sample, the ``<copyright>`` element contains a year of 2014. The sample is replaced with the current year, at the time of this writing, 2016.
* In the RSS feed sample, ``<itunes:summary>`` tag in the "Shake Shake Shake Your Spices" episode has an errant space in its ``<![CDATA[...]]>`` tag. The sample displays ``<![CDATA[...]] >``. The show feed removes the errant space.
* In the RSS feed sample, the domain in URLs is ``www.example.com`` or ``example.com``. Django's `testing framework <https://github.com/django/django/blob/1.10/django/test/client.py#L283>`_ uses the server name ``testserver``. The feed test replaces ``www.example.com`` with ``testserver``.
* In the RSS feed sample, the absolute URL of the show is ``/podcasts/everything/index.html``. In the interest of `clean URLs <https://docs.djangoproject.com/en/1.10/topics/http/urls/>`_, the feed test removes ``index.html``.
* In the RSS feed sample, only instances of ``<itunes:summary>`` or ``<itunes:subtitle>`` that have HTML contain ``<![CDATA[...]]>`` tags to escape the HTML. Rather than conditionally insert ``<![CDATA[...]]>`` tags, they are inserted in all instances of ``<itunes:summary>`` and ``<itunes:subtitle>``.
* In the RSS feed sample, the enclosure ``url`` of an ``<item>`` is often different from the ``<guid>``, e.g. ``http://example.com/podcasts/everything/AllAboutEverythingEpisode3.m4a`` vs. ``http://example.com/podcasts/archive/aae20140615.m4a``. The ``<guid>`` of an ``<item>`` is normalized to return the enclosure URL and eliminate a competing, arbitrary URL.
* In the RSS feed sample, the (fake) enclosure files have accompanying fake values in ``<itunes:duration>`` elements. The app automatically reads the duration of media files using the Python `Mutagen <https://pypi.python.org/pypi/mutagen>`_ package, and their durations are not subject to manual editing.
* In the RSS feed sample, the enclosure ``length`` of an ``<item>`` is similarly determined by automatically reading the enclosure `size of the file <https://docs.djangoproject.com/en/1.10/ref/files/file/#django.core.files.File.size>`_.
* In the RSS feed sample, ``<item>`` elements omit ``<link>`` and ``<description>`` elements. While `technically valid <https://cyber.harvard.edu/rss/rss.html#hrelementsOfLtitemgt>`_, Django encourages its use by automatically querying for an item's absolute URL, and thus each item's ``<link>`` and ``<description>`` are preserved.
* In the RSS feed sample, the ``<item>`` elements contain ``<pubDate>`` values whose time zones are inconsistent: ``GMT`` (which is `obsolete <https://en.wikipedia.org/wiki/Greenwich_Mean_Time>`_), ``EST``, ``-0700``, and ``+3000`` (which should be ``+0300``). Because Django defines ``TIME_ZONE`` at the project level in `settings <https://docs.djangoproject.com/en/1.10/ref/settings/#std:setting-TIME_ZONE>`_, it's impossible to display datetimes in the show feed with different UTC offsets. For example, given a datetime ``2016-03-11T01:15:00+0300`` (which might be, say, ``'Europe/Moscow'``), a setting of ``TIME_ZONE = 'UTC'`` would ultimately result in a display of ``Thu, 10 Mar 2016 22:15:00 +0000``, that is, moving three hours backward to achieve UTC, which would be around 10 p.m. the prior evening. All values of ``<pubDate>`` elements have been converted to the UTC time zone.
* In the RSS feed sample, the "Red,Whine, & Blue" episode contains a ``<pubDate>`` element whose value is ``Fri, 11 Mar 2016 01:15:00 +3000``. There exists no ``+3000`` UTC time offset, as described in the `list of tz database time zones <https://en.wikipedia.org/wiki/List_of_tz_database_time_zones>`_.
* The show feed and RSS feed sample only compare semantic differences, i.e. parsed content, and not syntax differences, i.e. various orderings of elements, capitialization, orderings of attributes, and spaces, etc. Django's |assertXMLEqual|_ is used to assert equality.

.. |adds an <atom:link>| replace:: adds an ``<atom:link>``
.. _adds an <atom:link>: https://github.com/django/django/blob/1.10/django/utils/feedgenerator.py#L265

.. |adds a <lastBuildDate>| replace:: adds a ``<lastBuildDate>``
.. _adds a <lastBuildDate>: https://github.com/django/django/blob/1.10/django/utils/feedgenerator.py#L272

.. |assertXMLEqual| replace:: ``assertXMLEqual``
.. _assertXMLEqual: https://docs.djangoproject.com/en/1.10/topics/testing/tools/#django.test.SimpleTestCase.assertXMLEqual
