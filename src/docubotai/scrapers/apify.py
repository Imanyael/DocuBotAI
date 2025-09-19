"""
Apify-powered scraper implementation for DocuBotAI.
"""
import json
from pathlib import Path
from typing import List

from apify_client import ApifyClient
from loguru import logger

from docubot.scrapers.base import BaseScraper, ScrapedDocument


class ApifyScraper(BaseScraper):
    """Apify-powered documentation scraper."""

    def __init__(
        self,
        output_dir: str | Path,
        apify_token: str | None = None,
        actor_id: str = "apify/website-content-crawler",
    ):
        """Initialize the Apify scraper.

        Args:
            output_dir: Directory to save scraped documents.
            apify_token: Apify API token. If not provided, will try to get from environment.
            actor_id: ID of the Apify actor to use for scraping.
        """
        super().__init__(output_dir)
        self.client = ApifyClient(apify_token)
        self.actor_id = actor_id

    async def scrape(self, source: str) -> List[ScrapedDocument]:
        """Scrape documentation using Apify.

        Args:
            source: URL of the documentation to scrape.

        Returns:
            List of scraped documents.
        """
        logger.info(f"Starting Apify scraper for {source}")
        
        # Start the actor and wait for it to finish
        run = self.client.actor(self.actor_id).call(
            run_input={
                "startUrls": [{"url": source}],
                "maxCrawlingDepth": 5,
                "maxPagesPerCrawl": 100,
                "onlyContent": True,
            }
        )

        # Get the actor run's dataset
        documents = []
        for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
            doc = ScrapedDocument(
                url=item["url"],
                title=item.get("title", ""),
                content=item.get("text", ""),
                metadata={
                    "html": item.get("html", ""),
                    "timestamp": item.get("timestamp"),
                    "depth": item.get("depth", 0),
                }
            )
            documents.append(doc)

        logger.info(f"Scraped {len(documents)} documents from {source}")
        return documents

    async def save(self, documents: List[ScrapedDocument]) -> None:
        """Save scraped documents to JSON files.

        Args:
            documents: List of scraped documents to save.
        """
        for i, doc in enumerate(documents):
            output_file = self.output_dir / f"doc_{i:04d}.json"
            with open(output_file, "w") as f:
                json.dump(doc.model_dump(), f, indent=2)
        
        logger.info(f"Saved {len(documents)} documents to {self.output_dir}")