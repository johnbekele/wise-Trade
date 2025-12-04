from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from app.core.config import settings


class ClaudeAI:
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.model = settings.CLAUDE_MODEL
        self.client = Anthropic(api_key=self.api_key)
    
    def get_api_key(self) -> str:
        return self.api_key
    
    def get_model(self) -> str:
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
        # Run agent loop with autonomous tool use
        messages = [{"role": "user", "content": user_message}]
        iteration = 0
        
        while iteration < max_iterations:
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    messages=messages,
                    tools=tools if tools else None,
                    system=system
                )
                
                assistant_message = {"role": "assistant", "content": []}
                tool_results = []
                
                for content_block in response.content:
                    if content_block.type == "text":
                        assistant_message["content"].append({"type": "text", "text": content_block.text})
                    elif content_block.type == "tool_use":
                        assistant_message["content"].append({
                            "type": "tool_use",
                            "id": content_block.id,
                            "name": content_block.name,
                            "input": content_block.input
                        })
                        try:
                            tool_result = tool_executor(content_block.name, content_block.input)
                            tool_results.append({"type": "tool_result", "tool_use_id": content_block.id, "content": tool_result})
                        except Exception as e:
                            tool_results.append({"type": "tool_result", "tool_use_id": content_block.id, "content": f"Error executing tool: {str(e)}"})
                
                messages.append(assistant_message)
                
                if not tool_results:
                    final_text = ""
                    for content in assistant_message["content"]:
                        if content.get("type") == "text":
                            final_text += content.get("text", "")
                    return final_text if final_text else "Agent completed without response."
                
                messages.append({"role": "user", "content": tool_results})
                iteration += 1
                
            except Exception as e:
                raise Exception(f"Agent iteration failed: {str(e)}")
        
        if messages and len(messages) > 0:
            last_message = messages[-1]
            if isinstance(last_message.get("content"), list):
                for content in last_message["content"]:
                    if isinstance(content, dict) and content.get("type") == "text":
                        return content.get("text", "Agent reached max iterations.")
        
        return "Agent reached maximum iterations without completing."
