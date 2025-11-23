"""Clarity Analyzer - 15 points total."""

import re
from typing import Dict, Any, List
from ..config import FILLER_WORDS, MAX_SCORES
from ..utils.keywords import tokenize_words
from ..utils.scorer import score_filler_rate


class ClarityAnalyzer:
    """Analyzes clarity through filler word detection."""
    
    def __init__(self):
        self.max_score = MAX_SCORES['clarity']
        self.filler_words = FILLER_WORDS
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze clarity based on filler word usage.
        
        Args:
            text: Transcript text
            
        Returns:
            Dictionary with filler word analysis and score
        """
        words = tokenize_words(text)
        total_words = len(words)
        
        if total_words == 0:
            return {
                'score': self.max_score,
                'max_score': self.max_score,
                'filler_count': 0,
                'filler_rate': 0,
                'total_words': 0,
                'filler_details': {}
            }
        
        # Count filler words
        filler_count, filler_details = self._count_filler_words(text)
        
        # Calculate filler rate (percentage)
        filler_rate = (filler_count / total_words) * 100
        filler_rate = round(filler_rate, 2)
        
        # Get score
        score = score_filler_rate(filler_rate)
        
        return {
            'score': score,
            'max_score': self.max_score,
            'filler_count': filler_count,
            'filler_rate': filler_rate,
            'total_words': total_words,
            'filler_details': filler_details
        }
    
    def _count_filler_words(self, text: str) -> tuple:
        """
        Count occurrences of filler words.
        
        Args:
            text: Input text
            
        Returns:
            Tuple of (total_count, details_dict)
        """
        text_lower = text.lower()
        total_count = 0
        details = {}
        
        for filler in self.filler_words:
            # Use word boundary matching for single words
            # and phrase matching for multi-word fillers
            if ' ' in filler:
                # Multi-word filler (e.g., "you know")
                count = text_lower.count(filler)
            else:
                # Single word filler with word boundaries
                pattern = r'\b' + re.escape(filler) + r'\b'
                count = len(re.findall(pattern, text_lower))
            
            if count > 0:
                details[filler] = count
                total_count += count
        
        return total_count, details
