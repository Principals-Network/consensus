from typing import Dict, List, Any
import numpy as np
from collections import defaultdict

class DelphiMethod:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.rounds = []
        self.feedback_history = []
        
    def conduct_round(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Conduct a single Delphi round"""
        round_data = {
            'round_number': len(self.rounds) + 1,
            'responses': responses,
            'analysis': self._analyze_round(responses),
            'feedback': self._generate_feedback(responses)
        }
        
        self.rounds.append(round_data)
        return round_data
    
    def _analyze_round(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze responses for the current round"""
        return {
            'statistical_summary': self._calculate_statistics(responses),
            'convergence_measure': self._measure_convergence(),
            'opinion_changes': self._track_opinion_changes(),
            'stability_assessment': self._assess_stability()
        }
    
    def _calculate_statistics(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate statistical measures for responses"""
        evaluations = [r['evaluation'] for r in responses]
        
        return {
            'median_scores': self._calculate_median_scores(evaluations),
            'interquartile_ranges': self._calculate_iqr(evaluations),
            'consensus_indicators': self._calculate_consensus_indicators(evaluations)
        }
    
    def _generate_feedback(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate anonymous feedback summary"""
        feedback = {
            'statistical_summary': self._format_statistical_summary(),
            'key_arguments': self._summarize_arguments(responses),
            'emerging_patterns': self._identify_patterns(),
            'suggested_considerations': self._generate_considerations()
        }
        
        self.feedback_history.append(feedback)
        return feedback 