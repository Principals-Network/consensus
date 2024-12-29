from typing import Dict, List, Any
from src.consensus.consensus_metrics import ConsensusMetrics
import numpy as np

class ConsensusAlgorithm:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.metrics = ConsensusMetrics(config)
        self.min_consensus_threshold = config.get('min_consensus_threshold', 0.7)
        
    def analyze_discussion(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the current state of discussion and suggest next steps"""
        # Calculate consensus metrics
        consensus_score = self.metrics.calculate_consensus_score(responses)
        opinion_clusters = self.metrics.identify_clusters(responses)
        key_disagreements = self.metrics.analyze_disagreements(responses)
        
        # Generate analysis and recommendations
        analysis = {
            'consensus_score': consensus_score,
            'opinion_clusters': opinion_clusters,
            'key_disagreements': key_disagreements,
            'next_steps': self._determine_next_steps(consensus_score, key_disagreements),
            'suggested_compromises': self._generate_compromise_suggestions(
                responses, key_disagreements
            )
        }
        
        return analysis
    
    def _determine_next_steps(self, 
                            consensus_score: float, 
                            disagreements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Determine next steps based on current discussion state"""
        steps = []
        
        if consensus_score < self.min_consensus_threshold:
            # Add steps to address key disagreements
            for disagreement in disagreements:
                steps.append({
                    'action': 'address_disagreement',
                    'aspect': disagreement['aspect'],
                    'severity': disagreement['severity'],
                    'suggested_approach': self._suggest_resolution_approach(disagreement)
                })
            
            # Add general consensus-building steps
            steps.extend([
                {
                    'action': 'clarify_positions',
                    'description': 'Request detailed explanations of positions'
                },
                {
                    'action': 'identify_common_ground',
                    'description': 'Focus discussion on areas of agreement'
                },
                {
                    'action': 'explore_compromises',
                    'description': 'Propose potential compromise solutions'
                }
            ])
        
        return steps
    
    def _suggest_resolution_approach(self, disagreement: Dict[str, Any]) -> str:
        """Suggest approach for resolving specific disagreement"""
        severity = disagreement.get('severity', 0.5)
        
        if severity > 0.8:
            return "Schedule dedicated discussion session"
        elif severity > 0.5:
            return "Request written position clarifications"
        else:
            return "Address during regular discussion"
    
    def _generate_compromise_suggestions(self,
                                      responses: List[Dict[str, Any]],
                                      disagreements: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate specific compromise suggestions"""
        suggestions = []
        
        for disagreement in disagreements:
            suggestion = {
                'aspect': disagreement['aspect'],
                'description': f"Find middle ground on {disagreement['aspect']}",
                'supporting_agents': [r['agent_role'] for r in responses if self._supports_aspect(r, disagreement['aspect'])],
                'expected_impact': 'high' if disagreement['severity'] > 0.7 else 'medium',
                'acceptance_likelihood': self._estimate_acceptance_likelihood(responses, disagreement)
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def _supports_aspect(self, response: Dict[str, Any], aspect: str) -> bool:
        """Check if agent supports particular aspect"""
        try:
            evaluation = response.get('evaluation', {})
            if aspect in evaluation:
                scores = self.metrics._extract_numerical_values(evaluation[aspect])
                return np.mean(scores) > 0.6 if scores else False
            return False
        except Exception as e:
            self.logger.error(f"Error checking aspect support: {str(e)}")
            return False
    
    def _estimate_acceptance_likelihood(self, responses: List[Dict[str, Any]], disagreement: Dict[str, Any]) -> float:
        """Estimate likelihood of compromise acceptance"""
        try:
            # Count supportive agents
            support_count = sum(1 for r in responses if self._supports_aspect(r, disagreement['aspect']))
            return support_count / len(responses) if responses else 0.5
        except Exception as e:
            self.logger.error(f"Error estimating acceptance likelihood: {str(e)}")
            return 0.5 