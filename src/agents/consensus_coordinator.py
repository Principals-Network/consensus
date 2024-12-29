from typing import Dict, List, Any
from src.agents.base import BoardAgent
from src.consensus.consensus_algorithm import ConsensusAlgorithm
import yaml

class ConsensusCoordinatorAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/consensus_coordinator.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
            
        super().__init__(
            role="Consensus Coordinator",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
        self.consensus_algorithm = ConsensusAlgorithm(config)
        self.discussion_state = {}
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposal from consensus perspective"""
        evaluation = {
            'consensus_potential': await self._assess_consensus_potential(proposal),
            'stakeholder_alignment': await self._assess_stakeholder_alignment(proposal),
            'discussion_strategy': await self._develop_discussion_strategy(proposal),
            'compromise_opportunities': await self._identify_compromise_opportunities(proposal)
        }
        evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
        return evaluation

    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate consensus-focused feedback"""
        prompt = self.prompts['feedback'].format(**context)
        response = await self.ai.generate_response(prompt, self.role, context)
        return response['content']

    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote based on consensus analysis"""
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

    async def moderate_discussion(self, agent_responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Moderate the discussion between agents"""
        # Analyze current discussion state
        analysis = self.consensus_algorithm.analyze_discussion(agent_responses)
        
        # Generate moderation response
        moderation = await self._generate_moderation_response(analysis)
        
        # Update discussion state
        self.discussion_state.update({
            'current_analysis': analysis,
            'moderation_response': moderation
        })
        
        return {
            'consensus_score': analysis['consensus_score'],
            'opinion_clusters': analysis['opinion_clusters'],
            'key_disagreements': analysis['key_disagreements'],
            'moderation': moderation,
            'next_steps': analysis['next_steps']
        }

    async def _assess_consensus_potential(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess potential for reaching consensus"""
        prompt = self.prompts['consensus_potential'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'alignment_potential': 0.75,
            'compromise_feasibility': 0.8,
            'discussion_complexity': 0.6
        }

    async def _assess_stakeholder_alignment(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess alignment between stakeholders"""
        prompt = self.prompts['stakeholder_alignment'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'interest_alignment': 0.7,
            'priority_conflicts': ['budget allocation', 'timeline'],
            'common_ground': ['research value', 'innovation potential']
        }

    async def _develop_discussion_strategy(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Develop strategy for facilitating discussion"""
        prompt = self.prompts['discussion_strategy'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'focus_points': ['budget concerns', 'resource allocation'],
            'discussion_structure': ['individual perspectives', 'group discussion'],
            'facilitation_approach': 'structured dialogue'
        }

    async def _identify_compromise_opportunities(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential areas for compromise"""
        prompt = self.prompts['compromise_opportunities'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return [
            {
                'aspect': 'budget allocation',
                'suggestion': 'phased implementation',
                'feasibility': 0.8
            },
            {
                'aspect': 'resource allocation',
                'suggestion': 'shared facilities',
                'feasibility': 0.9
            }
        ]

    async def _generate_moderation_response(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate moderation response based on analysis"""
        prompt = self.prompts['moderation'].format(**analysis)
        response = await self.ai.generate_response(prompt, self.role, analysis)
        
        return {
            'summary': self._summarize_current_state(analysis),
            'focus_points': self._identify_focus_points(analysis),
            'suggested_actions': self._suggest_actions(analysis),
            'discussion_guidance': self._generate_discussion_guidance(analysis)
        }

    def _generate_recommendation(self, evaluation: Dict[str, Any]) -> str:
        """Generate recommendation based on consensus analysis"""
        consensus_potential = evaluation['consensus_potential']
        stakeholder_alignment = evaluation['stakeholder_alignment']
        
        avg_potential = sum(consensus_potential.values()) / len(consensus_potential)
        alignment_score = stakeholder_alignment['interest_alignment']
        
        if avg_potential > 0.8 and alignment_score > 0.8:
            return "Proceed with Discussion"
        elif avg_potential > 0.6 and alignment_score > 0.6:
            return "Proceed with Structured Approach"
        elif avg_potential > 0.4:
            return "Proceed with Caution"
        else:
            return "Reconsider Proposal" 