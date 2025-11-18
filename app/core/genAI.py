from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

class GenAI:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL
    
    def get_api_key(self):
        return self.api_key
    
    def get_model(self):
        return self.model
        
    def get_llm(self):
        """Get a basic LLM instance without tools"""
        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            temperature=0.7,
        )
    
    def generate_content_direct(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Generate content using Google AI SDK directly, bypassing LangChain
        to avoid max_retries compatibility issues.
        
        Args:
            prompt: The prompt to send to the model
            temperature: Temperature for generation (default: 0.7)
        
        Returns:
            Generated text content
        """
        try:
            import google.genai as genai
        except ImportError:
            raise ImportError(
                "google-genai package not found. Install it with: pip install google-genai"
            )
        
        # Create client with API key
        client = genai.Client(api_key=self.api_key)
        
        # Generate content using the client
        try:
            response = client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={"temperature": temperature}
            )
        except Exception as gen_error:
            raise Exception(f"Failed to generate content with model '{self.model}': {str(gen_error)}")
        
        # Extract text from response
        if hasattr(response, 'text') and response.text:
            return response.text
        elif hasattr(response, 'candidates') and response.candidates:
            if hasattr(response.candidates[0], 'content'):
                content = response.candidates[0].content
                if hasattr(content, 'parts') and content.parts:
                    return content.parts[0].text if hasattr(content.parts[0], 'text') else str(content.parts[0])
                elif hasattr(content, 'text'):
                    return content.text
        
        # Fallback to string representation
        return str(response)
