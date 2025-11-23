"""
Student Introduction Evaluation Tool - Main Entry Point

This tool evaluates student introduction transcripts based on a comprehensive rubric.
"""

import json
import argparse
from typing import Dict, Any
from pathlib import Path

from .analyzers import (
    ContentAnalyzer,
    SpeechRateAnalyzer,
    GrammarAnalyzer,
    ClarityAnalyzer,
    EngagementAnalyzer
)
# Semantic analyzer is optional - requires sentence-transformers
try:
    from .analyzers.semantic_analyzer import SemanticAnalyzer
    SEMANTIC_AVAILABLE = True
except ImportError:
    SEMANTIC_AVAILABLE = False
    
from .utils.keywords import count_sentences, tokenize_words


class StudentEvaluator:
    """Main evaluator that orchestrates all analysis modules."""
    
    def __init__(self, use_semantic: bool = True):
        """
        Initialize evaluator with all analyzer modules.
        
        Args:
            use_semantic: Whether to use semantic analysis (requires sentence-transformers)
        """
        self.content_analyzer = ContentAnalyzer()
        self.speech_rate_analyzer = SpeechRateAnalyzer()
        self.grammar_analyzer = GrammarAnalyzer()
        self.clarity_analyzer = ClarityAnalyzer()
        self.engagement_analyzer = EngagementAnalyzer()
        
        # Initialize semantic analyzer if available and requested
        self.use_semantic = use_semantic and SEMANTIC_AVAILABLE
        self.semantic_analyzer = None
        
        if self.use_semantic:
            try:
                self.semantic_analyzer = SemanticAnalyzer()
                print("✅ Semantic analysis enabled (NLP-based)")
            except Exception as e:
                print(f"⚠️ Semantic analysis unavailable: {e}")
                print("📝 Falling back to rule-based only")
                self.use_semantic = False
    
    def evaluate(self, transcript: str, duration_seconds: int) -> Dict[str, Any]:
        """
        Evaluate a student introduction transcript.
        
        Args:
            transcript: The transcript text
            duration_seconds: Duration of the speech in seconds
            
        Returns:
            Complete evaluation results with all scores
        """
        # Metadata
        words = tokenize_words(transcript)
        word_count = len(words)
        sentence_count = count_sentences(transcript)
        
        # Run all analyzers
        print("Analyzing content and structure...")
        content_results = self.content_analyzer.analyze(transcript)
        
        # Enhance with semantic analysis if available
        if self.use_semantic and self.semantic_analyzer:
            print("Applying semantic analysis to content...")
            semantic_enhancement = self.semantic_analyzer.enhance_content_score(
                content_results['total_score'],
                transcript,
                content_results['max_score']
            )
            content_results['semantic_enhancement'] = semantic_enhancement
            # Use enhanced score
            original_content_score = content_results['total_score']
            content_results['total_score'] = semantic_enhancement['enhanced_score']
            content_results['scoring_method'] = semantic_enhancement['method']
        else:
            content_results['scoring_method'] = 'Rule-based only'
        
        print("Analyzing speech rate...")
        speech_rate_results = self.speech_rate_analyzer.analyze(transcript, duration_seconds)
        
        print("Analyzing grammar and vocabulary...")
        grammar_results = self.grammar_analyzer.analyze(transcript)
        
        print("Analyzing clarity...")
        clarity_results = self.clarity_analyzer.analyze(transcript)
        
        print("Analyzing engagement...")
        engagement_results = self.engagement_analyzer.analyze(transcript)
        
        # Enhance engagement with semantic analysis if available
        if self.use_semantic and self.semantic_analyzer:
            print("Applying semantic analysis to engagement...")
            engagement_enhancement = self.semantic_analyzer.enhance_engagement_score(
                engagement_results['score'],
                transcript,
                engagement_results['max_score']
            )
            engagement_results['semantic_enhancement'] = engagement_enhancement
            engagement_results['score'] = engagement_enhancement['enhanced_score']
            engagement_results['scoring_method'] = engagement_enhancement['method']
        else:
            engagement_results['scoring_method'] = 'Sentiment-based only'
        
        # Calculate total score
        total_score = (
            content_results['total_score'] +
            speech_rate_results['score'] +
            grammar_results['total_score'] +
            clarity_results['score'] +
            engagement_results['score']
        )
        
        max_score = 100
        percentage = round((total_score / max_score) * 100, 1)
        
        # Determine grade
        grade = self._calculate_grade(percentage)
        
        # Compile results
        results = {
            'transcript': transcript,
            'metadata': {
                'word_count': word_count,
                'sentence_count': sentence_count,
                'duration_seconds': duration_seconds,
                'wpm': speech_rate_results['wpm']
            },
            'scores': {
                'content_and_structure': {
                    'salutation_score': content_results['salutation']['score'],
                    'keywords_score': content_results['keywords']['score'],
                    'flow_score': content_results['flow']['score'],
                    'total': content_results['total_score'],
                    'max': content_results['max_score'],
                    'percentage': content_results['percentage'],
                    'details': content_results
                },
                'speech_rate': {
                    'wpm': speech_rate_results['wpm'],
                    'label': speech_rate_results['label'],
                    'score': speech_rate_results['score'],
                    'max': speech_rate_results['max_score']
                },
                'language_and_grammar': {
                    'grammar_score': grammar_results['grammar']['score'],
                    'vocabulary_score': grammar_results['vocabulary']['score'],
                    'total': grammar_results['total_score'],
                    'max': grammar_results['max_score'],
                    'percentage': grammar_results['percentage'],
                    'details': grammar_results
                },
                'clarity': {
                    'filler_count': clarity_results['filler_count'],
                    'filler_rate': clarity_results['filler_rate'],
                    'score': clarity_results['score'],
                    'max': clarity_results['max_score'],
                    'details': clarity_results
                },
                'engagement': {
                    'sentiment_compound_normalized': engagement_results.get('compound_normalized', 0),
                    'sentiment_positive': engagement_results['sentiment_positive'],
                    'interpretation': engagement_results['interpretation'],
                    'score': engagement_results['score'],
                    'max': engagement_results['max_score'],
                    'details': engagement_results
                }
            },
            'final_score': total_score,
            'max_score': max_score,
            'percentage': percentage,
            'grade': grade
        }
        
        return results
    
    def _calculate_grade(self, percentage: float) -> str:
        """Calculate letter grade from percentage."""
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'B+'
        elif percentage >= 75:
            return 'B'
        elif percentage >= 70:
            return 'C+'
        elif percentage >= 65:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    def print_summary(self, results: Dict[str, Any]):
        """Print a human-readable summary of results."""
        print("\n" + "="*60)
        print("STUDENT INTRODUCTION EVALUATION REPORT")
        print("="*60)
        
        print(f"\n📊 METADATA")
        print(f"  Word Count: {results['metadata']['word_count']}")
        print(f"  Sentence Count: {results['metadata']['sentence_count']}")
        print(f"  Duration: {results['metadata']['duration_seconds']} seconds")
        print(f"  Speech Rate: {results['metadata']['wpm']} WPM")
        
        print(f"\n📝 CONTENT & STRUCTURE (40 points)")
        cs = results['scores']['content_and_structure']
        print(f"  Salutation: {cs['salutation_score']}/5")
        print(f"  Keywords: {cs['keywords_score']}/30")
        print(f"  Flow: {cs['flow_score']}/5")
        print(f"  Total: {cs['total']}/{cs['max']} ({cs['percentage']}%)")
        
        print(f"\n⚡ SPEECH RATE (10 points)")
        sr = results['scores']['speech_rate']
        print(f"  WPM: {sr['wpm']} ({sr['label']})")
        print(f"  Score: {sr['score']}/{sr['max']}")
        
        print(f"\n📖 LANGUAGE & GRAMMAR (20 points)")
        lg = results['scores']['language_and_grammar']
        print(f"  Grammar: {lg['grammar_score']}/10")
        print(f"  Vocabulary: {lg['vocabulary_score']}/10")
        print(f"  Total: {lg['total']}/{lg['max']} ({lg['percentage']}%)")
        
        print(f"\n✨ CLARITY (15 points)")
        cl = results['scores']['clarity']
        print(f"  Filler Words: {cl['filler_count']} ({cl['filler_rate']}%)")
        print(f"  Score: {cl['score']}/{cl['max']}")
        
        print(f"\n💫 ENGAGEMENT (15 points)")
        eg = results['scores']['engagement']
        print(f"  Sentiment: {eg['interpretation']}")
        print(f"  Sentiment Score: {eg.get('sentiment_compound_normalized', eg.get('sentiment_positive', 0))}")
        print(f"  Score: {eg['score']}/{eg['max']}")
        
        print(f"\n{'='*60}")
        print(f"🎯 FINAL SCORE: {results['final_score']}/{results['max_score']} ({results['percentage']}%)")
        print(f"📊 GRADE: {results['grade']}")
        print("="*60 + "\n")


def main():
    """Command-line interface."""
    parser = argparse.ArgumentParser(
        description="Evaluate student introduction transcripts"
    )
    parser.add_argument(
        '--transcript',
        type=str,
        help='Path to transcript text file or direct text'
    )
    parser.add_argument(
        '--duration',
        type=int,
        required=True,
        help='Duration of speech in seconds'
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Output JSON file path (optional)'
    )
    
    args = parser.parse_args()
    
    # Load transcript
    transcript_path = Path(args.transcript)
    if transcript_path.exists() and transcript_path.is_file():
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript = f.read()
        print(f"Loaded transcript from: {transcript_path}")
    else:
        transcript = args.transcript
        print("Using provided transcript text")
    
    # Create evaluator and run analysis
    evaluator = StudentEvaluator()
    results = evaluator.evaluate(transcript, args.duration)
    
    # Print summary
    evaluator.print_summary(results)
    
    # Save to file if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"✅ Results saved to: {output_path}")
    
    return results


if __name__ == '__main__':
    main()
