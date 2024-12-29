from typing import Dict, List, Any
from .base import BoardAgent
import yaml

class FinancialOfficerAgent(BoardAgent):
    def __init__(self):
        with open('src/prompts/financial_officer.yaml', 'r') as file:
            config = yaml.safe_load(file)
            
        super().__init__(
            role="Financial Officer",
            priorities=config['priorities']
        )
        self.prompts = config['prompts']
        self.evaluation_criteria = config['evaluation_criteria']
        
    def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on financial impact"""
        evaluation = {
            'budget_impact': self._assess_budget_impact(proposal),
            'resource_efficiency': self._assess_resource_efficiency(proposal),
            'financial_sustainability': self._assess_financial_sustainability(proposal),
            'overall_recommendation': None
        }
        return evaluation 