"""Content and Structure Analyzer - 40 points total."""

import re
from typing import Dict, Any
from ..config import (
    SALUTATION_EXCELLENT,
    SALUTATION_GOOD,
    SALUTATION_NORMAL,
    SALUTATION_SCORES,
    MUST_HAVE_KEYWORDS,
    GOOD_TO_HAVE_KEYWORDS,
    CLOSING_PHRASES,
    MAX_SCORES
)
from ..utils.keywords import find_keywords


class ContentAnalyzer:
    """Analyzes content structure and completeness of introduction."""
    
    def __init__(self):
        self.max_salutation = MAX_SCORES['salutation']
        self.max_keywords = MAX_SCORES['keywords']
        self.max_flow = MAX_SCORES['flow']
        self.max_total = MAX_SCORES['content_total']
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze content and structure.
        
        Args:
            text: Transcript text
            
        Returns:
            Dictionary with scores and details
        """
        salutation_result = self._analyze_salutation(text)
        keywords_result = self._analyze_keywords(text)
        flow_result = self._analyze_flow(text)
        
        total_score = (
            salutation_result['score'] + 
            keywords_result['score'] + 
            flow_result['score']
        )
        
        return {
            'salutation': salutation_result,
            'keywords': keywords_result,
            'flow': flow_result,
            'total_score': total_score,
            'max_score': self.max_total,
            'percentage': round((total_score / self.max_total) * 100, 1)
        }
    
    def _analyze_salutation(self, text: str) -> Dict[str, Any]:
        """Analyze salutation level (5 points)."""
        text_lower = text.lower()
        first_sentence = text.split('.')[0].lower() if '.' in text else text[:100].lower()
        
        # Check excellent salutations
        for phrase in SALUTATION_EXCELLENT:
            if phrase in first_sentence:
                return {
                    'score': SALUTATION_SCORES['excellent'],
                    'max_score': self.max_salutation,
                    'level': 'Excellent',
                    'phrase_found': phrase
                }
        
        # Check good salutations
        for phrase in SALUTATION_GOOD:
            if phrase in first_sentence:
                return {
                    'score': SALUTATION_SCORES['good'],
                    'max_score': self.max_salutation,
                    'level': 'Good',
                    'phrase_found': phrase
                }
        
        # Check normal salutations
        for phrase in SALUTATION_NORMAL:
            if phrase in first_sentence:
                return {
                    'score': SALUTATION_SCORES['normal'],
                    'max_score': self.max_salutation,
                    'level': 'Normal',
                    'phrase_found': phrase
                }
        
        return {
            'score': SALUTATION_SCORES['none'],
            'max_score': self.max_salutation,
            'level': 'None',
            'phrase_found': None
        }
    
    def _analyze_keywords(self, text: str) -> Dict[str, Any]:
        """Analyze keyword presence (30 points max: 20 must-have + 10 good-to-have)."""
        must_have_score = 0
        must_have_found = []
        
        # Check must-have keywords (4 points each, max 20)
        for keyword, data in MUST_HAVE_KEYWORDS.items():
            if find_keywords(text, data['patterns']):
                must_have_score += data['score']
                must_have_found.append(keyword)
        
        # Cap at 20 points
        must_have_score = min(must_have_score, 20)
        
        good_to_have_score = 0
        good_to_have_found = []
        
        # Check good-to-have keywords (2 points each, max 10)
        for keyword, data in GOOD_TO_HAVE_KEYWORDS.items():
            if find_keywords(text, data['patterns']):
                good_to_have_score += data['score']
                good_to_have_found.append(keyword)
        
        # Cap at 10 points
        good_to_have_score = min(good_to_have_score, 10)
        
        total_keyword_score = must_have_score + good_to_have_score
        
        return {
            'score': total_keyword_score,
            'max_score': self.max_keywords,
            'must_have': {
                'score': must_have_score,
                'max': 20,
                'found': must_have_found,
                'count': len(must_have_found)
            },
            'good_to_have': {
                'score': good_to_have_score,
                'max': 10,
                'found': good_to_have_found,
                'count': len(good_to_have_found)
            }
        }
    
    def _analyze_flow(self, text: str) -> Dict[str, Any]:
        """
        Analyze flow/order (5 points).
        Expected order: Salutation → Basic details → Additional details → Closing
        """
        text_lower = text.lower()
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if not sentences:
            return {
                'score': 0,
                'max_score': self.max_flow,
                'order_followed': False,
                'reason': 'No sentences found'
            }
        
        # Check if there's a closing
        has_closing = any(
            re.search(pattern, text_lower) 
            for pattern in CLOSING_PHRASES
        )
        
        # Simple heuristic: Check if salutation is in first sentence
        # and closing is near the end
        has_salutation_first = any(
            phrase in sentences[0].lower()
            for phrase in SALUTATION_EXCELLENT + SALUTATION_GOOD + SALUTATION_NORMAL
        )
        
        # Award full points if basic structure is present
        if has_salutation_first or has_closing:
            return {
                'score': self.max_flow,
                'max_score': self.max_flow,
                'order_followed': True,
                'has_salutation_first': has_salutation_first,
                'has_closing': has_closing
            }
        
        # Partial credit if at least some structure exists
        return {
            'score': 2,
            'max_score': self.max_flow,
            'order_followed': False,
            'has_salutation_first': has_salutation_first,
            'has_closing': has_closing
        }
