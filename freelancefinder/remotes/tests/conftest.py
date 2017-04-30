"""pytest directory configuration."""
import random

from faker import Faker
import feedparser
import pytest
import pytz


@pytest.fixture(scope='function')
def fossjobs_rss_feed():
    """Generate a fake rss feed like the fossjobs feed."""
    fake = Faker()
    raw_rss = """<?xml version="1.0" encoding="utf-8"?>
    <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns="http://purl.org/rss/1.0/" xmlns:dc="http://purl.org/dc/elements/1.1/">
    <channel rdf:about="https://www.fossjobs.net/rss.xml">
    <description>Latest jobs</description>
    <link>https://www.fossjobs.net/</link>
    <title>fossjobs.net</title>
    <dc:date>03-04-2017</dc:date>
    <items>
        <rdf:Seq>
            <rdf:li rdf:resource="https://www.fossjobs.net/1/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/2/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/3/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/4/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/5/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/6/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/7/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/8/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/9/"/>
            <rdf:li rdf:resource="https://www.fossjobs.net/10/"/>
        </rdf:Seq>
    </items>
    </channel>
   """
    for seq in range(1, 11):
        job_type = random.choice(['[Full-time]', '[Part-time]', '[Freelance]'])
        raw_rss += """
            <item rdf:about="https://www.fossjobs.net/{}/">
                <description>{}</description>
                <link>{}</link>
                <title>{} {}</title>
                <dc:date>{}</dc:date>
            </item>
            """.format(seq, fake.text(max_nb_chars=500), fake.url(), job_type, fake.job(), fake.iso8601(tzinfo=None))
    raw_rss += "</rdf:RDF>"
    return feedparser.parse(raw_rss)


@pytest.fixture(scope='function')
def trabajospython_rss_feed():
    """Generate a fake rss feed like the trabajospython feed."""
    fake = Faker()
    raw_rss = """<?xml version="1.0" encoding="ISO-8859-1"?>
<?xml-stylesheet type="text/xsl" media="screen" href="/~d/styles/rss2full.xsl"?><?xml-stylesheet type="text/css" media="screen" href="http://feeds.feedburner.com/~d/styles/itemcontent.css"?><rss version="2.0">
  <channel>
    <title>TrabajosPython</title>
    <description>Software-Development</description>
    <link>http://www.trabajospython.com/</link>
    <language>es</language>
    <atom10:link xmlns:atom10="http://www.w3.org/2005/Atom" rel="self" type="application/rss+xml" href="http://feeds.feedburner.com/trabajos_python" /><feedburner:info xmlns:feedburner="http://rssnamespace.org/feedburner/ext/1.0" uri="trabajos_python" /><atom10:link xmlns:atom10="http://www.w3.org/2005/Atom" rel="hub" href="http://pubsubhubbub.appspot.com/" />
   """
    for seq in range(1, 11):
        raw_rss += """
            <item>
                <pubDate>{}</pubDate>
                <title>{}</title>
                <link>{}</link>
                <description>{}</description>
            </item>
            """.format(fake.date_time_this_year(before_now=True, tzinfo=pytz.timezone('UTC')).strftime('%a, %e %b %Y %H:%M:%S %z'), fake.job(), fake.url(), fake.text(max_nb_chars=500))
    raw_rss += """</channel>
    </rss>
    """

    return feedparser.parse(raw_rss)
