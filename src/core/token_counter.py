# proj/src/core/token_counter.py

import tiktoken

class TokenCounter:
    """
    Utility for counting tokens across different models
    """
    def __init__(self, encoding_name: str = 'cl100k_base'):
        """
        Initialize token counter with a specific encoding
        
        Args:
            encoding_name (str): Name of the encoding to use
        """
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in a given text
        
        Args:
            text (str): Input text to count tokens
        
        Returns:
            int: Number of tokens in the text
        """
        return len(self.encoding.encode(text))
    
    def estimate_max_tokens(self, max_input_tokens: int = 8192) -> int:
        """
        Estimate maximum tokens for processing
        
        Args:
            max_input_tokens (int): Maximum tokens for the model
        
        Returns:
            int: Recommended max tokens for processing
        """
        return max_input_tokens // 2  # Reserve tokens for response