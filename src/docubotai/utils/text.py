"""
Text processing utilities for DocuBotAI.
"""
import re
from typing import List

from bs4 import BeautifulSoup


def clean_html(html: str) -> str:
    """Clean HTML content by removing tags and normalizing whitespace.

    Args:
        html: HTML content to clean.

    Returns:
        Cleaned text content.
    """
    # Parse HTML
    soup = BeautifulSoup(html, "html.parser")
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text content
    text = soup.get_text()
    
    # Normalize whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = " ".join(chunk for chunk in chunks if chunk)
    
    return text


def extract_code_blocks(text: str) -> List[tuple[str, str]]:
    """Extract code blocks from markdown text.

    Args:
        text: Markdown text to process.

    Returns:
        List of tuples containing (language, code).
    """
    # Match code blocks with language specification
    pattern = r"```(\w+)\n(.*?)\n```"
    matches = re.finditer(pattern, text, re.DOTALL)
    
    code_blocks = []
    for match in matches:
        language = match.group(1)
        code = match.group(2).strip()
        code_blocks.append((language, code))
    
    return code_blocks


def normalize_text(text: str) -> str:
    """Normalize text by cleaning and standardizing format.

    Args:
        text: Text to normalize.

    Returns:
        Normalized text.
    """
    # Convert to lowercase
    text = text.lower()
    
    # Replace multiple spaces with single space
    text = re.sub(r"\s+", " ", text)
    
    # Remove special characters
    text = re.sub(r"[^\w\s]", "", text)
    
    # Strip whitespace
    text = text.strip()
    
    return text


def split_into_sentences(text: str) -> List[str]:
    """Split text into sentences.

    Args:
        text: Text to split.

    Returns:
        List of sentences.
    """
    # Simple sentence splitting based on common punctuation
    sentences = re.split(r"[.!?]+", text)
    
    # Clean and filter sentences
    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]
    
    return sentences


def calculate_text_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts using simple token overlap.

    Args:
        text1: First text.
        text2: Second text.

    Returns:
        Similarity score between 0 and 1.
    """
    # Normalize texts
    text1 = normalize_text(text1)
    text2 = normalize_text(text2)
    
    # Split into tokens
    tokens1 = set(text1.split())
    tokens2 = set(text2.split())
    
    # Calculate Jaccard similarity
    intersection = len(tokens1.intersection(tokens2))
    union = len(tokens1.union(tokens2))
    
    if union == 0:
        return 0.0
    
    return intersection / union