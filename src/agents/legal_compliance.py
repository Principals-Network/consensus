from typing import Dict, List, Any
from .base import BoardAgent
import yaml

class LegalComplianceAgent(BoardAgent):
    def __init__(self):
        with open('src/prompts/legal_compliance.yaml', 'r') as file:
            config = yaml.safe_load(file)
            
        super().__init__(
            role="Legal Compliance Officer",
            priorities=config['priorities']
        )
        self.prompts = config['prompts']
        self.evaluation_criteria = config['evaluation_criteria']
        
    def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on legal compliance"""
        evaluation = {
            'regulatory_compliance': self._assess_regulatory_compliance(proposal),
            'legal_risks': self._assess_legal_risks(proposal),
            'policy_alignment': self._assess_policy_alignment(proposal),
            'overall_recommendation': None
        }
        return evaluation
        
    def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate compliance-focused feedback"""
        return self._generate_structured_feedback(context)
        
    def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with legal compliance rationale"""
        evaluation = self.evaluate_proposal(proposal)
        vote_decision = self._make_vote_decision(evaluation)
        return {
            'vote': vote_decision['vote'],
            'rationale': vote_decision['rationale'],
            'concerns': vote_decision['concerns'],
            'suggestions': vote_decision['suggestions']
        } 