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


@pytest.fixture(scope='function')
def workinstartups_api_response():
    """Generate a workinstartups format response."""
    class WIS(object):

        def __call__(self):
            return self.fake_response()

        @property
        def text(self):
            return self.fake_response()

        def fake_response(self):
            fake = Faker()
            raw_response = """var jobs = ["""
            for seq in range(1, 16):
                raw_response += """{{
"id":"{}",
"type_id":"1",
"category_id":"15",
"category_name":"Sales",
"company":"Smarter Applications",
"company_id":"189",
"url":"",
"title":"{}",
"url_title":"{}",
"location":"",
"location_outside_ro":null,
"is_location_anywhere":true,
"description":"{}",
"created_on":"30-04-2017",
"created":"30 Apr 2017",
"closed_on":"2017-05-30 16:16:17",
"apply":"",
"views_count":"18",
"city_id":null,
"mysql_date":"{}",
"apply_online":"1",
"is_active":"1",
"days_old":"0",
"is_spotlight":"0",
"type_name":"Full-time",
"type_var_name":"fulltime",
"salary_from":"30000",
"salary_to":null,
"salary_currency":"pounds",
"salary_frequency":"per_year",
"salary_frequency_label":"per year",
"expiration_date":"2017-06-30 23:59:59",
"expiration":"30 Jun 2017"
}},""".format(seq, fake.job(), fake.slug(), fake.text(max_nb_chars=500), fake.date_time_this_year(before_now=True).strftime("%Y-%m-%d %l:%M:%S")).replace('\n', '')

            raw_response = raw_response.rstrip(',')
            raw_response += "];"
            return raw_response
    return WIS()
