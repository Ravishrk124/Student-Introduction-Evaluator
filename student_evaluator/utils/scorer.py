"""Scorer utility for mapping values to score ranges."""

from typing import Dict, Any


def score_from_range(value: float, ranges: list) -> Dict[str, Any]:
    """
    Map a value to a score based on defined ranges.
    
    Args:
        value: Value to score
        ranges: List of range dictionaries with 'min', 'max', 'score' keys
        
    Returns:
        Dictionary with score and label
    """
    for range_def in ranges:
        if range_def['min'] <= value <= range_def['max']:
            return {
                'score': range_def['score'],
                'label': range_def.get('label', ''),
                'value': value
            }
    return {'score': 0, 'label': 'Unknown', 'value': value}


def score_grammar(errors_per_100: float) -> int:
    """
    Calculate grammar score based on error rate.
    
    Formula: Score = 1 - min(errors_per_100 / 10, 1)
    Then map to point scale.
    
    Args:
        errors_per_100: Number of errors per 100 words
        
    Returns:
        Grammar score (0-10)
    """
    normalized = 1 - min(errors_per_100 / 10, 1)
    
    if normalized >= 0.9:
        return 10
    elif normalized >= 0.7:
        return 8
    elif normalized >= 0.5:
        return 6
    elif normalized >= 0.3:
        return 4
    else:
        return 2


def score_vocabulary(ttr: float) -> int:
    """
    Score vocabulary richness based on TTR.
    
    Args:
        ttr: Type-Token Ratio (0 to 1)
        
    Returns:
        Vocabulary score (0-10)
    """
    if ttr >= 0.9:
        return 10
    elif ttr >= 0.7:
        return 8
    elif ttr >= 0.5:
        return 6
    elif ttr >= 0.3:
        return 4
    else:
        return 2


def score_filler_rate(filler_rate: float) -> int:
    """
    Score based on filler word rate.
    
    Args:
        filler_rate: Percentage of filler words (0-100)
        
    Returns:
        Clarity score (0-15)
    """
    if filler_rate <= 3:
        return 15
    elif filler_rate <= 6:
        return 12
    elif filler_rate <= 9:
        return 9
    elif filler_rate <= 12:
        return 6
    else:
        return 3


def score_sentiment(compound_score: float) -> int:
    """
    Score based on sentiment compound score.
    
    Args:
        compound_score: VADER compound score (0 to 1)
        
    Returns:
        Engagement score (0-15)
    """
    if compound_score >= 0.9:
        return 15
    elif compound_score >= 0.7:
        return 12
    elif compound_score >= 0.5:
        return 9
    elif compound_score >= 0.3:
        return 6
    else:
        return 3
