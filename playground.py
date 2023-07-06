import requests
import feedparser

# URL for the arXiv RSS feed you're interested in.
# This is an example for the Computer Science category.
url = "http://arxiv.org/rss/cs"

response = requests.get(url)

feed = feedparser.parse(response.content)

# The 'entries' field contains individual items in the feed
for entry in feed.entries:
    print(entry)
    print("Title:", entry.title)
    print("Link:", entry.link)
    print("Published:", entry.published)
    print("Summary:", entry.summary)
    print()
    break

