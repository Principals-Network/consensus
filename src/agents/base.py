from typing import Dict, List, Any
from abc import ABC, abstractmethod
from src.ai.claude_integration import ClaudeAI
from src.utils.logging import setup_logger
import yaml

class BoardAgent(ABC):
    """Base class for all board member agents"""
    
    def __init__(self, role: str, priorities: List[str], config: Dict[str, Any]):
        self.role = role
        self.priorities = priorities
        self.voting_history = []
        self.ai = ClaudeAI(config)
        self.config = config
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a proposal from agent's perspective"""
        pass
    
    @abstractmethod
    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate feedback based on agent's role"""
        pass
    
    @abstractmethod
    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast a vote with rationale"""
        pass
    
    def _construct_evaluation_prompt(self, proposal: Dict[str, Any]) -> str:
        """Construct prompt for proposal evaluation"""
        return f"""
        As the {self.role}, evaluate the following proposal:
        
        {proposal['description']}
        
        Consider these aspects from your role's perspective:
        1. Alignment with your priorities
        2. Potential impacts
        3. Concerns and risks
        4. Opportunities and benefits
        
        Provide a structured evaluation including:
        - Key points of analysis
        - Specific concerns
        - Potential improvements
        - Overall assessment
        """
    
    def _construct_feedback_prompt(self, context: Dict[str, Any]) -> str:
        """Construct prompt for feedback generation"""
        return f"""
        Based on the current discussion state and your role as {self.role},
        provide constructive feedback on:
        
        1. Areas of agreement
        2. Points of concern
        3. Suggested modifications
        4. Potential compromises
        
        Frame your feedback to be:
        - Constructive
        - Specific
        - Solution-oriented
        - Role-aligned
        """
    
    def _construct_voting_prompt(self, proposal: Dict[str, Any]) -> str:
        """Construct prompt for voting decision"""
        return f"""
        As the {self.role}, cast your vote on the current proposal:
        
        {proposal['description']}
        
        Provide:
        1. Your vote (support/oppose/abstain)
        2. Detailed rationale
        3. Key concerns (if any)
        4. Suggested modifications (if any)
        
        Base your decision on:
        - Your role's priorities
        - Previous discussion points
        - Potential impacts
        - Implementation feasibility
        """ 
    
    def _parse_evaluation_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the AI response for evaluation"""
        content = response['content']
        return {
            'key_points': self._extract_key_points(content),
            'concerns': self._extract_concerns(content),
            'improvements': self._extract_improvements(content),
            'assessment': self._extract_assessment(content)
        }
    
    def _parse_feedback_response(self, response: Dict[str, Any]) -> str:
        """Parse the AI response for feedback"""
        return response['content']
    
    def _parse_vote_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the AI response for voting"""
        content = response['content']
        return {
            'vote': self._extract_vote(content),
            'rationale': self._extract_rationale(content),
            'concerns': self._extract_concerns(content),
            'suggestions': self._extract_suggestions(content)
        } 
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from AI response"""
        # Split by newlines and look for bullet points or numbered items
        lines = content.split('\n')
        key_points = []
        for line in lines:
            line = line.strip()
            if line.startswith(('- ', '• ', '* ', '1. ', '2. ')):
                key_points.append(line.lstrip('- •*123456789. '))
        return key_points
    
    def _extract_concerns(self, content: str) -> List[str]:
        """Extract concerns from AI response"""
        concerns = []
        # Look for sections mentioning concerns, risks, or challenges
        sections = content.lower().split('concerns:' or 'risks:' or 'challenges:')
        if len(sections) > 1:
            concern_section = sections[1].split('\n\n')[0]
            concerns = [c.strip('- ') for c in concern_section.split('\n') if c.strip()]
        return concerns
    
    def _extract_improvements(self, content: str) -> List[str]:
        """Extract suggested improvements from AI response"""
        improvements = []
        sections = content.lower().split('improvements:' or 'suggestions:' or 'recommendations:')
        if len(sections) > 1:
            improvement_section = sections[1].split('\n\n')[0]
            improvements = [i.strip('- ') for i in improvement_section.split('\n') if i.strip()]
        return improvements
    
    def _extract_assessment(self, content: str) -> str:
        """Extract overall assessment from AI response"""
        sections = content.lower().split('assessment:' or 'conclusion:' or 'summary:')
        if len(sections) > 1:
            return sections[1].split('\n\n')[0].strip()
        return ""
    
    def _extract_vote(self, content: str) -> str:
        """Extract vote decision from AI response"""
        vote_map = {
            'support': 'support',
            'approve': 'support',
            'yes': 'support',
            'oppose': 'oppose',
            'reject': 'oppose',
            'no': 'oppose',
            'abstain': 'abstain'
        }
        
        content_lower = content.lower()
        for key, value in vote_map.items():
            if key in content_lower:
                return value
        return 'abstain'
    
    def _extract_rationale(self, content: str) -> str:
        """Extract voting rationale from AI response"""
        sections = content.lower().split('rationale:' or 'reasoning:' or 'because:')
        if len(sections) > 1:
            return sections[1].split('\n\n')[0].strip()
        return ""
    
    def _extract_suggestions(self, content: str) -> List[str]:
        """Extract suggestions from AI response"""
        suggestions = []
        sections = content.lower().split('suggestions:' or 'modifications:' or 'recommendations:')
        if len(sections) > 1:
            suggestion_section = sections[1].split('\n\n')[0]
            suggestions = [s.strip('- ') for s in suggestion_section.split('\n') if s.strip()]
        return suggestions 
    
    def _load_config(self, file_path: str) -> Dict[str, Any]:
        """Load and validate config file"""
        try:
            with open(file_path, 'r') as file:
                config = yaml.safe_load(file)
                self._validate_config(config)
                return config
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {file_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file: {e}")
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate config structure"""
        required_keys = ['priorities', 'prompts', 'evaluation_criteria']
        missing_keys = [key for key in required_keys if key not in config]
        if missing_keys:
            raise ValueError(f"Missing required config keys: {missing_keys}") 
    
    async def _safe_ai_call(self, prompt: str, role: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Safely make AI API calls with retries and error handling"""
        try:
            return await self.ai.generate_response(prompt, role, context)
        except Exception as e:
            self.logger.error(f"Error in AI call: {str(e)}")
            return {
                'content': "Error generating response. Please try again.",
                'error': str(e)
            } 