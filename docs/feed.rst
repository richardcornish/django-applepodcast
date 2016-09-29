.. _feed:

Feed
****

The show feed is optimized for submission to the iTunes Store by adding additional `iTunes-specific tags <https://help.apple.com/itc/podcasts_connect/#/itcb54353390>`_.

The following is the direct output of a show feed following the `RSS feed sample <https://help.apple.com/itc/podcasts_connect/#/itcbaf351599>`_ in the Podcasts Connect documentation as closely as possible. In the absence of the (fake) enclosure files, the enclosure files below were sampled from the `Serial <https://serialpodcast.org/>`_ podcast.

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
