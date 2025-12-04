"""
Claude AI Integration using Anthropic Code Agent SDK
Agent-based implementation with autonomous tool use
"""
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from app.core.config import settings


class ClaudeAI:
    """Claude AI client with Code Agent capabilities"""
    
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.model = settings.CLAUDE_MODEL
        self.client = Anthropic(api_key=self.api_key)
    
    def get_api_key(self) -> str:
        """Get Claude API key"""
        return self.api_key
    
    def get_model(self) -> str:
        """Get Claude model name"""
        return self.model
    
    def run_agent(
        self,
        user_message: str,
        tools: List[Dict[str, Any]],
        tool_executor: callable,
        system: Optional[str] = None,
        max_iterations: int = 10,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        timeout: int = 60
    ) -> str:
        """
        Run an agent loop where Claude autonomously uses tools
        
        Args:
            user_message: Initial user query
            tools: List of tool definitions available to the agent
            tool_executor: Function to execute tools (tool_name, tool_input) -> result
            system: Optional system message
            max_iterations: Maximum number of agent iterations (default: 10)
            temperature: Temperature for generation (default: 0.7)
            max_tokens: Maximum tokens per response (default: 4096)
        
        Returns:
            Final agent response as text
        """
        messages = [{"role": "user", "content": user_message}]
        iteration = 0
        
        while iteration < max_iterations:
            try:
                # Get agent response
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                    tools=tools if tools else None,
                    system=system
                )
                
                # Add assistant response to conversation
                assistant_message = {"role": "assistant", "content": []}
                tool_results = []
                
                for content_block in response.content:
                    if content_block.type == "text":
                        assistant_message["content"].append({
                            "type": "text",
                            "text": content_block.text
                        })
                    elif content_block.type == "tool_use":
                        assistant_message["content"].append({
                            "type": "tool_use",
                            "id": content_block.id,
                            "name": content_block.name,
                            "input": content_block.input
                        })
                        
                        # Execute tool
                        try:
                            tool_result = tool_executor(content_block.name, content_block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": content_block.id,
                                "content": tool_result
                            })
                        except Exception as e:
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": content_block.id,
                                "content": f"Error executing tool: {str(e)}"
                            })
                
                messages.append(assistant_message)
                
                # If no tools were used, agent is done
                if not tool_results:
                    # Extract final text response
                    final_text = ""
                    for content in assistant_message["content"]:
                        if content.get("type") == "text":
                            final_text += content.get("text", "")
                    return final_text if final_text else "Agent completed without response."
                
                # Add tool results to conversation
                messages.append({
                    "role": "user",
                    "content": tool_results
                })
                
                iteration += 1
                
            except Exception as e:
                raise Exception(f"Agent iteration failed: {str(e)}")
        
        # If max iterations reached, extract any text from last response
        if messages and len(messages) > 0:
            last_message = messages[-1]
            if isinstance(last_message.get("content"), list):
                for content in last_message["content"]:
                    if isinstance(content, dict) and content.get("type") == "text":
                        return content.get("text", "Agent reached max iterations.")
        
        return "Agent reached maximum iterations without completing."
