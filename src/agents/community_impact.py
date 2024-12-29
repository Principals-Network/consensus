from typing import Dict, List, Any
from .base import BoardAgent
import yaml

class CommunityImpactAgent(BoardAgent):
    def __init__(self):
        with open('src/prompts/community_impact.yaml', 'r') as file:
            config = yaml.safe_load(file)
            
        super().__init__(
            role="Community Impact Officer",
            priorities=config['priorities']
        )
        self.prompts = config['prompts']
        self.evaluation_criteria = config['evaluation_criteria']
        
    def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on community impact"""
        evaluation = {
            'public_relations': self._assess_public_relations(proposal),
            'community_engagement': self._assess_community_engagement(proposal),
            'reputation_impact': self._assess_reputation_impact(proposal),
            'overall_recommendation': None
        }
        return evaluation
        
    def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate community-focused feedback"""
        return self._generate_structured_feedback(context)
        
    def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with community impact rationale"""
        evaluation = self.evaluate_proposal(proposal)
        vote_decision = self._make_vote_decision(evaluation)
        return {
            'vote': vote_decision['vote'],
            'rationale': vote_decision['rationale'],
            'concerns': vote_decision['concerns'],
            'suggestions': vote_decision['suggestions']
        } 