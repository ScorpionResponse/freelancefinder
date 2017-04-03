"""pytest global configuration."""
import random

from faker import Faker
import feedparser
import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Enable db across all tests."""
    pass


@pytest.fixture
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
