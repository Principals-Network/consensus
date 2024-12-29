from typing import Dict, List, Any
from src.agents.base import BoardAgent
import yaml

class FinancialAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/financial.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
        
        super().__init__(
            role="Financial Officer",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on financial impact"""
        evaluation = {
            'budget_analysis': await self._assess_budget_impact(proposal),
            'resource_allocation': await self._assess_resource_allocation(proposal),
            'financial_sustainability': await self._assess_financial_sustainability(proposal),
            'roi_projection': await self._assess_roi(proposal)
        }
        evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
        return evaluation

    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate financial perspective feedback"""
        prompt = self.prompts['feedback'].format(**context)
        response = await self.ai.generate_response(prompt, self.role, context)
        return response['content']

    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with financial rationale"""
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

    async def _assess_budget_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess budget impact and financial requirements"""
        try:
            prompt = self.prompts['budget_analysis'].format(
                budget=proposal.get('budget', 0),
                timeline=proposal.get('timeline', 'Not specified'),
                funding_sources=proposal.get('funding_sources', {})
            )
            response = await self.ai.generate_response(prompt, self.role, proposal)
            
            budget = proposal.get('budget', 0)
            funding_sources = proposal.get('funding_sources', {})
            
            return {
                'immediate_cost': budget,
                'annual_impact': self._calculate_annual_impact(proposal),
                'funding_sources': self._identify_funding_sources(proposal),
                'risk_assessment': self._assess_financial_risk(proposal)
            }
        except KeyError as e:
            print(f"Warning: Missing key in proposal for budget analysis: {e}")
            return {
                'immediate_cost': 0,
                'annual_impact': 0,
                'funding_sources': {},
                'risk_assessment': {'budget_overrun': 1.0}
            }

    async def _assess_resource_allocation(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess resource allocation efficiency"""
        prompt = self.prompts['resource_allocation'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'efficiency': self._evaluate_resource_efficiency(proposal),
            'distribution': self._analyze_resource_distribution(proposal),
            'optimization': self._suggest_resource_optimization(proposal)
        }

    async def _assess_financial_sustainability(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess long-term financial sustainability"""
        prompt = self.prompts['sustainability'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        return {
            'long_term_viability': self._evaluate_long_term_viability(proposal),
            'revenue_potential': self._assess_revenue_potential(proposal),
            'cost_reduction_opportunities': self._identify_cost_reductions(proposal)
        }

    async def _assess_roi(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Project return on investment"""
        prompt = self.prompts['roi_analysis'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        
        costs = self._calculate_total_costs(proposal)
        benefits = self._project_benefits(proposal)
        timeline = float(proposal.get('timeline', '1').split()[0])
        
        roi = (benefits - costs) / costs if costs > 0 else 0
        
        return {
            'roi_percentage': roi * 100,
            'payback_period': costs / (benefits / timeline) if benefits > 0 else float('inf'),
            'net_present_value': self._calculate_npv(costs, benefits, timeline)
        }

    def _generate_recommendation(self, evaluation: Dict[str, Any]) -> str:
        """Generate overall recommendation based on financial analysis"""
        roi = evaluation['roi_projection']
        risks = evaluation['budget_analysis']['risk_assessment']
        sustainability = evaluation['financial_sustainability']
        
        if roi['roi_percentage'] > 15 and risks['budget_overrun'] < 0.3:
            return "Strongly Support"
        elif roi['roi_percentage'] > 10 and risks['budget_overrun'] < 0.4:
            return "Support with Conditions"
        elif roi['roi_percentage'] > 5:
            return "Neutral"
        else:
            return "Oppose" 

    def _calculate_annual_impact(self, proposal: Dict[str, Any]) -> float:
        """Calculate annual financial impact"""
        total_budget = proposal.get('budget', 0)
        timeline_years = float(proposal.get('timeline', '1').split()[0])
        return total_budget / timeline_years

    def _identify_funding_sources(self, proposal: Dict[str, Any]) -> Dict[str, Dict[str, float]]:
        """Analyze funding sources and their reliability"""
        funding_sources = proposal.get('funding_sources', {})
        return {
            source: {
                'amount': proposal.get('budget', 0) * percentage,
                'reliability': self._assess_funding_reliability(source)
            }
            for source, percentage in funding_sources.items()
        }

    def _assess_funding_reliability(self, source: str) -> float:
        """Assess reliability of funding source"""
        reliability_scores = {
            'university': 0.9,
            'grants': 0.7,
            'industry': 0.8,
            'donations': 0.5
        }
        return reliability_scores.get(source.lower(), 0.5)

    def _assess_financial_risk(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess various financial risks"""
        return {
            'budget_overrun': self._calculate_overrun_risk(proposal),
            'funding_stability': self._assess_funding_stability(proposal),
            'operational_risk': self._assess_operational_risk(proposal)
        }

    def _calculate_overrun_risk(self, proposal: Dict[str, Any]) -> float:
        """Calculate risk of budget overrun"""
        budget = proposal.get('budget', 0)
        timeline = float(proposal.get('timeline', '1').split()[0])
        complexity = len(proposal.get('research_areas', []))
        
        # Higher budget, longer timeline, and more complexity increase risk
        risk = (
            0.3 * min(budget / 1000000, 1.0) +  # Budget factor
            0.3 * min(timeline / 5, 1.0) +      # Timeline factor
            0.4 * min(complexity / 5, 1.0)      # Complexity factor
        )
        return risk

    def _assess_funding_stability(self, proposal: Dict[str, Any]) -> float:
        """Assess stability of funding sources"""
        funding_sources = proposal.get('funding_sources', {})
        if not funding_sources:
            return 1.0  # Maximum risk if no funding sources specified
        
        weighted_stability = sum(
            percentage * self._assess_funding_reliability(source)
            for source, percentage in funding_sources.items()
        )
        return 1.0 - weighted_stability  # Convert to risk score

    def _assess_operational_risk(self, proposal: Dict[str, Any]) -> float:
        """Assess operational financial risks"""
        staffing = proposal.get('staffing', {})
        space = proposal.get('space_requirements', {})
        
        staff_cost_risk = min(sum(staffing.values()) * 0.1, 1.0)
        space_cost_risk = min(sum(space.values()) * 0.0001, 1.0)
        
        return (staff_cost_risk + space_cost_risk) / 2

    def _evaluate_resource_efficiency(self, proposal: Dict[str, Any]) -> float:
        """Evaluate efficiency of resource utilization"""
        space_reqs = proposal.get('space_requirements', {})
        staffing = proposal.get('staffing', {})
        
        if not space_reqs or not staffing:
            return 0.5
        
        space_efficiency = self._calculate_space_efficiency(space_reqs, staffing)
        staff_efficiency = self._calculate_staff_efficiency(staffing)
        
        return (space_efficiency + staff_efficiency) / 2

    def _analyze_resource_distribution(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Analyze distribution of resources"""
        return {
            'space_allocation': self._analyze_space_distribution(proposal),
            'staff_allocation': self._analyze_staff_distribution(proposal),
            'budget_allocation': self._analyze_budget_distribution(proposal)
        }

    def _suggest_resource_optimization(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Suggest ways to optimize resource usage"""
        return [
            {
                'area': 'space',
                'suggestion': 'Implement shared workspace model',
                'potential_savings': 0.15
            },
            {
                'area': 'staffing',
                'suggestion': 'Phase hiring with project milestones',
                'potential_savings': 0.20
            }
        ]

    def _calculate_total_costs(self, proposal: Dict[str, Any]) -> float:
        """Calculate total costs including indirect costs"""
        direct_costs = proposal.get('budget', 0)
        indirect_rate = 0.4  # 40% indirect cost rate
        return direct_costs * (1 + indirect_rate)

    def _project_benefits(self, proposal: Dict[str, Any]) -> float:
        """Project financial benefits"""
        budget = proposal.get('budget', 0)
        research_areas = len(proposal.get('research_areas', []))
        funding_mix = len(proposal.get('funding_sources', {}))
        
        # Simple benefit projection model
        return budget * (1.5 + 0.1 * research_areas + 0.1 * funding_mix)

    def _calculate_npv(self, costs: float, benefits: float, timeline: float) -> float:
        """Calculate Net Present Value"""
        discount_rate = 0.1  # 10% discount rate
        
        npv = -costs  # Initial investment
        annual_benefit = benefits / timeline
        
        for year in range(int(timeline)):
            npv += annual_benefit / ((1 + discount_rate) ** (year + 1))
        
        return npv

    def _calculate_space_efficiency(self, space_reqs: Dict[str, int], staffing: Dict[str, int]) -> float:
        """Calculate space utilization efficiency"""
        total_space = sum(space_reqs.values())
        total_staff = sum(staffing.values())
        
        if total_staff == 0:
            return 0.5
        
        space_per_person = total_space / total_staff
        target_space = 200  # Target sq ft per person
        
        return max(0, min(1, target_space / space_per_person))

    def _calculate_staff_efficiency(self, staffing: Dict[str, int]) -> float:
        """Calculate staff utilization efficiency"""
        faculty = staffing.get('faculty', 0)
        staff = staffing.get('staff', 0)
        students = staffing.get('graduate_students', 0)
        
        if faculty == 0:
            return 0.5
        
        support_ratio = (staff + students) / faculty
        target_ratio = 5  # Target support staff per faculty
        
        return max(0, min(1, target_ratio / support_ratio)) 

    def _analyze_space_distribution(self, proposal: Dict[str, Any]) -> float:
        """Analyze space allocation distribution"""
        space_reqs = proposal.get('space_requirements', {})
        if not space_reqs:
            return 0.5
        
        # Calculate distribution metrics
        total_space = sum(space_reqs.values())
        if total_space == 0:
            return 0.5
        
        # Analyze distribution ratios
        ratios = {
            'research': space_reqs.get('research_labs', 0) / total_space,
            'office': space_reqs.get('offices', 0) / total_space,
            'common': space_reqs.get('common_areas', 0) / total_space
        }
        
        # Score based on ideal ratios
        ideal_ratios = {'research': 0.5, 'office': 0.3, 'common': 0.2}
        score = sum(
            1 - abs(ratios[space_type] - ideal)
            for space_type, ideal in ideal_ratios.items()
        ) / len(ideal_ratios)
        
        return score

    def _analyze_staff_distribution(self, proposal: Dict[str, Any]) -> float:
        """Analyze staff allocation distribution"""
        staffing = proposal.get('staffing', {})
        if not staffing:
            return 0.5
        
        total_staff = sum(staffing.values())
        if total_staff == 0:
            return 0.5
        
        # Calculate staff ratios
        ratios = {
            'faculty': staffing.get('faculty', 0) / total_staff,
            'staff': staffing.get('staff', 0) / total_staff,
            'students': staffing.get('graduate_students', 0) / total_staff
        }
        
        # Score based on ideal ratios
        ideal_ratios = {'faculty': 0.3, 'staff': 0.3, 'students': 0.4}
        score = sum(
            1 - abs(ratios[staff_type] - ideal)
            for staff_type, ideal in ideal_ratios.items()
        ) / len(ideal_ratios)
        
        return score

    def _analyze_budget_distribution(self, proposal: Dict[str, Any]) -> float:
        """Analyze budget allocation distribution"""
        budget = proposal.get('budget', 0)
        if budget == 0:
            return 0.5
        
        funding_sources = proposal.get('funding_sources', {})
        if not funding_sources:
            return 0.5
        
        # Calculate funding diversity score
        source_count = len(funding_sources)
        max_sources = 4  # Expected maximum number of funding sources
        diversity_score = min(source_count / max_sources, 1.0)
        
        # Calculate distribution balance
        max_percentage = max(funding_sources.values())
        min_percentage = min(funding_sources.values())
        balance_score = 1 - (max_percentage - min_percentage)
        
        # Combine scores
        return (diversity_score * 0.6 + balance_score * 0.4)

    def _evaluate_long_term_viability(self, proposal: Dict[str, Any]) -> float:
        """Evaluate long-term financial viability"""
        # Calculate viability score based on multiple factors
        scores = [
            self._assess_funding_stability(proposal),
            self._evaluate_revenue_sustainability(proposal),
            self._assess_cost_structure(proposal)
        ]
        return sum(scores) / len(scores)

    def _assess_revenue_potential(self, proposal: Dict[str, Any]) -> float:
        """Assess potential revenue generation"""
        research_areas = len(proposal.get('research_areas', []))
        funding_mix = len(proposal.get('funding_sources', {}))
        
        # Score based on revenue factors
        research_score = min(research_areas * 0.2, 1.0)
        funding_score = min(funding_mix * 0.25, 1.0)
        
        return (research_score + funding_score) / 2

    def _identify_cost_reductions(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential cost reduction opportunities"""
        opportunities = []
        
        # Space optimization opportunities
        space_reqs = proposal.get('space_requirements', {})
        if space_reqs:
            opportunities.append({
                'area': 'space',
                'strategy': 'Shared facility usage',
                'potential_savings': 0.15
            })
        
        # Staffing optimization opportunities
        staffing = proposal.get('staffing', {})
        if staffing:
            opportunities.append({
                'area': 'staffing',
                'strategy': 'Phased hiring approach',
                'potential_savings': 0.20
            })
        
        # Funding optimization opportunities
        funding = proposal.get('funding_sources', {})
        if funding:
            opportunities.append({
                'area': 'funding',
                'strategy': 'Grant matching program',
                'potential_savings': 0.10
            })
        
        return opportunities

    def _evaluate_revenue_sustainability(self, proposal: Dict[str, Any]) -> float:
        """Evaluate sustainability of revenue streams"""
        funding_sources = proposal.get('funding_sources', {})
        if not funding_sources:
            return 0.5
        
        # Calculate sustainability score based on funding mix
        sustainability_weights = {
            'university': 0.9,
            'grants': 0.6,
            'industry': 0.7,
            'donations': 0.4
        }
        
        weighted_sum = sum(
            percentage * sustainability_weights.get(source.lower(), 0.5)
            for source, percentage in funding_sources.items()
        )
        
        return weighted_sum

    def _assess_cost_structure(self, proposal: Dict[str, Any]) -> float:
        """Assess the cost structure sustainability"""
        budget = proposal.get('budget', 0)
        if budget == 0:
            return 0.5
        
        # Calculate fixed vs variable costs ratio
        fixed_costs = sum(proposal.get('space_requirements', {}).values()) * 100  # $100 per sq ft
        staff_costs = sum(
            count * self._get_annual_cost(role)
            for role, count in proposal.get('staffing', {}).items()
        )
        
        total_costs = fixed_costs + staff_costs
        if total_costs == 0:
            return 0.5
        
        fixed_ratio = fixed_costs / total_costs
        # Prefer balanced cost structure (40-60% fixed costs)
        return 1 - abs(fixed_ratio - 0.5)

    def _get_annual_cost(self, role: str) -> float:
        """Get annual cost for different roles"""
        cost_map = {
            'faculty': 120000,
            'staff': 60000,
            'graduate_students': 30000
        }
        return cost_map.get(role, 50000) 