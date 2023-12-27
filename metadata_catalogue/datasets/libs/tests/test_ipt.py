import logging
from unittest.mock import patch

import pytest

from ...models import Dataset
from ..ipt import rss_to_datasets

RSS_TEXT = """
<rss version="2.0" xmlns:ipt="http://ipt.gbif.org/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <channel>
    <title>NINA IPT service</title>
    <link>https://ipt.nina.no</link>
    <atom:link href="https://ipt.nina.no/rss.do" rel="self" type="application/rss+xml"/>
    <description>Resource metadata of NINA IPT service</description>
    <language>en-us</language>
      <!-- RFC-822 date-time / Wed, 02 Oct 2010 13:00:00 GMT -->
      <pubDate>Tue, 05 May 2015 09:54:05 +0000</pubDate>
      <lastBuildDate>Mon, 25 Dec 2023 12:00:03 +0000</lastBuildDate>
      <!-- UUID of the IPT making RSS feed available -->
      <ipt:identifier>e312f477-a9ba-485e-8c1c-700868a0bfb7</ipt:identifier>
    <generator>GBIF IPT 2.7.6-rd4b666d</generator>
      <webMaster>rv@nina.no (Roald Vang)</webMaster>
    <docs>http://cyber.law.harvard.edu/rss/rss.html</docs>
    <ttl>15</ttl>
      <geo:Point>
        <geo:lat>63.413916</geo:lat>
        <geo:long>10.406317</geo:long>
      </geo:Point>
      <item>
        <title>NINA Artskart data - Version 1.336</title>
        <link>https://ipt.nina.no/resource?r=nina_artskart</link>
        <!-- shows what changed in this version, or shows the resource description if change summary was empty -->
        <description>[Several smaller datasets with biodiversity data delivered from NINA to The Norwegian Biodiversity Information Centres Species Map Service, https://artskart.artsdatabanken.no. New datasets are added regularly.]</description>
        <author>rv@nina.no (Roald Vang)</author>
        <ipt:eml>https://ipt.nina.no/eml.do?r=nina_artskart</ipt:eml>
        <ipt:dwca>https://ipt.nina.no/archive.do?r=nina_artskart</ipt:dwca>
        <pubDate>Mon, 25 Dec 2023 12:00:14 +0000</pubDate>
        <guid isPermaLink="false">4a832966-48ad-4d83-858c-044705f74cac/v1.336</guid>
      </item>
  </channel>
</rss>
"""


def mocked_getLogger(name):
    # You can customize the behavior of the mock logger as needed
    mock_logger = logging.getLogger(name)
    mock_logger.setLevel(logging.DEBUG)
    return mock_logger


@pytest.mark.django_db(transaction=True)
@patch("metadata_catalogue.datasets.libs.ipt.async_task")
@patch("metadata_catalogue.datasets.libs.ipt.logger.warn")
def test_rss_to_datasets(logger_mock, task_mock):
    rss_to_datasets(RSS_TEXT)
    assert task_mock.called
    assert not logger_mock.called

    assert Dataset.objects.count() == 1


RSS_TEXT_NO_DWCA = """
<rss version="2.0" xmlns:ipt="http://ipt.gbif.org/" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#">
  <channel>
    <title>NINA IPT service</title>
    <link>https://ipt.nina.no</link>
    <atom:link href="https://ipt.nina.no/rss.do" rel="self" type="application/rss+xml"/>
    <description>Resource metadata of NINA IPT service</description>
    <language>en-us</language>
      <!-- RFC-822 date-time / Wed, 02 Oct 2010 13:00:00 GMT -->
      <pubDate>Tue, 05 May 2015 09:54:05 +0000</pubDate>
      <lastBuildDate>Mon, 25 Dec 2023 12:00:03 +0000</lastBuildDate>
      <!-- UUID of the IPT making RSS feed available -->
      <ipt:identifier>e312f477-a9ba-485e-8c1c-700868a0bfb7</ipt:identifier>
    <generator>GBIF IPT 2.7.6-rd4b666d</generator>
      <webMaster>rv@nina.no (Roald Vang)</webMaster>
    <docs>http://cyber.law.harvard.edu/rss/rss.html</docs>
    <ttl>15</ttl>
      <geo:Point>
        <geo:lat>63.413916</geo:lat>
        <geo:long>10.406317</geo:long>
      </geo:Point>
      <item>
        <title>NINA Artskart data - Version 1.336</title>
        <link>https://ipt.nina.no/resource?r=nina_artskart</link>
        <!-- shows what changed in this version, or shows the resource description if change summary was empty -->
        <description>[Several smaller datasets with biodiversity data delivered from NINA to The Norwegian Biodiversity Information Centres Species Map Service, https://artskart.artsdatabanken.no. New datasets are added regularly.]</description>
        <author>rv@nina.no (Roald Vang)</author>
        <ipt:eml>https://ipt.nina.no/eml.do?r=nina_artskart</ipt:eml>
        <pubDate>Mon, 25 Dec 2023 12:00:14 +0000</pubDate>
        <guid isPermaLink="false">4a832966-48ad-4d83-858c-044705f74cac/v1.336</guid>
      </item>
  </channel>
</rss>
"""


@pytest.mark.django_db(transaction=True)
@patch("metadata_catalogue.datasets.libs.ipt.async_task")
@patch("metadata_catalogue.datasets.libs.ipt.logger.warn")
def test_rss_to_datasets_no_dwca(logger_mock, task_mock):
    rss_to_datasets(RSS_TEXT_NO_DWCA)
    assert not task_mock.called
    assert logger_mock.called

    assert Dataset.objects.count() == 0
