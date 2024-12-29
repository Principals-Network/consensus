from typing import Dict, List, Any
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from src.utils.logging import setup_logger

class ClaudeAI:
    def __init__(self, config: Dict[str, Any] = None):
        if config is None:
            from src.config.config_loader import ConfigLoader
            config = ConfigLoader().get_ai_config()
        
        self.config = config
        self.model = "claude-3-5-sonnet-20241022"  # Hardcoded correct model
        self.context_window = 200000
        
        # Initialize async client
        self.client = anthropic.AsyncAnthropic(
            api_key=config['anthropic_api_key']
        )
        
        self.logger = setup_logger(f"{__name__}.ClaudeAI")
        self.logger.info("Initializing Claude AI integration...")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def generate_response(self, 
                              prompt: str, 
                              role: str, 
                              context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI response using Claude"""
        try:
            # Create system message
            system_prompt = self._construct_system_prompt(role, context)
            
            # Create the message
            message = await self.client.messages.create(
                model=self.model,
                max_tokens=self.config.get('max_tokens', 2000),
                temperature=self.config.get('temperature', 0.5),
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return {
                'content': message.content[0].text,
                'role': "assistant",
                'model': self.model,
                'stop_reason': message.stop_reason if hasattr(message, 'stop_reason') else None,
                'usage': message.usage if hasattr(message, 'usage') else None
            }
            
        except Exception as e:
            self.logger.error(f"Error calling Anthropic API: {str(e)}")
            raise  # Re-raise to trigger retry
    
    def _construct_system_prompt(self, role: str, context: Dict[str, Any]) -> str:
        """Construct role-specific system prompt"""
        base_prompt = f"""You are a {role} on the university's board of directors.
        Your responsibility is to evaluate proposals and participate in board discussions
        from your specific perspective and expertise.
        
        Current Discussion Context:
        - Round: {context.get('round', 1)}
        - Topic: {context.get('topic', 'Not specified')}
        - Current Consensus Level: {context.get('consensus_score', 'Not available')}
        
        Maintain your role's perspective while being:
        1. Constructive in feedback
        2. Clear in reasoning
        3. Open to compromise
        4. Focused on institutional benefit
        """
        
        # Add role-specific guidelines
        role_guidelines = self.config['role_guidelines'].get(role, {})
        if role_guidelines:
            base_prompt += f"\n\nRole-Specific Guidelines:\n{role_guidelines}"
        
        return base_prompt
    
    def _add_discussion_context(self, 
                              messages: List[Dict[str, Any]], 
                              history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Add relevant discussion history to messages"""
        relevant_history = self._select_relevant_history(history)
        
        for entry in relevant_history:
            messages.insert(1, {
                "role": "system",
                "content": f"Previous Discussion Point: {entry['content']}"
            })
        
        return messages
    
    def _parse_response(self, response: Any) -> Dict[str, Any]:
        """Parse and structure the AI response"""
        try:
            return {
                'content': response.content[0].text,
                'role': response.role,
                'model': response.model,
                'stop_reason': response.stop_reason,
                'usage': response.usage
            }
        except AttributeError as e:
            print(f"Error parsing response: {str(e)}")
            return {
                'content': str(response),
                'role': "assistant",
                'model': self.model,
                'stop_reason': "error",
                'usage': None
            }
    
    def _select_relevant_history(self, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Select most relevant historical context"""
        # For now, return last 3 entries
        return history[-3:] if len(history) > 3 else history 