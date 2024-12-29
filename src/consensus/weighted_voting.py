from typing import Dict, List, Any
import numpy as np
from collections import defaultdict

class WeightedVoting:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.weight_schemes = {
            'expertise_based': self._calculate_expertise_weights,
            'stake_based': self._calculate_stake_weights,
            'consensus_contribution': self._calculate_contribution_weights
        }
    
    def calculate_decision(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate weighted voting decision"""
        weights = self._compute_weights(responses)
        weighted_votes = self._apply_weights(responses, weights)
        
        return {
            'decision': self._determine_outcome(weighted_votes),
            'confidence': self._calculate_decision_confidence(weighted_votes),
            'weight_distribution': weights,
            'vote_analysis': self._analyze_votes(weighted_votes)
        }
    
    def _compute_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Compute weights for each agent based on multiple factors"""
        weights = defaultdict(float)
        
        for scheme, weight_func in self.weight_schemes.items():
            scheme_weights = weight_func(responses)
            for agent, weight in scheme_weights.items():
                weights[agent] += weight * self.config['weight_scheme_importance'][scheme]
        
        return self._normalize_weights(weights)
    
    def _calculate_expertise_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate weights based on agent expertise"""
        weights = {}
        for response in responses:
            agent = response['agent_role']
            weights[agent] = self._evaluate_expertise(response)
        return weights
    
    def _calculate_stake_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate weights based on agent stake in the decision"""
        weights = {}
        for response in responses:
            agent = response['agent_role']
            weights[agent] = self._evaluate_stake(response)
        return weights
    
    def _calculate_contribution_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate weights based on contribution to consensus"""
        weights = {}
        for response in responses:
            agent = response['agent_role']
            weights[agent] = self._evaluate_contribution(response)
        return weights 