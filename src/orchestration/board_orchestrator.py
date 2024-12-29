from typing import Dict, List, Any
from src.agents.base import BoardAgent
from src.agents.consensus_coordinator import ConsensusCoordinatorAgent
from src.agents.documentation import DocumentationAgent
from src.config.config_loader import ConfigLoader
from src.agents.research_innovation import ResearchInnovationAgent
from src.agents.infrastructure import InfrastructureAgent
from src.agents.financial import FinancialAgent
from src.agents.academic_affairs import AcademicAffairsAgent
from src.utils.logging import setup_logger

class BoardOrchestrator:
    def __init__(self):
        self.logger = setup_logger(f"{__name__}.BoardOrchestrator")
        self.logger.info("Initializing Board Orchestrator...")
        
        # Load configuration
        self.config = ConfigLoader().get_ai_config()
        
        # Initialize all agents
        self.logger.debug("Creating board agents...")
        self.agents = [
            AcademicAffairsAgent(self.config),
            FinancialAgent(self.config),
            ResearchInnovationAgent(self.config),
            InfrastructureAgent(self.config)
        ]
        self.consensus_coordinator = ConsensusCoordinatorAgent(self.config)
        self.documentation_agent = DocumentationAgent(self.config)
        self.logger.info("All agents initialized successfully")
        
    async def initiate_discussion(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Run a full discussion round with all agents"""
        self.logger.info(f"\n{'='*50}\nStarting discussion for proposal: {proposal['title']}\n{'='*50}")
        
        discussion_state = {
            'round': 1,
            'proposal': proposal,
            'responses': [],
            'consensus_state': 'initial'
        }
        
        # Get initial evaluations from all agents
        self.logger.info("\n--- Initial Evaluation Round ---")
        evaluations = []
        for agent in self.agents:
            self.logger.info(f"\n{agent.role} is evaluating the proposal...")
            evaluation = await agent.evaluate_proposal(proposal)
            self.logger.info(f"{agent.role}'s recommendation: {evaluation.get('overall_recommendation', 'No recommendation')}")
            evaluations.append({
                'agent_role': agent.role,
                'evaluation': evaluation
            })
        
        # Get consensus analysis
        self.logger.info("\n--- Consensus Analysis ---")
        consensus_analysis = await self.consensus_coordinator.moderate_discussion(evaluations)
        self.logger.info(f"Current consensus score: {consensus_analysis['consensus_score']:.2f}")
        
        # If no consensus, get agent feedback
        if consensus_analysis['consensus_score'] < self.config['consensus_threshold']:
            self.logger.info("\n--- Feedback Round ---")
            feedback_round = []
            for agent in self.agents:
                self.logger.info(f"\n{agent.role} is providing feedback...")
                feedback = await agent.generate_feedback({
                    'evaluations': evaluations,
                    'consensus_analysis': consensus_analysis
                })
                self.logger.info(f"{agent.role}'s feedback length: {len(str(feedback))} chars")
                feedback_round.append({
                    'agent_role': agent.role,
                    'feedback': feedback
                })
            
            # Update consensus analysis with feedback
            self.logger.info("\n--- Updated Consensus Analysis ---")
            consensus_analysis = await self.consensus_coordinator.moderate_discussion(
                evaluations + feedback_round
            )
            self.logger.info(f"Updated consensus score: {consensus_analysis['consensus_score']:.2f}")
        
        # Final voting round
        self.logger.info("\n--- Final Voting Round ---")
        votes = []
        for agent in self.agents:
            self.logger.info(f"\n{agent.role} is voting...")
            vote = await agent.vote({
                'proposal': proposal,
                'evaluations': evaluations,
                'consensus_analysis': consensus_analysis
            })
            self.logger.info(f"{agent.role}'s vote: {vote.get('vote', 'No vote')} - {vote.get('rationale', 'No rationale')[:100]}...")
            votes.append({
                'agent_role': agent.role,
                'vote': vote
            })
        
        # Document the discussion
        self.logger.info("\n--- Documenting Discussion ---")
        documentation = await self.documentation_agent.record_discussion({
            'proposal': proposal,
            'evaluations': evaluations,
            'consensus_analysis': consensus_analysis,
            'votes': votes
        })
        
        self.logger.info("\n--- Discussion Complete ---")
        
        return {
            'consensus_score': consensus_analysis['consensus_score'],
            'opinion_clusters': consensus_analysis['opinion_clusters'],
            'weighted_voting': {
                'vote_analysis': self._analyze_votes(votes),
                'weight_distribution': self._calculate_weights(votes)
            },
            'key_disagreements': consensus_analysis['key_disagreements'],
            'delphi_analysis': {
                'round_number': discussion_state['round'],
                'analysis': consensus_analysis['analysis'],
                'feedback': consensus_analysis['feedback']
            },
            'suggested_compromises': consensus_analysis['suggested_compromises'],
            'documentation': documentation
        } 

    def _analyze_votes(self, votes: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze voting results"""
        vote_counts = {'support': 0, 'oppose': 0, 'abstain': 0}
        for vote_data in votes:
            vote_type = vote_data['vote']['vote']
            vote_counts[vote_type] += 1
        return vote_counts

    def _calculate_weights(self, votes: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate agent voting weights"""
        weights = {}
        for vote_data in votes:
            agent_role = vote_data['agent_role']
            # For now, equal weights
            weights[agent_role] = 1.0 / len(votes)
        return weights 