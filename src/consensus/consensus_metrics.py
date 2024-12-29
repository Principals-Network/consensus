import numpy as np
from typing import Dict, List, Any
from collections import Counter
import networkx as nx
from src.utils.logging import setup_logger

class ConsensusMetrics:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.threshold = config.get('consensus_threshold', 0.7)
        self.weights = self._initialize_weights()
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
        
    def calculate_consensus_score(self, responses: List[Dict[str, Any]]) -> float:
        """Calculate overall consensus score from agent responses"""
        if not responses:
            return 0.0
            
        # Extract positions and weights
        positions = self._extract_positions(responses)
        weights = self._get_agent_weights(responses)
        
        # Calculate various consensus measures
        agreement_score = self._calculate_agreement_score(positions)
        similarity_score = self._calculate_similarity_score(positions)
        convergence_score = self._calculate_convergence_score(positions)
        
        # Weighted combination of measures
        consensus_score = (
            0.4 * agreement_score +
            0.4 * similarity_score +
            0.2 * convergence_score
        )
        
        return min(max(consensus_score, 0.0), 1.0)
    
    def identify_clusters(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify clusters of similar opinions"""
        if not responses:
            return []
            
        # Create similarity matrix
        positions = self._extract_positions(responses)
        similarity_matrix = self._calculate_similarity_matrix(positions)
        
        # Build graph from similarity matrix
        G = nx.Graph()
        for i in range(len(responses)):
            for j in range(i + 1, len(responses)):
                if similarity_matrix[i][j] > self.threshold:
                    G.add_edge(responses[i]['agent_role'], responses[j]['agent_role'],
                             weight=similarity_matrix[i][j])
        
        # Find communities/clusters
        communities = list(nx.community.greedy_modularity_communities(G))
        
        # Format clusters
        clusters = []
        for i, community in enumerate(communities):
            cluster = {
                'id': i + 1,
                'members': list(community),
                'size': len(community),
                'cohesion': self._calculate_cluster_cohesion(community, similarity_matrix, responses)
            }
            clusters.append(cluster)
        
        return clusters
    
    def analyze_disagreements(self, responses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify and analyze key points of disagreement"""
        if not responses:
            return []
            
        disagreements = []
        aspects = self._identify_evaluation_aspects(responses)
        
        for aspect in aspects:
            positions = self._extract_aspect_positions(responses, aspect)
            if self._is_significant_disagreement(positions):
                disagreement = {
                    'aspect': aspect,
                    'severity': self._calculate_disagreement_severity(positions),
                    'positions': self._summarize_positions(positions),
                    'potential_resolution': self._suggest_resolution(positions)
                }
                disagreements.append(disagreement)
        
        return sorted(disagreements, key=lambda x: x['severity'], reverse=True)
    
    def calculate_delphi_metrics(self, 
                               current_round: List[Dict[str, Any]], 
                               previous_rounds: List[List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Calculate Delphi method metrics across rounds"""
        metrics = {
            'convergence': self._calculate_round_convergence(current_round, previous_rounds),
            'stability': self._calculate_position_stability(current_round, previous_rounds),
            'diversity': self._calculate_opinion_diversity(current_round),
            'participation': self._calculate_participation_rate(current_round)
        }
        
        return metrics
    
    def _extract_positions(self, responses: List[Dict[str, Any]]) -> List[np.ndarray]:
        """Extract numerical position vectors from responses"""
        try:
            positions = []
            for response in responses:
                if 'evaluation' in response:
                    position = self._encode_position(response['evaluation'])
                    if np.any(position):  # Only add non-zero positions
                        positions.append(position)
            return positions
        except Exception as e:
            self.logger.error(f"Error extracting positions: {str(e)}")
            return []
    
    def _calculate_similarity_matrix(self, positions: np.ndarray) -> np.ndarray:
        """Calculate pairwise similarity matrix between positions"""
        return cosine_similarity(positions)
    
    def _calculate_cluster_cohesion(self, 
                                  community: set, 
                                  similarity_matrix: np.ndarray,
                                  responses: List[Dict[str, Any]]) -> float:
        """Calculate internal cohesion of an opinion cluster"""
        if len(community) < 2:
            return 1.0
            
        # Get indices of community members
        member_indices = [i for i, r in enumerate(responses) 
                        if r['agent_role'] in community]
        
        # Calculate average pairwise similarity within cluster
        similarities = []
        for i in range(len(member_indices)):
            for j in range(i + 1, len(member_indices)):
                similarities.append(
                    similarity_matrix[member_indices[i]][member_indices[j]]
                )
        
        return np.mean(similarities) if similarities else 0.0
    
    def _calculate_disagreement_severity(self, positions: Dict[str, Any]) -> float:
        """Calculate severity of disagreement based on position distances"""
        if not positions:
            return 0.0
            
        values = list(positions.values())
        max_diff = max(values) - min(values)
        variance = np.var(values) if len(values) > 1 else 0
        
        return (0.7 * max_diff + 0.3 * variance)
    
    def _suggest_resolution(self, positions: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest potential resolution for disagreement"""
        median_position = np.median(list(positions.values()))
        
        return {
            'suggested_value': median_position,
            'rationale': self._generate_resolution_rationale(positions),
            'required_movement': self._calculate_required_movement(positions, median_position)
        }
    
    def _initialize_weights(self) -> Dict[str, float]:
        """Initialize aspect weights for consensus calculation"""
        return {
            'agreement': 0.4,
            'similarity': 0.4,
            'convergence': 0.2
        } 
    
    def _encode_position(self, evaluation: Dict[str, Any]) -> np.ndarray:
        """Encode evaluation into numerical position vector"""
        try:
            # Define aspects to consider
            aspects = [
                'research_potential',
                'innovation_impact',
                'collaboration_opportunities',
                'knowledge_transfer',
                'space_utilization',
                'facility_requirements',
                'sustainability_impact',
                'maintenance_implications'
            ]
            
            # Initialize position vector
            position = np.zeros(len(aspects))
            
            # Encode each aspect
            for i, aspect in enumerate(aspects):
                if aspect in evaluation:
                    # Get all numerical values from the aspect
                    values = self._extract_numerical_values(evaluation[aspect])
                    position[i] = np.mean(values) if values else 0.5
            
            # Normalize
            return position / np.linalg.norm(position) if np.any(position) else position
        
        except Exception as e:
            self.logger.error(f"Error encoding position: {str(e)}")
            return np.zeros(len(aspects))
    
    def _extract_numerical_values(self, data: Any) -> List[float]:
        """Recursively extract numerical values from nested structures"""
        values = []
        
        if isinstance(data, (int, float)):
            values.append(float(data))
        elif isinstance(data, dict):
            for value in data.values():
                values.extend(self._extract_numerical_values(value))
        elif isinstance(data, (list, tuple)):
            for item in data:
                values.extend(self._extract_numerical_values(item))
            
        return [v for v in values if 0 <= v <= 1]  # Filter for valid scores 
    
    def _get_agent_weights(self, responses: List[Dict[str, Any]]) -> Dict[str, float]:
        """Get weights for each agent's opinion"""
        try:
            # Define base weights for different roles
            role_weights = {
                'Academic Affairs Officer': 0.2,
                'Financial Officer': 0.2,
                'Research and Innovation Officer': 0.2,
                'Infrastructure Officer': 0.2,
                'Student Affairs Officer': 0.1,
                'Community Impact Officer': 0.1
            }
            
            # Get weights for present agents
            weights = {}
            total_weight = 0
            for response in responses:
                role = response['agent_role']
                weight = role_weights.get(role, 0.1)  # Default weight for unknown roles
                weights[role] = weight
                total_weight += weight
            
            # Normalize weights
            if total_weight > 0:
                return {role: w/total_weight for role, w in weights.items()}
            else:
                # Equal weights if no valid weights found
                equal_weight = 1.0 / len(responses) if responses else 1.0
                return {response['agent_role']: equal_weight for response in responses}
            
        except Exception as e:
            self.logger.error(f"Error calculating agent weights: {str(e)}")
            # Fallback to equal weights
            equal_weight = 1.0 / len(responses) if responses else 1.0
            return {response['agent_role']: equal_weight for response in responses} 
    
    def _calculate_agreement_score(self, positions: List[np.ndarray]) -> float:
        """Calculate direct agreement score between positions"""
        try:
            if not positions:
                return 0.0
            
            # Calculate pairwise cosine similarities
            similarities = []
            for i in range(len(positions)):
                for j in range(i + 1, len(positions)):
                    similarity = np.dot(positions[i], positions[j])
                    similarity = similarity / (np.linalg.norm(positions[i]) * np.linalg.norm(positions[j]))
                    similarities.append(similarity)
            
            return np.mean(similarities) if similarities else 0.0
        except Exception as e:
            self.logger.error(f"Error calculating agreement score: {str(e)}")
            return 0.0
    
    def _calculate_similarity_score(self, positions: List[np.ndarray]) -> float:
        """Calculate overall similarity between positions"""
        try:
            if not positions:
                return 0.0
            
            # Calculate centroid
            centroid = np.mean(positions, axis=0)
            
            # Calculate distances to centroid
            distances = [np.linalg.norm(pos - centroid) for pos in positions]
            
            # Convert distances to similarity scores (inverse and normalize)
            max_distance = max(distances) if distances else 1.0
            similarities = [1 - (d / max_distance) for d in distances]
            
            return np.mean(similarities)
        except Exception as e:
            self.logger.error(f"Error calculating similarity score: {str(e)}")
            return 0.0
    
    def _calculate_convergence_score(self, positions: List[np.ndarray]) -> float:
        """Calculate convergence of positions"""
        try:
            if not positions:
                return 0.0
            
            # Calculate variance in each dimension
            variances = np.var(positions, axis=0)
            
            # Convert variance to convergence score (inverse)
            convergence = 1.0 - min(np.mean(variances), 1.0)
            
            return convergence
        except Exception as e:
            self.logger.error(f"Error calculating convergence score: {str(e)}")
            return 0.0
    
    def _generate_resolution_rationale(self, positions: Dict[str, Any]) -> str:
        """Generate rationale for suggested resolution"""
        try:
            median_val = np.median(list(positions.values()))
            spread = np.std(list(positions.values()))
            
            if spread < 0.2:
                return "Positions are already fairly close"
            elif spread < 0.4:
                return "Moderate adjustments needed for consensus"
            else:
                return "Significant compromises required"
        except Exception as e:
            self.logger.error(f"Error generating resolution rationale: {str(e)}")
            return "Unable to generate resolution rationale"
    
    def _calculate_required_movement(self, positions: Dict[str, Any], target: float) -> Dict[str, float]:
        """Calculate required movement for each position"""
        try:
            movements = {}
            for role, position in positions.items():
                movements[role] = abs(position - target)
            return movements
        except Exception as e:
            self.logger.error(f"Error calculating required movements: {str(e)}")
            return {} 