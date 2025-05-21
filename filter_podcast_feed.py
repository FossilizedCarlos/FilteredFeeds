import os
import re
import feedparser
import yaml
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, ElementTree


def extract_front_matter(md_content):
    match = re.search(r'^---\s*\n(.*?)\n---\s*\n', md_content, re.DOTALL)
    if match:
        return yaml.safe_load(match.group(1))
    return None


def match_keywords(text, keywords):
    if not keywords:
        return True
    if isinstance(keywords, str):
        keywords = [keywords]
    return any(kw.lower() in text.lower() for kw in keywords)


def filter_episodes(feed_url, include=None, exclude=None, filter_type='include', max_episodes=None):
    d = feedparser.parse(feed_url)
    episodes = d.entries

    if filter_type == "exclude":
        episodes = [ep for ep in episodes if not match_keywords(ep.title, exclude)]
    elif filter_type == "include":
        episodes = [ep for ep in episodes if match_keywords(ep.title, include)]
    elif filter_type == "both":
        episodes = [ep for ep in episodes if not match_keywords(ep.title, exclude)]
        episodes = [ep for ep in episodes if match_keywords(ep.title, include)]

    episodes.sort(key=lambda ep: ep.get("published_parsed", datetime.min), reverse=True)
    if max_episodes:
        episodes = episodes[:max_episodes]

    return d.feed, episodes


def create_filtered_feed(feed_info, episodes, output_file):
    rss = Element('rss', version='2.0')
    channel = SubElement(rss, 'channel')
    
    for tag in ['title', 'link', 'description']:
        if tag in feed_info:
            el = SubElement(channel, tag)
            el.text = feed_info[tag]
    
    for entry in episodes:
        item = SubElement(channel, 'item')
        SubElement(item, 'title').text = entry.get('title')
        SubElement(item, 'link').text = entry.get('link')
        SubElement(item, 'guid').text = entry.get('guid', entry.get('link'))
        SubElement(item, 'pubDate').text = entry.get('published', '')
    
        if 'description' in entry:
            SubElement(item, 'description').text = entry['description']
    
        # Add <enclosure> if available
        if 'enclosures' in entry and entry.enclosures:
            enclosure = entry.enclosures[0]  # use the first enclosure
            if 'href' in enclosure:
                SubElement(item, 'enclosure', {
                    'url': enclosure['href'],
                    'length': enclosure.get('length', '0'),
                    'type': enclosure.get('type', 'audio/mpeg')
                })
    
    tree = ElementTree(rss)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)


# Main script
for file in os.listdir():
    if file.endswith('.md') and file.lower() != 'readme.md':
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()

        metadata = extract_front_matter(content)
        if not metadata or 'feed' not in metadata or 'name' not in metadata:
            continue

        feed_url = metadata['feed']
        name = metadata['name']
        include = metadata.get('include', [])
        exclude = metadata.get('exclude', [])
        filter_type = metadata.get('filter type', 'include').strip().lower()
        episodes = metadata.get('episodes')

        try:
            episodes = int(episodes)
        except:
            episodes = None

        feed_info, filtered_episodes = filter_episodes(
            feed_url,
            include=include,
            exclude=exclude,
            filter_type=filter_type,
            max_episodes=episodes
        )

        create_filtered_feed(feed_info, filtered_episodes, f"{name}.xml")
