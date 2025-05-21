# filter_podcast_feed.py
import feedparser
import xml.etree.ElementTree as ET
import requests

FEED_URL = "https://www.omnycontent.com/d/playlist/e73c998e-6e60-432f-8610-ae210140c5b1/1508ddb2-0c9a-42f6-aafe-ae3300346aa9/bf391792-153e-41b3-9d3d-ae3300346ad8/podcast.rss"
KEYWORD = "Best of The Herd"

response = requests.get(FEED_URL)
response.raise_for_status()

root = ET.fromstring(response.content)
channel = root.find('channel')
items = channel.findall('item')

for item in items:
    title_elem = item.find('title')
    if title_elem is None or KEYWORD.lower() not in title_elem.text.lower():
        channel.remove(item)

tree = ET.ElementTree(root)
tree.write("filtered.xml", encoding="utf-8", xml_declaration=True)
