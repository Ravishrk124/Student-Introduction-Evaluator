"""Grammar and Language Analyzer - 20 points total."""

from typing import Dict, Any
import language_tool_python
from ..config import MAX_SCORES
from ..utils.keywords import tokenize_words, calculate_ttr
from ..utils.scorer import score_grammar, score_vocabulary


class GrammarAnalyzer:
    """Analyzes grammar errors and vocabulary richness."""
    
    def __init__(self):
        self.max_grammar = MAX_SCORES['grammar']
        self.max_vocabulary = MAX_SCORES['vocabulary']
        self.max_total = MAX_SCORES['grammar_total']
        
        # Initialize LanguageTool (lazy loading)
        self.tool = None
    
    def _init_tool(self):
        """Initialize LanguageTool if not already initialized."""
        if self.tool is None:
            try:
                self.tool = language_tool_python.LanguageTool('en-US')
            except Exception as e:
                print(f"Warning: Could not initialize LanguageTool: {e}")
                self.tool = None
    
    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Analyze grammar and vocabulary.
        
        Args:
            text: Transcript text
            
        Returns:
            Dictionary with grammar and vocabulary scores
        """
        grammar_result = self._analyze_grammar(text)
        vocabulary_result = self._analyze_vocabulary(text)
        
        total_score = grammar_result['score'] + vocabulary_result['score']
        
        return {
            'grammar': grammar_result,
            'vocabulary': vocabulary_result,
            'total_score': total_score,
            'max_score': self.max_total,
            'percentage': round((total_score / self.max_total) * 100, 1)
        }
    
    def _analyze_grammar(self, text: str) -> Dict[str, Any]:
        """
        Analyze grammar errors (10 points).
        Uses LanguageTool to detect errors.
        """
        self._init_tool()
        
        if self.tool is None:
            # Fallback: assume perfect grammar if tool not available
            return {
                'score': self.max_grammar,
                'max_score': self.max_grammar,
                'error_count': 0,
                'errors_per_100': 0,
                'errors': [],
                'note': 'LanguageTool not available, assuming no errors'
            }
        
        try:
            # Check grammar
            matches = self.tool.check(text)
            error_count = len(matches)
            
            # Calculate errors per 100 words
            words = tokenize_words(text)
            word_count = len(words)
            
            if word_count == 0:
                errors_per_100 = 0
            else:
                errors_per_100 = (error_count / word_count) * 100
            
            # Calculate score
            score = score_grammar(errors_per_100)
            
            # Extract error details (limited to first 5)
            error_details = []
            for match in matches[:5]:
                error_details.append({
                    'message': match.message,
                    'context': match.context,
                    'offset': match.offset
                })
            
            return {
                'score': score,
                'max_score': self.max_grammar,
                'error_count': error_count,
                'errors_per_100': round(errors_per_100, 2),
                'word_count': word_count,
                'errors': error_details
            }
        
        except Exception as e:
            # Fallback on error
            return {
                'score': self.max_grammar,
                'max_score': self.max_grammar,
                'error_count': 0,
                'errors_per_100': 0,
                'errors': [],
                'error': str(e),
                'note': 'Error in grammar check, assuming no errors'
            }
    
    def _analyze_vocabulary(self, text: str) -> Dict[str, Any]:
        """
        Analyze vocabulary richness using TTR (10 points).
        TTR = unique words / total words
        """
        ttr = calculate_ttr(text)
        score = score_vocabulary(ttr)
        
        words = tokenize_words(text)
        unique_words = set(words)
        
        return {
            'score': score,
            'max_score': self.max_vocabulary,
            'ttr': ttr,
            'total_words': len(words),
            'unique_words': len(unique_words)
        }
    
    def __del__(self):
        """Cleanup LanguageTool on deletion."""
        if self.tool is not None:
            try:
                self.tool.close()
            except:
                pass
