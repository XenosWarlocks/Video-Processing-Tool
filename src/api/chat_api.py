# proj/src/api/chat_api.py
from typing import Optional, Dict, List, Union
from src.core.base_processor import ConfigManager
from src.ai_integration.gemini_processor import GeminiProcessor

class Message:
    """
    Represents a chat message with role and content
    """
    def __init__(self, content: str, role: str = "user", metadata: Dict = None):
        self.content = content
        self.role = role
        self.metadata = metadata or {}

class ChatAPI:
    def __init__(self):
        # Initialize the config manager and processor
        config_manager = ConfigManager()
        self.processor = GeminiProcessor(config_manager)
        self.chat_history: List[Message] = []
        
    def send_message(
        self, 
        message: str, 
        is_system: bool = False,
        video_context: Optional[Dict] = None,
        metadata: Optional[Dict] = None
    ) -> Union[str, Dict]:
        """
        Send a message to the AI and get response
        
        Args:
            message (str): User's or system message
            is_system (bool): Whether this is a system message
            video_context (Dict, optional): Video analysis context if available
            metadata (Dict, optional): Additional message metadata
            
        Returns:
            Union[str, Dict]: AI's response or error message
        """
        try:
            # Determine message role
            role = "system" if is_system else "user"
            
            # Create message object
            current_message = Message(
                content=message,
                role=role,
                metadata=metadata
            )
            
            # Add message to history
            self.chat_history.append(current_message)
            
            # Process the message through the AI processor
            response = self.processor.process([{
                'text': message,
                'role': role,
                'video_context': video_context,
                'metadata': metadata
            }])
            
            # Extract response text from processed data
            response_text = self._extract_response_text(response)
            
            # Create and store assistant's response
            assistant_message = Message(
                content=response_text,
                role="assistant",
                metadata={'processed_data': response}
            )
            self.chat_history.append(assistant_message)
            
            return response_text
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            # Store error in history
            error_msg = Message(
                content=error_message,
                role="system",
                metadata={'error': str(e)}
            )
            self.chat_history.append(error_msg)
            return {'error': error_message}
    
    def _extract_response_text(self, processed_data: List[Dict]) -> str:
        """
        Extract readable response text from processed AI data
        
        Args:
            processed_data (List[Dict]): Processed AI response data
            
        Returns:
            str: Extracted response text
        """
        try:
            # Extract insights and summaries from processed data
            summaries = []
            for item in processed_data:
                for insight in item.get('insights', []):
                    if 'summary' in insight:
                        summaries.append(insight['summary'])
            
            # Combine summaries or return default message
            if summaries:
                return ' '.join(summaries)
            return "I processed your message but couldn't generate a proper response."
            
        except Exception as e:
            return f"Error extracting response: {str(e)}"
    
    def get_chat_history(self, include_metadata: bool = False) -> List[Dict]:
        """
        Get the complete chat history
        
        Args:
            include_metadata (bool): Whether to include message metadata
            
        Returns:
            List[Dict]: Chat history
        """
        if include_metadata:
            return [
                {
                    'role': msg.role,
                    'content': msg.content,
                    'metadata': msg.metadata
                }
                for msg in self.chat_history
            ]
        
        return [
            {
                'role': msg.role,
                'content': msg.content
            }
            for msg in self.chat_history
        ]
    
    def clear_history(self):
        """Clear the chat history"""
        self.chat_history = []
        
    def get_last_message(self) -> Optional[Message]:
        """
        Get the last message in the chat history
        
        Returns:
            Optional[Message]: Last message or None if history is empty
        """
        return self.chat_history[-1] if self.chat_history else None
