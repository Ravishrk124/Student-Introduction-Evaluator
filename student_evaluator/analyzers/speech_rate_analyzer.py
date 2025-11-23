"""Speech Rate Analyzer - 10 points total."""

from typing import Dict, Any
from ..config import SPEECH_RATE_RANGES, MAX_SCORES
from ..utils.scorer import score_from_range
from ..utils.keywords import tokenize_words


class SpeechRateAnalyzer:
    """Analyzes speech rate (words per minute)."""
    
    def __init__(self):
        self.max_score = MAX_SCORES['speech_rate']
    
    def analyze(self, text: str, duration_seconds: int) -> Dict[str, Any]:
        """
        Analyze speech rate.
        
        Args:
            text: Transcript text
            duration_seconds: Duration of speech in seconds
            
        Returns:
            Dictionary with WPM and score
        """
        if duration_seconds <= 0:
            return {
                'wpm': 0,
                'score': 0,
                'max_score': self.max_score,
                'label': 'Invalid duration',
                'error': 'Duration must be greater than 0'
            }
        
        words = tokenize_words(text)
        word_count = len(words)
        
        # Calculate WPM
        wpm = (word_count / duration_seconds) * 60
        wpm = round(wpm, 1)
        
        # Get score from ranges
        result = score_from_range(wpm, SPEECH_RATE_RANGES)
        
        return {
            'wpm': wpm,
            'word_count': word_count,
            'duration_seconds': duration_seconds,
            'score': result['score'],
            'max_score': self.max_score,
            'label': result['label']
        }
