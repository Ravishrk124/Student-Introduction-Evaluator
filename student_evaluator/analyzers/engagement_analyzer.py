"""Engagement Analyzer - 15 points total."""

from typing import Dict, Any
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from ..config import MAX_SCORES
from ..utils.scorer import score_sentiment


class EngagementAnalyzer:
    """Analyzes engagement through sentiment analysis."""
    
    def __init__(self):
        self.max_score = MAX_SCORES['engagement']
        self.analyzer = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze engagement using sentiment analysis.
        
        Args:
            text: Transcript text
            
        Returns:
            Dictionary with sentiment scores and engagement score
        """
        if not text.strip():
            return {
                'score': 0,
                'max_score': self.max_score,
                'sentiment_compound': 0,
                'sentiment_positive': 0,
                'sentiment_neutral': 0,
                'sentiment_negative': 0,
                'interpretation': 'No text'
            }
        
        # Get sentiment scores
        sentiment_scores = self.analyzer.polarity_scores(text)
        
        # Extract compound score (normalized from -1 to 1)
        compound = sentiment_scores['compound']
        
        # Normalize compound to 0-1 scale (VADER compound is -1 to 1)
        # For positive scoring, we use the normalized compound score
        # This gives a better overall sentiment measure
        compound_normalized = (compound + 1) / 2  # Now 0 to 1
        
        # The rubric asks for "probability of positive words"
        # VADER compound score is a normalized weighted composite
        # We'll use the compound_normalized as our main metric
        positive_score_metric = compound_normalized
        
        # Calculate engagement score based on normalized compound
        score = score_sentiment(positive_score_metric)
        
        # Interpret sentiment
        if compound_normalized >= 0.7:
            interpretation = "Positive (enthusiastic, confident)"
        elif compound_normalized >= 0.5:
            interpretation = "Neutral (factual, calm)"
        else:
            interpretation = "Negative (disinterested, anxious)"
        
        return {
            'score': score,
            'max_score': self.max_score,
            'sentiment_compound': round(compound, 3),
            'sentiment_positive': round(sentiment_scores['pos'], 3),
            'sentiment_neutral': round(sentiment_scores['neu'], 3),
            'sentiment_negative': round(sentiment_scores['neg'], 3),
            'compound_normalized': round(compound_normalized, 3),
            'interpretation': interpretation
        }
