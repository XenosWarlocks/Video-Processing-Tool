import os
import re
from typing import List, Dict, Any, Optional

import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential

from src.core.base_processor import BaseProcessor, ConfigManager
from src.core.token_counter import TokenCounter

class TextInsight(BaseModel):
    """
    Structured model for text insights
    """
    sentiment: str = Field(description="Overall sentiment of the text")
    keywords: List[str] = Field(description="Top 5 important keywords")
    summary: str = Field(description="Concise summary of the text")
    complexity: str = Field(description="Text complexity level")

class GeminiProcessor(BaseProcessor):
    """
    Enhanced Gemini AI processor with advanced text processing capabilities
    """
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        
        # Configure Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        
        # Initialize Gemini model and token counter
        self.model = genai.GenerativeModel(
            self.config.get_config('ai', 'model_name', 'gemini-pro')
        )
        self.token_counter = TokenCounter()

    def _chunk_text(self, text: str, max_tokens: int = 2000) -> List[str]:
        """
        Chunk large text into manageable segments
        
        Args:
            text (str): Input text to chunk
            max_tokens (int): Maximum tokens per chunk
        
        Returns:
            List[str]: List of text chunks
        """
        # Basic chunking strategy
        words = text.split()
        chunks = []
        current_chunk = []
        current_token_count = 0

        for word in words:
            word_tokens = self.token_counter.count_tokens(word)

            if current_token_count + word_tokens > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_token_count = 0

            current_chunk.append(word)
            current_token_count += word_tokens

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _process_chunk(self, chunk: str) -> TextInsight:
        """
        Process a single text chunk with advanced insights
        
        Args:
            chunk (str): Text chunk to process
        
        Returns:
            TextInsight: Structured insights for the chunk
        """
        # Create Pydantic output parser
        parser = PydanticOutputParser(pydantic_object=TextInsight)
        
        # Create a comprehensive prompt template
        prompt = PromptTemplate(
            template="""You are an advanced and highly capable AI specializing in comprehensive text analysis. 
            Your goal is to analyze the following text and provide actionable and thorough insights based on the outlined instructions. 

            **Text Analysis Requirements:**
            1. **Sentiment Analysis:** 
                - Determine the overall sentiment (e.g., positive, negative, neutral).
                - Provide a detailed explanation of the sentiment by identifying specific phrases or words contributing to the tone.
                - Assign a sentiment weight (on a scale of -1 to +1) to indicate sentiment intensity.

            2. **Keyword Extraction:** 
                - Identify the most important keywords and phrases in the text. 
                - Prioritize keywords based on frequency, relevance, and contextual importance. 
                - Highlight relationships between key phrases, if applicable.

            3. **Concise Summary:** 
                - Provide a brief, accurate summary of the text (no more than 6-9 sentences). 
                - Ensure the summary captures the primary ideas and intent of the text.

            4. **Text Complexity Assessment:** 
                - Evaluate the linguistic complexity of the text based on factors such as vocabulary, sentence structure, and readability. 
                - Rate the text's complexity on a scale from 1 (simple) to 5 (highly complex). 
                - Suggest potential audiences who would find this text accessible or challenging.

            5. **Formatting & Structured Output:** 
                - Present the analysis in a well-organized JSON format, adhering to the format instructions below.
                - Ensure output consistency and avoid redundancies in your response.

            **Text to Analyze:**
            {text}

            **Format Instructions:**
            {format_instructions}
            """,
            input_variables=["text"],
            partial_variables={
                "format_instructions": parser.get_format_instructions()
            }
        )

        # Prepare the prompt
        formatted_prompt = prompt.format_prompt(text=chunk)

        # Generate response
        try:
            response = self.model.generate_content(formatted_prompt.to_string())
            return parser.parse(response.text)
        except Exception as e:
            self.log_error(f"Chunk processing error: {e}")
            # Return a default insight if processing fails
            return TextInsight(
                sentiment="Unknown",
                keywords=[],
                summary="Error processing chunk",
                complexity="N/A"
            )
    
    def process(self, text_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Advanced text processing with chunking and multi-step analysis
        
        Args:
            text_data (List[Dict[str, str]]): List of text entries
        
        Returns:
            List[Dict[str, Any]]: Enhanced text data with comprehensive insights
        """
        enhanced_data = []
        for entry in text_data:
            try:
                # Chunk the text
                text_chunks = self._chunk_text(entry['text'])

                # Process each chunk
                chunk_insights = [self._process_chunk(chunk) for chunk in text_chunks]

                # Aggregate insights
                enhanced_entry = {
                    'original_text': entry['text'],
                    'frame_path': entry.get('frame_path'),
                    'total_tokens': self.token_counter.count_tokens(entry['text']),
                    'insights': [
                        {
                            'sentiment': insight.sentiment,
                            'keywords': insight.keywords,
                            'summary': insight.summary,
                            'complexity': insight.complexity
                        } for insight in chunk_insights
                    ]
                }
                enhanced_data.append(enhanced_entry)
            
            except Exception as e:
                self.log_error(f"Error processing entry: {e}")
                enhanced_data.append({
                    'original_text': entry['text'],
                    'frame_path': entry.get('frame_path'),
                    'total_tokens': self.token_counter.count_tokens(entry['text']),
                    'insights': [],
                    'error': str(e)
                })
        
        return enhanced_data
    
    def _normalize_text(self, text: str) -> str:
        """
        Normalize text by removing extra whitespaces and cleaning
        
        Args:
            text (str): Input text
        
        Returns:
            str: Cleaned and normalized text
        """
        # Remove extra whitespaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters if needed
        text = re.sub(r'[^\w\s.,!?]', '', text)
        
        return text