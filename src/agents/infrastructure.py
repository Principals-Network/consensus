from typing import Dict, List, Any
from src.agents.base import BoardAgent
import yaml

class InfrastructureAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/infrastructure.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
        
        super().__init__(
            role="Infrastructure Officer",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on infrastructure impact"""
        try:
            evaluation = {
                'space_utilization': self._assess_space_utilization(proposal),
                'facility_requirements': self._assess_facility_requirements(proposal),
                'sustainability_impact': self._assess_sustainability_impact(proposal),
                'maintenance_implications': self._assess_maintenance_implications(proposal)
            }
            evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
            return evaluation
        except Exception as e:
            self.logger.error(f"Error evaluating proposal: {str(e)}")
            return {
                'overall_recommendation': "Need More Information",
                'error': str(e)
            }

    def _assess_space_utilization(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess space utilization and efficiency"""
        try:
            space_reqs = proposal.get('space_requirements', {})
            
            # Calculate basic metrics
            total_space = sum(space_reqs.values())
            if total_space == 0:
                return {
                    'total_space_needed': 0,
                    'space_efficiency': 0.5,
                    'utilization_rate': 0.5,
                    'optimization_potential': []
                }
            
            # Calculate efficiency metrics
            space_efficiency = self._calculate_space_efficiency(space_reqs)
            utilization_rate = self._estimate_utilization_rate(space_reqs)
            
            return {
                'total_space_needed': total_space,
                'space_efficiency': space_efficiency,
                'utilization_rate': utilization_rate,
                'optimization_potential': self._identify_optimization_opportunities(space_reqs)
            }
        except Exception as e:
            self.logger.error(f"Error assessing space utilization: {str(e)}")
            return {
                'total_space_needed': 0,
                'space_efficiency': 0.5,
                'utilization_rate': 0.5,
                'optimization_potential': []
            }
    
    def _assess_facility_requirements(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess facility requirements and modifications"""
        return {
            'renovation_needs': self._identify_renovation_needs(proposal),
            'equipment_requirements': self._assess_equipment_needs(proposal),
            'infrastructure_upgrades': self._identify_infrastructure_upgrades(proposal),
            'timeline_feasibility': self._evaluate_timeline_feasibility(proposal)
        }
    
    def _assess_sustainability_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess environmental and sustainability impact"""
        return {
            'energy_efficiency': self._evaluate_energy_efficiency(proposal),
            'resource_consumption': self._estimate_resource_consumption(proposal),
            'environmental_impact': self._assess_environmental_impact(proposal),
            'sustainability_score': self._calculate_sustainability_score(proposal)
        }
    
    def _assess_maintenance_implications(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess maintenance requirements and costs"""
        space_reqs = proposal.get('space_requirements', {})
        total_space = sum(space_reqs.values())
        
        # Calculate annual maintenance costs
        maintenance_costs = {
            'routine': total_space * 4,    # $4 per sq ft annually
            'preventive': total_space * 2,  # $2 per sq ft annually
            'repairs': total_space * 1.5,   # $1.5 per sq ft annually
            'specialized': space_reqs.get('research_labs', 0) * 8  # $8 per sq ft for labs
        }
        
        return {
            'annual_costs': maintenance_costs,
            'total_annual_cost': sum(maintenance_costs.values()),
            'maintenance_schedule': self._generate_maintenance_schedule(proposal),
            'staffing_requirements': self._estimate_maintenance_staffing(proposal)
        }
    
    def _generate_maintenance_schedule(self, proposal: Dict[str, Any]) -> Dict[str, str]:
        """Generate recommended maintenance schedule"""
        return {
            'daily': 'Basic cleaning and monitoring',
            'weekly': 'Equipment checks and minor maintenance',
            'monthly': 'Detailed systems inspection',
            'quarterly': 'Major systems maintenance',
            'annual': 'Comprehensive facility audit'
        }
    
    def _estimate_maintenance_staffing(self, proposal: Dict[str, Any]) -> Dict[str, int]:
        """Estimate required maintenance staff"""
        space_reqs = proposal.get('space_requirements', {})
        total_space = sum(space_reqs.values())
        
        # Estimate staff needs based on space
        return {
            'technicians': max(1, int(total_space / 50000)),  # 1 tech per 50k sq ft
            'specialists': max(1, int(space_reqs.get('research_labs', 0) / 20000)),  # 1 specialist per 20k lab sq ft
            'supervisors': max(1, int(total_space / 100000))  # 1 supervisor per 100k sq ft
        }
    
    def _calculate_space_efficiency(self, space_reqs: Dict[str, int]) -> float:
        """Calculate space utilization efficiency"""
        total_space = sum(space_reqs.values())
        usable_space = space_reqs.get('research_labs', 0) + space_reqs.get('offices', 0)
        return usable_space / total_space if total_space > 0 else 0
    
    def _estimate_utilization_rate(self, space_reqs: Dict[str, int]) -> float:
        """Estimate expected space utilization rate"""
        # Implement utilization rate calculation based on space type and usage patterns
        base_rates = {
            'research_labs': 0.8,
            'offices': 0.7,
            'common_areas': 0.5
        }
        
        total_weighted_rate = sum(
            space_reqs.get(space_type, 0) * rate
            for space_type, rate in base_rates.items()
        )
        total_space = sum(space_reqs.values())
        
        return total_weighted_rate / total_space if total_space > 0 else 0
    
    def _generate_recommendation(self, proposal: Dict[str, Any]) -> str:
        """Generate overall recommendation based on infrastructure analysis"""
        space_score = self._calculate_space_score(proposal)
        facility_score = self._calculate_facility_score(proposal)
        sustainability_score = self._calculate_sustainability_score(proposal)
        maintenance_score = self._calculate_maintenance_score(proposal)
        
        total_score = (
            space_score * 0.3 +
            facility_score * 0.3 +
            sustainability_score * 0.2 +
            maintenance_score * 0.2
        )
        
        if total_score > 0.8:
            return "Strongly Support"
        elif total_score > 0.6:
            return "Support with Minor Modifications"
        elif total_score > 0.4:
            return "Support with Major Modifications"
        else:
            return "Cannot Support - Infrastructure Constraints"
    
    def _calculate_space_score(self, proposal: Dict[str, Any]) -> float:
        """Calculate space utilization score"""
        space_analysis = self._assess_space_utilization(proposal)
        weights = {
            'space_efficiency': 0.4,
            'utilization_rate': 0.4,
            'optimization_potential': 0.2
        }
        
        return sum(
            weights[key] * self._normalize_score(value)
            for key, value in space_analysis.items()
            if key in weights
        )
    
    def _normalize_score(self, value: Any) -> float:
        """Normalize various score types to 0-1 range"""
        if isinstance(value, dict):
            return sum(value.values()) / len(value)
        elif isinstance(value, (int, float)):
            return min(max(value, 0), 1)
        else:
            return 0.5
        
    def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate infrastructure-focused feedback"""
        return self._generate_structured_feedback(context)
        
    def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with infrastructure rationale"""
        evaluation = self.evaluate_proposal(proposal)
        vote_decision = self._make_vote_decision(evaluation)
        return {
            'vote': vote_decision['vote'],
            'rationale': vote_decision['rationale'],
            'concerns': vote_decision['concerns'],
            'suggestions': vote_decision['suggestions']
        } 

    def _identify_optimization_opportunities(self, space_reqs: Dict[str, int]) -> List[Dict[str, Any]]:
        """Identify opportunities for space optimization"""
        opportunities = []
        total_space = sum(space_reqs.values())
        
        if total_space == 0:
            return opportunities
        
        # Check lab space utilization
        lab_space = space_reqs.get('research_labs', 0)
        lab_ratio = lab_space / total_space
        if lab_ratio > 0.5:
            opportunities.append({
                'area': 'research_labs',
                'type': 'space_sharing',
                'description': 'Implement shared lab space model',
                'potential_savings': 0.2,
                'impact': 'medium'
            })
        
        # Check office space efficiency
        office_space = space_reqs.get('offices', 0)
        office_ratio = office_space / total_space
        if office_ratio > 0.3:
            opportunities.append({
                'area': 'offices',
                'type': 'flexible_workspace',
                'description': 'Implement flexible/hybrid workspace model',
                'potential_savings': 0.25,
                'impact': 'high'
            })
        
        # Check common areas utilization
        common_space = space_reqs.get('common_areas', 0)
        common_ratio = common_space / total_space
        if common_ratio < 0.2:
            opportunities.append({
                'area': 'common_areas',
                'type': 'multi_purpose',
                'description': 'Create multi-purpose common spaces',
                'potential_savings': 0.15,
                'impact': 'medium'
            })
        
        # Consider scheduling optimization
        if lab_space > 0:
            opportunities.append({
                'area': 'scheduling',
                'type': 'time_sharing',
                'description': 'Implement advanced lab scheduling system',
                'potential_savings': 0.1,
                'impact': 'high'
            })
        
        # Consider technology integration
        opportunities.append({
            'area': 'technology',
            'type': 'smart_building',
            'description': 'Implement smart space monitoring and management',
            'potential_savings': 0.15,
            'impact': 'high'
        })
        
        return opportunities 

    def _identify_renovation_needs(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify necessary renovations and modifications"""
        space_reqs = proposal.get('space_requirements', {})
        renovations = []
        
        # Lab space renovations
        if space_reqs.get('research_labs', 0) > 0:
            renovations.append({
                'area': 'research_labs',
                'type': 'specialized_facilities',
                'description': 'Lab space modifications for AI research',
                'priority': 'high',
                'estimated_cost': space_reqs['research_labs'] * 1000  # $1000 per sq ft
            })
        
        # Office renovations
        if space_reqs.get('offices', 0) > 0:
            renovations.append({
                'area': 'offices',
                'type': 'workspace_modernization',
                'description': 'Modern collaborative workspace setup',
                'priority': 'medium',
                'estimated_cost': space_reqs['offices'] * 500  # $500 per sq ft
            })
        
        # Common area renovations
        if space_reqs.get('common_areas', 0) > 0:
            renovations.append({
                'area': 'common_areas',
                'type': 'multi_purpose_conversion',
                'description': 'Flexible meeting and collaboration spaces',
                'priority': 'medium',
                'estimated_cost': space_reqs['common_areas'] * 400  # $400 per sq ft
            })
        
        return renovations

    def _assess_equipment_needs(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess equipment requirements and specifications"""
        research_areas = proposal.get('research_areas', [])
        space_reqs = proposal.get('space_requirements', {})
        
        base_equipment = {
            'computing': {
                'type': 'High-performance computing infrastructure',
                'priority': 'high',
                'estimated_cost': 500000
            },
            'networking': {
                'type': 'Advanced networking equipment',
                'priority': 'high',
                'estimated_cost': 200000
            },
            'security': {
                'type': 'Security systems and access control',
                'priority': 'medium',
                'estimated_cost': 150000
            }
        }
        
        # Add research-specific equipment
        if any('AI' in area for area in research_areas):
            base_equipment['ai_cluster'] = {
                'type': 'AI Computing Cluster',
                'priority': 'high',
                'estimated_cost': 1000000
            }
        
        return base_equipment

    def _identify_infrastructure_upgrades(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify necessary infrastructure upgrades"""
        upgrades = []
        space_reqs = proposal.get('space_requirements', {})
        total_space = sum(space_reqs.values())
        
        # Power infrastructure
        upgrades.append({
            'system': 'electrical',
            'type': 'power_upgrade',
            'description': 'Enhanced power distribution for computing equipment',
            'priority': 'high',
            'estimated_cost': total_space * 50  # $50 per sq ft
        })
        
        # HVAC upgrades
        upgrades.append({
            'system': 'hvac',
            'type': 'cooling_upgrade',
            'description': 'Enhanced cooling for computing equipment',
            'priority': 'high',
            'estimated_cost': total_space * 40  # $40 per sq ft
        })
        
        # Network infrastructure
        upgrades.append({
            'system': 'network',
            'type': 'connectivity_upgrade',
            'description': 'High-speed network infrastructure',
            'priority': 'high',
            'estimated_cost': total_space * 30  # $30 per sq ft
        })
        
        return upgrades

    def _evaluate_timeline_feasibility(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate feasibility of implementation timeline"""
        timeline = proposal.get('timeline', '3 years')
        try:
            years = float(timeline.split()[0])
        except (ValueError, IndexError):
            years = 3.0
        
        # Calculate feasibility scores
        renovation_time = 1.5  # Base renovation time in years
        equipment_time = 0.5   # Base equipment installation time
        upgrade_time = 1.0     # Base infrastructure upgrade time
        
        total_required_time = renovation_time + equipment_time + upgrade_time
        timeline_feasibility = min(years / total_required_time, 1.0)
        
        return {
            'timeline_feasibility': timeline_feasibility,
            'required_time': total_required_time,
            'proposed_time': years,
            'risk_level': 'low' if timeline_feasibility > 0.8 else 'medium' if timeline_feasibility > 0.6 else 'high'
        } 

    def _evaluate_energy_efficiency(self, proposal: Dict[str, Any]) -> float:
        """Evaluate energy efficiency potential"""
        space_reqs = proposal.get('space_requirements', {})
        total_space = sum(space_reqs.values())
        
        # Base efficiency score
        base_score = 0.7  # Modern building standards
        
        # Adjust for space type
        if total_space > 0:
            lab_ratio = space_reqs.get('research_labs', 0) / total_space
            base_score -= lab_ratio * 0.2  # Labs are less energy efficient
        
        return base_score

    def _estimate_resource_consumption(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Estimate resource consumption metrics"""
        space_reqs = proposal.get('space_requirements', {})
        total_space = sum(space_reqs.values())
        
        return {
            'power_usage': total_space * 50,  # kWh per year per sq ft
            'water_usage': total_space * 15,  # Gallons per day per sq ft
            'hvac_load': total_space * 30,    # BTU per hour per sq ft
            'efficiency_score': self._evaluate_energy_efficiency(proposal)
        }

    def _assess_environmental_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess environmental impact of the proposal"""
        resource_consumption = self._estimate_resource_consumption(proposal)
        
        return {
            'carbon_footprint': resource_consumption['power_usage'] * 0.4,  # CO2 tons per year
            'water_impact': resource_consumption['water_usage'] * 365,      # Annual water usage
            'waste_generation': sum(proposal.get('space_requirements', {}).values()) * 2.5,  # Pounds per day
            'mitigation_potential': self._evaluate_energy_efficiency(proposal)
        }

    def _calculate_sustainability_score(self, proposal: Dict[str, Any]) -> float:
        """Calculate overall sustainability score"""
        energy_efficiency = self._evaluate_energy_efficiency(proposal)
        environmental_impact = self._assess_environmental_impact(proposal)
        
        # Weight different factors
        weights = {
            'energy_efficiency': 0.4,
            'environmental_impact': 0.3,
            'mitigation_potential': 0.3
        }
        
        return (
            energy_efficiency * weights['energy_efficiency'] +
            environmental_impact['mitigation_potential'] * weights['mitigation_potential'] +
            (1 - environmental_impact['carbon_footprint'] / 1000) * weights['environmental_impact']
        ) 

    def _calculate_facility_score(self, evaluation: Dict[str, Any]) -> float:
        """Calculate overall facility score"""
        try:
            # Extract component scores
            space_score = evaluation['space_utilization'].get('space_efficiency', 0.5)
            facility_reqs = evaluation['facility_requirements']
            timeline_score = facility_reqs.get('timeline_feasibility', {}).get('timeline_feasibility', 0.5)
            
            # Calculate renovation feasibility
            renovation_needs = facility_reqs.get('renovation_needs', [])
            renovation_cost = sum(need.get('estimated_cost', 0) for need in renovation_needs)
            renovation_score = 1.0 - min(renovation_cost / 5000000, 1.0)  # Scale based on $5M threshold
            
            # Weight the components
            weights = {
                'space': 0.3,
                'renovation': 0.3,
                'timeline': 0.4
            }
            
            return (
                space_score * weights['space'] +
                renovation_score * weights['renovation'] +
                timeline_score * weights['timeline']
            )
        except Exception as e:
            self.logger.error(f"Error calculating facility score: {str(e)}")
            return 0.5 

    def _calculate_maintenance_score(self, evaluation: Dict[str, Any]) -> float:
        """Calculate maintenance feasibility score"""
        try:
            maintenance_impl = evaluation.get('maintenance_implications', {})
            
            # Get annual costs
            annual_costs = maintenance_impl.get('annual_costs', {})
            total_cost = maintenance_impl.get('total_annual_cost', 0)
            
            # Calculate cost feasibility (lower is better)
            cost_score = 1.0 - min(total_cost / 1000000, 1.0)  # Scale based on $1M threshold
            
            # Get staffing requirements
            staffing = maintenance_impl.get('staffing_requirements', {})
            total_staff = sum(staffing.values())
            staffing_score = 1.0 - min(total_staff / 10, 1.0)  # Scale based on 10 staff threshold
            
            # Weight the components
            weights = {
                'cost': 0.6,
                'staffing': 0.4
            }
            
            return (
                cost_score * weights['cost'] +
                staffing_score * weights['staffing']
            )
        except Exception as e:
            self.logger.error(f"Error calculating maintenance score: {str(e)}")
            return 0.5 