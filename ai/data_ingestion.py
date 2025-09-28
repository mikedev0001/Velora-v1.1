import requests
import csv
import io
import logging

class DataIngestion:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def fetch_public_dataset(self, url):
        """Download and parse a CSV dataset from a public URL."""
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            content = resp.content.decode('utf-8')
            reader = csv.DictReader(io.StringIO(content))
            data = list(reader)
            self.logger.info(f"Fetched {len(data)} records from {url}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to fetch dataset: {e}")
            return []

    def fetch_threat_feed(self, feed_url, api_key=None):
        """Fetch JSON threat feed from an API or public endpoint."""
        headers = {'User-Agent': 'AI-Security-Agent'}
        if api_key:
            headers['Authorization'] = f"Bearer {api_key}"
        try:
            resp = requests.get(feed_url, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            self.logger.info(f"Fetched threat feed from {feed_url}")
            return data
        except Exception as e:
            self.logger.error(f"Failed to fetch threat feed: {e}")
            return []

# Example usage:
# ingestion = DataIngestion()
# dataset = ingestion.fetch_public_dataset('https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset')
# feed = ingestion.fetch_threat_feed('https://api.abuseipdb.com/api/v2/blacklist', api_key='YOUR_KEY')
