from typing import Dict, List, Any
from src.agents.base import BoardAgent
import yaml
from datetime import datetime

class DocumentationAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/documentation.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
        
        super().__init__(
            role="Documentation Officer",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
        self.discussion_history = []
        self.decision_records = {}
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposal from documentation perspective"""
        evaluation = {
            'documentation_requirements': await self._assess_documentation_needs(proposal),
            'tracking_complexity': await self._assess_tracking_complexity(proposal),
            'record_keeping_strategy': await self._develop_record_strategy(proposal),
            'transparency_measures': await self._identify_transparency_measures(proposal)
        }
        evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
        return evaluation

    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate documentation-focused feedback"""
        prompt = self.prompts['feedback'].format(**context)
        response = await self.ai.generate_response(prompt, self.role, context)
        return response['content']

    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote based on documentation considerations"""
        evaluation = await self.evaluate_proposal(proposal)
        prompt = self.prompts['voting'].format(
            evaluation=evaluation,
            proposal=proposal
        )
        response = await self.ai.generate_response(prompt, self.role, {
            'evaluation': evaluation,
            'proposal': proposal
        })
        return self._parse_vote_response(response)

    async def record_discussion(self, discussion_data: Dict[str, Any]) -> Dict[str, Any]:
        """Record and structure discussion points"""
        timestamp = datetime.now().isoformat()
        
        record = {
            'timestamp': timestamp,
            'proposal': discussion_data['proposal'],
            'key_points': await self._extract_key_points(discussion_data),
            'evaluations': await self._summarize_evaluations(discussion_data['evaluations']),
            'consensus_analysis': await self._summarize_consensus(discussion_data['consensus_analysis']),
            'votes': await self._record_votes(discussion_data['votes']),
            'decision': await self._determine_final_decision(discussion_data),
            'action_items': await self._identify_action_items(discussion_data)
        }
        
        self.discussion_history.append(record)
        return record

    async def generate_minutes(self, discussion_data: Dict[str, Any]) -> str:
        """Generate formatted meeting minutes"""
        prompt = self.prompts['minutes_generation'].format(**discussion_data)
        response = await self.ai.generate_response(prompt, self.role, discussion_data)
        
        minutes = f"""
        Board Discussion Minutes
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        
        Proposal: {discussion_data['proposal']['title']}
        
        1. Key Points Discussed:
        {await self._format_key_points(discussion_data)}
        
        2. Agent Evaluations:
        {await self._format_evaluations(discussion_data['evaluations'])}
        
        3. Consensus Analysis:
        {await self._format_consensus_analysis(discussion_data['consensus_analysis'])}
        
        4. Voting Results:
        {await self._format_voting_results(discussion_data['votes'])}
        
        5. Decision:
        {await self._format_decision(discussion_data)}
        
        6. Action Items:
        {await self._format_action_items(discussion_data)}
        
        Minutes recorded by: Documentation Officer
        """
        return minutes

    async def _assess_documentation_needs(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess documentation requirements"""
        prompt = self.prompts['documentation_needs'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'complexity_level': 'high',
            'required_templates': ['decision record', 'meeting minutes'],
            'tracking_requirements': ['milestones', 'decisions', 'action items']
        }

    def _generate_recommendation(self, evaluation: Dict[str, Any]) -> str:
        """Generate recommendation based on documentation analysis"""
        doc_requirements = evaluation['documentation_requirements']
        tracking_complexity = evaluation['tracking_complexity']
        
        if doc_requirements['complexity_level'] == 'high':
            return "Enhanced Documentation Required"
        elif tracking_complexity > 0.7:
            return "Standard Documentation with Extra Tracking"
        else:
            return "Standard Documentation Sufficient" 