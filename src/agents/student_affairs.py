from typing import Dict, List, Any
from .base import BoardAgent
import yaml

class StudentAffairsAgent(BoardAgent):
    def __init__(self):
        with open('src/prompts/student_affairs.yaml', 'r') as file:
            config = yaml.safe_load(file)
            
        super().__init__(
            role="Student Affairs Officer",
            priorities=config['priorities']
        )
        self.prompts = config['prompts']
        self.evaluation_criteria = config['evaluation_criteria']
        
    def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on student impact"""
        evaluation = {
            'student_experience': self._assess_student_experience(proposal),
            'accessibility_impact': self._assess_accessibility(proposal),
            'service_quality': self._assess_service_quality(proposal),
            'overall_recommendation': None
        }
        return evaluation
        
    def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate student-centered feedback"""
        return self._generate_structured_feedback(context)
        
    def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with student welfare rationale"""
        evaluation = self.evaluate_proposal(proposal)
        vote_decision = self._make_vote_decision(evaluation)
        return {
            'vote': vote_decision['vote'],
            'rationale': vote_decision['rationale'],
            'concerns': vote_decision['concerns'],
            'suggestions': vote_decision['suggestions']
        } 