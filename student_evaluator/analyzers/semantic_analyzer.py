"""
Enhanced Semantic Analyzer using Sentence Transformers
Adds NLP-based semantic similarity scoring to the evaluation.
"""

from typing import Dict, Any
from sentence_transformers import SentenceTransformer, util
import numpy as np


class SemanticAnalyzer:
    """
    Analyzes semantic similarity between transcript and rubric descriptions.
    Uses sentence-transformers for embedding-based comparison.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the semantic analyzer with a sentence transformer model.
        
        Args:
            model_name: Name of the sentence-transformers model to use
        """
        print(f"Loading semantic model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        print("Semantic model loaded successfully!")
        
        # Define ideal descriptions for each criterion
        self.criterion_descriptions = {
            'content': [
                "A complete self-introduction with name, age, class, school, and family details",
                "Includes personal hobbies, interests, and activities the student enjoys",
                "Mentions unique facts, goals, or achievements about themselves"
            ],
            'speech_rate': [
                "Speaking at a comfortable, natural pace that is easy to follow",
                "Neither too fast nor too slow, maintaining good rhythm"
            ],
            'grammar': [
                "Grammatically correct sentences with proper structure",
                "Rich vocabulary with varied word choices and expressions"
            ],
            'clarity': [
                "Clear and articulate speech without filler words",
                "Confident delivery with minimal hesitation"
            ],
            'engagement': [
                "Enthusiastic and positive tone showing confidence",
                "Engaging delivery that captures attention",
                "Expresses excitement and genuine interest"
            ]
        }
    
    def analyze_content_semantics(self, transcript: str) -> Dict[str, Any]:
        """
        Analyze how well the transcript semantically matches ideal content.
        
        Args:
            transcript: Student's introduction transcript
            
        Returns:
            Dictionary with semantic similarity scores
        """
        transcript_embedding = self.model.encode(transcript, convert_to_tensor=True)
        
        scores = {}
        for criterion, descriptions in self.criterion_descriptions.items():
            # Get embeddings for all ideal descriptions
            desc_embeddings = self.model.encode(descriptions, convert_to_tensor=True)
            
            # Calculate cosine similarity
            similarities = util.cos_sim(transcript_embedding, desc_embeddings)
            
            # Take maximum similarity across all descriptions
            max_similarity = float(similarities.max())
            
            # Average similarity across all descriptions
            avg_similarity = float(similarities.mean())
            
            scores[criterion] = {
                'max_similarity': round(max_similarity, 3),
                'avg_similarity': round(avg_similarity, 3),
                'all_similarities': [round(float(s), 3) for s in similarities[0]]
            }
        
        return scores
    
    def analyze_keyword_semantics(self, transcript: str, keywords: list) -> Dict[str, Any]:
        """
        Analyze semantic similarity between transcript and specific keywords.
        
        Args:
            transcript: Student's introduction transcript
            keywords: List of keywords to check
            
        Returns:
            Dictionary with keyword match scores
        """
        if not keywords:
            return {'semantic_match_score': 0.0, 'details': []}
        
        transcript_embedding = self.model.encode(transcript, convert_to_tensor=True)
        keyword_embeddings = self.model.encode(keywords, convert_to_tensor=True)
        
        # Calculate similarities
        similarities = util.cos_sim(transcript_embedding, keyword_embeddings)
        
        details = []
        for i, keyword in enumerate(keywords):
            details.append({
                'keyword': keyword,
                'similarity': round(float(similarities[0][i]), 3)
            })
        
        # Average similarity as overall score
        avg_similarity = float(similarities.mean())
        
        return {
            'semantic_match_score': round(avg_similarity, 3),
            'details': sorted(details, key=lambda x: x['similarity'], reverse=True)
        }
    
    def enhance_content_score(
        self, 
        rule_based_score: int, 
        transcript: str, 
        max_score: int = 40
    ) -> Dict[str, Any]:
        """
        Enhance content score by combining rule-based and semantic approaches.
        
        Args:
            rule_based_score: Score from rule-based keyword matching
            transcript: The transcript text
            max_score: Maximum possible score
            
        Returns:
            Enhanced score with semantic analysis
        """
        semantic_results = self.analyze_content_semantics(transcript)
        
        # Get content semantic similarity
        content_sim = semantic_results['content']['avg_similarity']
        
        # Combine rule-based (70%) and semantic (30%)
        rule_based_normalized = rule_based_score / max_score
        combined_normalized = (rule_based_normalized * 0.7) + (content_sim * 0.3)
        
        enhanced_score = int(combined_normalized * max_score)
        
        return {
            'enhanced_score': enhanced_score,
            'original_score': rule_based_score,
            'semantic_contribution': round((content_sim * 0.3) * max_score, 1),
            'semantic_similarity': content_sim,
            'method': 'Rule-based (70%) + Semantic (30%)'
        }
    
    def enhance_engagement_score(
        self,
        sentiment_score: int,
        transcript: str,
        max_score: int = 15
    ) -> Dict[str, Any]:
        """
        Enhance engagement score with semantic similarity to positive expressions.
        
        Args:
            sentiment_score: Score from VADER sentiment
            transcript: The transcript text
            max_score: Maximum possible score
            
        Returns:
            Enhanced engagement score
        """
        semantic_results = self.analyze_content_semantics(transcript)
        engagement_sim = semantic_results['engagement']['avg_similarity']
        
        # Combine sentiment (60%) and semantic (40%)
        sentiment_normalized = sentiment_score / max_score
        combined_normalized = (sentiment_normalized * 0.6) + (engagement_sim * 0.4)
        
        enhanced_score = int(combined_normalized * max_score)
        
        return {
            'enhanced_score': enhanced_score,
            'original_score': sentiment_score,
            'semantic_contribution': round((engagement_sim * 0.4) * max_score, 1),
            'semantic_similarity': engagement_sim,
            'method': 'Sentiment (60%) + Semantic (40%)'
        }
