# Filtered Podcast Feeds via GitHub Actions

This repository automatically creates filtered versions of podcast RSS feeds using simple `.md` files for configuration. Filtered feeds can be served via GitHub Pages and subscribed to in any podcast app.

---

## Features

- Filter podcast feeds by keywords (`include`, `exclude`, or both)
- YAML front matter config — no code needed
- Output valid RSS feeds with:
  - Audio `<enclosure>` tags
  - iTunes-compatible podcast cover images
- GitHub Actions automation:
  - On `.md` file changes: generates new feeds
  - Every 12 hours: refreshes existing feeds

---

## Setup Instructions

### 1. Create Feed Config Files

Each feed is defined in a Markdown file (e.g., `pod.md`) like this:

```yaml
---
feed: "https://example.com/podcast.rss"
episodes: 35                    # Number of episodes to retain (default: all)
filter type: "both"             # include, exclude, or both
exclude:
  - "bonus"
  - "replay"
include:
  - "Best of"
  - "Top Segment"
name: "pod"                    # Output filename will be: pod.xml
---
```

You can have as many of these files as you want. Each one generates its own `.xml` feed.

---

### 2. GitHub Pages (Optional)

Enable GitHub Pages under **Settings > Pages**. Choose:
- Branch: `main`
- Folder: `/ (root)`

Your feed will be available at:

```text
https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/herd.xml
```

---

### 3. Actions Included

#### `generate-from-md.yml`
Triggered when any `.md` file (except `README.md`) is added or updated.

- Parses feed config
- Fetches and filters episodes
- Outputs XML feeds

#### `refresh-feeds.yml`
Runs every 12 hours (cron job) to keep existing feeds fresh.

---

## How It Works

Feeds are parsed using `feedparser` and filtered based on `title` keywords. Filter results are saved to `.xml` files containing:

- Channel metadata
- Episode items
- Enclosure links
- iTunes podcast image (when available)

---


## 🔧 Dependencies

These are installed automatically in the GitHub Actions:

```bash
pip install feedparser pyyaml
```
