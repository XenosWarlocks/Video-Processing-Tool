# proj/src/ai_integration/text_enrichment.py
import os
import re
from typing import List, Dict, Any, Optional
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from textstat import flesch_reading_ease, flesch_kincaid_grade

class TextEnrichmentProcessor:
    """
    Advanced text enrichment processor with multiple analysis techniques
    """
    def __init__(self):
        # Download necessary NLTK resources
        import nltk
        """
        Initialize the text enrichment processor with required NLTK downloads
        """
        # Create data directory if it doesn't exist
        nltk_data_dir = os.path.join(os.path.expanduser('~'), 'nltk_data')
        if not os.path.exists(nltk_data_dir):
            os.makedirs(nltk_data_dir)
        
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
    
    def preprocess_text(self, text: str, remove_digits: bool = True, remove_punctuation: bool = True) -> str:
        
        text = text.lower()
        if remove_digits:
            text = re.sub(r'\d+', '', text)
        if remove_punctuation:
            text = re.sub(r'[^\w\s]', '', text)
        return text
    
    def extract_key_phrases(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key phrases using TF-IDF
        
        Args:
            text (str): Input text
            top_n (int): Number of top phrases to return
        
        Returns:
            List[str]: Top key phrases
        """
        preprocessed_text = self.preprocess_text(text)
        
        # TF-IDF Vectorization with stop words
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words=list(self.stop_words))
        tfidf_matrix = vectorizer.fit_transform([preprocessed_text])
        
        # Get feature names and scores
        feature_names = vectorizer.get_feature_names_out()
        tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
        
        # Sort phrases by TF-IDF score
        sorted_phrases = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)
        
        return [phrase for phrase, score in sorted_phrases[:top_n]]
    
    def analyze_readability(self, text: str) -> Dict[str, float | str]:
        """
        Analyze text readability using multiple metrics
        
        Args:
            text (str): Input text
        
        Returns:
            Dict[str, Any]: Readability analysis results
        """
        score = flesch_reading_ease(text)
        return {
            'flesch_reading_ease': score,
            'flesch_kincaid_grade': flesch_kincaid_grade(text),
            'complexity_level': self._get_complexity_level(score)
        }
    
    def _get_complexity_level(self, score: float) -> str:
        """
        Determine text complexity level based on Flesch Reading Ease score
        
        Args:
            score (float): Flesch Reading Ease score
        
        Returns:
            str: Complexity level description
        """
        if score < 30:
            return 'Very Difficult'
        elif score < 50:
            return 'Difficult'
        elif score < 60:
            return 'Fairly Difficult'
        elif score < 70:
            return 'Standard'
        else:
            return 'Easy'
    
    def enrich_text(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive text enrichment
        
        Args:
            text (str): Input text
        
        Returns:
            Dict[str, Any]: Enriched text analysis
        """
        return {
            'original_text': text,
            'key_phrases': List[str],
            'readability': Dict[str, float | str],
            'word_count': int,
            'unique_words': int
        }