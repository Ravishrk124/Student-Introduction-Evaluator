"""Configuration constants for the evaluation tool."""

# Salutation patterns and scores
SALUTATION_EXCELLENT = ["i am excited to introduce", "feeling great", "i'm excited to introduce"]
SALUTATION_GOOD = ["good morning", "good afternoon", "good evening", "good day", "hello everyone"]
SALUTATION_NORMAL = ["hi", "hello", "hey"]

SALUTATION_SCORES = {
    'excellent': 5,
    'good': 4,
    'normal': 2,
    'none': 0
}

# Keyword patterns for content analysis
MUST_HAVE_KEYWORDS = {
    'name': {
        'patterns': [r'\bmyself\s+(\w+)', r'\bmy\s+name\s+is\s+(\w+)', r'\bi\s+am\s+(\w+)', r'\bi\'m\s+(\w+)'],
        'score': 4
    },
    'age': {
        'patterns': [r'\b(\d+)\s+years?\s+old\b', r'\bage\s+(\d+)', r'\bi\s+am\s+(\d+)'],
        'score': 4
    },
    'school_class': {
        'patterns': [r'\bclass\s+\d+', r'\bgrade\s+\d+', r'\bschool\b', r'\bstudying\s+in', r'\bsection\b'],
        'score': 4
    },
    'family': {
        'patterns': [r'\bfamily\b', r'\bmother\b', r'\bfather\b', r'\bparents\b', r'\bsibling', r'\bbrother\b', r'\bsister\b'],
        'score': 4
    },
    'hobbies': {
        'patterns': [r'\bhobb', r'\blike\s+to\b', r'\benjoy\b', r'\blove\s+to\b', r'\bplay\b', r'\binterest'],
        'score': 4
    }
}

GOOD_TO_HAVE_KEYWORDS = {
    'about_family': {
        'patterns': [r'\bspecial\s+thing\s+about\s+my\s+family\b', r'\bfamily\s+is\b', r'\bkind\s+hearted\b'],
        'score': 2
    },
    'origin': {
        'patterns': [r'\bi\s+am\s+from\b', r'\blive\s+in\b', r'\bparents\s+are\s+from\b', r'\bcity\b', r'\bvillage\b'],
        'score': 2
    },
    'ambition': {
        'patterns': [r'\bgoal\b', r'\bdream\b', r'\bambition\b', r'\bwant\s+to\s+be\b', r'\baspire\b', r'\bfuture\b'],
        'score': 2
    },
    'fun_fact': {
        'patterns': [r'\bfun\s+fact\b', r'\binteresting\s+thing\b', r'\bunique\b', r'\bspecial\b', r'\bdon\'t\s+know\s+about\s+me\b'],
        'score': 2
    },
    'strengths': {
        'patterns': [r'\bstrength\b', r'\bachievement\b', r'\bgood\s+at\b', r'\bexcel\b', r'\btalent\b'],
        'score': 2
    }
}

# Filler words list
FILLER_WORDS = [
    "um", "uh", "like", "you know", "so", "actually", "basically", 
    "right", "i mean", "well", "kinda", "sort of", "okay", "hmm", "ah"
]

# Speech rate (WPM) ranges and scores
SPEECH_RATE_RANGES = [
    {'min': 161, 'max': float('inf'), 'score': 2, 'label': 'Too Fast'},
    {'min': 141, 'max': 160, 'score': 6, 'label': 'Fast'},
    {'min': 111, 'max': 140, 'score': 10, 'label': 'Ideal'},
    {'min': 81, 'max': 110, 'score': 6, 'label': 'Slow'},
    {'min': 0, 'max': 80, 'score': 2, 'label': 'Too Slow'}
]

# Maximum scores for each criterion
MAX_SCORES = {
    'salutation': 5,
    'keywords': 30,
    'flow': 5,
    'content_total': 40,
    'speech_rate': 10,
    'grammar': 10,
    'vocabulary': 10,
    'grammar_total': 20,
    'clarity': 15,
    'engagement': 15,
    'total': 100
}

# Closing phrases
CLOSING_PHRASES = [r'\bthank\s+you\b', r'\bthanks\b', r'\bthank\s+you\s+for\s+listening\b']
