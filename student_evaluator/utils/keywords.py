"""Utility functions for keyword detection and pattern matching."""

import re
from typing import List, Dict, Any


def find_keywords(text: str, patterns: List[str]) -> bool:
    """
    Check if any pattern matches in the text.
    
    Args:
        text: Input text to search
        patterns: List of regex patterns to match
        
    Returns:
        True if any pattern is found, False otherwise
    """
    text_lower = text.lower()
    for pattern in patterns:
        if re.search(pattern, text_lower):
            return True
    return False


def extract_name(text: str) -> str:
    """
    Extract student name from text.
    
    Args:
        text: Input text
        
    Returns:
        Extracted name or empty string
    """
    patterns = [
        r'myself\s+(\w+)',
        r'my\s+name\s+is\s+(\w+)',
        r'i\s+am\s+(\w+)',
        r'i\'m\s+(\w+)'
    ]
    
    text_lower = text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(1).capitalize()
    return ""


def count_sentences(text: str) -> int:
    """
    Count number of sentences in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
    """
    # Simple sentence splitting on . ! ?
    sentences = re.split(r'[.!?]+', text)
    # Filter out empty strings
    sentences = [s.strip() for s in sentences if s.strip()]
    return len(sentences)


def tokenize_words(text: str) -> List[str]:
    """
    Tokenize text into words.
    
    Args:
        text: Input text
        
    Returns:
        List of words
    """
    # Remove punctuation and split
    words = re.findall(r'\b\w+\b', text.lower())
    return words


def calculate_ttr(text: str) -> float:
    """
    Calculate Type-Token Ratio (vocabulary richness).
    
    Args:
        text: Input text
        
    Returns:
        TTR value (0 to 1)
    """
    words = tokenize_words(text)
    if not words:
        return 0.0
    
    unique_words = set(words)
    ttr = len(unique_words) / len(words)
    return round(ttr, 3)
