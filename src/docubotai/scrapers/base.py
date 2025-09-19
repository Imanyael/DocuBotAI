"""
Base scraper module for DocuBotAI.
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel


class ScrapedDocument(BaseModel):
    """Model representing a scraped document."""
    url: str
    title: str
    content: str
    metadata: Dict[str, Any]


class BaseScraper(ABC):
    """Base class for all documentation scrapers."""

    def __init__(self, output_dir: str | Path):
        """Initialize the scraper.

        Args:
            output_dir: Directory to save scraped documents.
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    async def scrape(self, source: str) -> List[ScrapedDocument]:
        """Scrape documentation from the specified source.

        Args:
            source: URL or path to documentation source.

        Returns:
            List of scraped documents.
        """
        pass

    @abstractmethod
    async def save(self, documents: List[ScrapedDocument]) -> None:
        """Save scraped documents to the output directory.

        Args:
            documents: List of scraped documents to save.
        """
        pass