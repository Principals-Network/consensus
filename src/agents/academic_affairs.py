from typing import Dict, List, Any
from src.agents.base import BoardAgent
import yaml

class AcademicAffairsAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/academic_affairs.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
        
        super().__init__(
            role="Academic Affairs Officer",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on academic impact"""
        # Gather all evaluations
        academic_quality = await self._assess_academic_quality(proposal)
        faculty_impact = await self._assess_faculty_impact(proposal)
        curriculum_alignment = await self._assess_curriculum_alignment(proposal)
        student_impact = await self._assess_student_impact(proposal)
        research_contribution = await self._assess_research_contribution(proposal)
        
        # Create evaluation dictionary
        evaluation = {
            'academic_quality': academic_quality,
            'faculty_impact': faculty_impact,
            'curriculum_alignment': curriculum_alignment,
            'student_impact': student_impact,
            'research_contribution': research_contribution
        }
        
        # Generate recommendation
        evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
        
        return evaluation
    
    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate academic perspective feedback"""
        prompt = self.prompts['feedback'].format(**context)
        response = await self.ai.generate_response(prompt, self.role, context)
        return response['content']
    
    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with academic rationale"""
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
    
    async def _assess_academic_quality(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess academic quality and standards"""
        prompt = self.prompts['academic_quality'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        return {
            'program_rigor': self._evaluate_program_rigor(proposal),
            'faculty_expertise': self._evaluate_faculty_expertise(proposal),
            'research_potential': self._evaluate_research_potential(proposal),
            'educational_innovation': self._evaluate_educational_innovation(proposal)
        }
    
    async def _assess_faculty_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess impact on faculty"""
        prompt = self.prompts['faculty_impact'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        return {
            'new_positions': proposal.get('staffing', {}).get('faculty', 0),
            'expertise_alignment': self._evaluate_expertise_alignment(proposal),
            'research_opportunities': self._evaluate_research_opportunities(proposal),
            'teaching_load': self._evaluate_teaching_load(proposal)
        }
    
    async def _assess_curriculum_alignment(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess alignment with existing curriculum"""
        prompt = self.prompts['curriculum_alignment'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        return {
            'program_fit': self._evaluate_curriculum_fit(proposal),
            'interdisciplinary_potential': self._evaluate_interdisciplinary_potential(proposal),
            'resource_utilization': self._evaluate_resource_utilization(proposal),
            'integration_feasibility': self._evaluate_integration_feasibility(proposal)
        }
    
    async def _assess_student_impact(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess impact on student experience and opportunities"""
        try:
            prompt = self.prompts['student_impact'].format(
                department=proposal.get('department', 'Not specified'),
                research_areas=proposal.get('research_areas', []),
                staffing={
                    'graduate_students': proposal.get('staffing', {}).get('graduate_students', 0)
                }
            )
            response = await self.ai.generate_response(prompt, self.role, proposal)
            
            # Calculate impact scores
            grad_students = proposal.get('staffing', {}).get('graduate_students', 0)
            research_areas = len(proposal.get('research_areas', []))
            
            return {
                'learning_opportunities': min(0.2 * research_areas, 1.0),
                'research_involvement': min(grad_students / 10, 1.0),
                'career_prospects': 0.8  # Base score for career impact
            }
        except KeyError as e:
            print(f"Warning: Missing key in proposal for student impact assessment: {e}")
            return {
                'learning_opportunities': 0.5,  # Default scores if data is missing
                'research_involvement': 0.5,
                'career_prospects': 0.5
            }
    
    async def _assess_research_contribution(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess contribution to research objectives"""
        prompt = self.prompts['research_contribution'].format(**proposal)
        response = await self.ai.generate_response(prompt, self.role, proposal)
        return {
            'research_output': 0.8,
            'funding_potential': 0.75,
            'collaboration_opportunities': 0.85
        }
    
    def _evaluate_program_rigor(self, proposal: Dict[str, Any]) -> float:
        """Evaluate academic rigor of proposed program"""
        # Implement scoring based on research areas, faculty qualifications, etc.
        research_areas = proposal.get('research_areas', [])
        faculty_count = proposal.get('staffing', {}).get('faculty', 0)
        
        # Score based on research depth and faculty resources
        research_score = min(len(research_areas) * 0.2, 1.0)
        faculty_score = min(faculty_count * 0.1, 1.0)
        
        return (research_score + faculty_score) / 2
    
    def _evaluate_faculty_expertise(self, proposal: Dict[str, Any]) -> float:
        """Evaluate available faculty expertise"""
        department = proposal.get('department', '')
        research_areas = proposal.get('research_areas', [])
        
        # Mock expertise evaluation
        expertise_coverage = 0.8  # Simulated expertise coverage
        return expertise_coverage
    
    def _evaluate_research_potential(self, proposal: Dict[str, Any]) -> float:
        """Evaluate research potential"""
        research_areas = proposal.get('research_areas', [])
        funding = proposal.get('funding_sources', {})
        
        # Score based on research areas and funding diversity
        research_breadth = min(len(research_areas) * 0.25, 1.0)
        funding_diversity = len(funding.keys()) * 0.3
        
        return (research_breadth + funding_diversity) / 2
    
    def _evaluate_educational_innovation(self, proposal: Dict[str, Any]) -> float:
        """Evaluate innovative aspects of educational program"""
        # Mock innovation score based on proposal components
        return 0.75  # Simulated innovation score
    
    def _evaluate_expertise_alignment(self, proposal: Dict[str, Any]) -> float:
        """Evaluate alignment with existing expertise"""
        department = proposal.get('department', '')
        research_areas = proposal.get('research_areas', [])
        
        # Mock alignment calculation
        return 0.8  # Simulated alignment score
    
    def _evaluate_research_opportunities(self, proposal: Dict[str, Any]) -> float:
        """Evaluate research opportunities"""
        funding = proposal.get('funding_sources', {}).get('grants', 0)
        research_areas = proposal.get('research_areas', [])
        
        # Score based on funding and research areas
        funding_score = min(funding * 2, 1.0)
        opportunity_score = min(len(research_areas) * 0.25, 1.0)
        
        return (funding_score + opportunity_score) / 2
    
    def _evaluate_teaching_load(self, proposal: Dict[str, Any]) -> float:
        """Evaluate teaching load implications"""
        faculty = proposal.get('staffing', {}).get('faculty', 0)
        students = proposal.get('staffing', {}).get('graduate_students', 0)
        
        # Calculate student-faculty ratio
        ratio = students / faculty if faculty > 0 else float('inf')
        
        # Score based on ratio (lower is better)
        return max(1.0 - (ratio / 20), 0.0)
    
    def _evaluate_curriculum_fit(self, proposal: Dict[str, Any]) -> float:
        """Evaluate how well the proposal fits with existing curriculum"""
        research_areas = proposal.get('research_areas', [])
        department = proposal.get('department', '')
        
        # Mock evaluation of curriculum fit
        base_score = 0.8  # Base fit score
        research_bonus = min(len(research_areas) * 0.05, 0.2)  # Bonus for research breadth
        
        return min(base_score + research_bonus, 1.0)
    
    def _evaluate_interdisciplinary_potential(self, proposal: Dict[str, Any]) -> float:
        """Evaluate potential for interdisciplinary collaboration"""
        research_areas = proposal.get('research_areas', [])
        
        # Score based on diversity of research areas
        return min(len(research_areas) * 0.2, 1.0)
    
    def _evaluate_resource_utilization(self, proposal: Dict[str, Any]) -> float:
        """Evaluate efficiency of resource utilization"""
        space_reqs = proposal.get('space_requirements', {})
        staffing = proposal.get('staffing', {})
        
        # Calculate space efficiency
        total_space = sum(space_reqs.values())
        space_per_person = total_space / (staffing.get('faculty', 1) + 
                                        staffing.get('staff', 0) +
                                        staffing.get('graduate_students', 0))
        
        # Score based on space efficiency (lower is better)
        space_score = max(1.0 - (space_per_person / 200), 0.0)  # Assume 200 sq ft per person is ideal
        
        return space_score
    
    def _evaluate_integration_feasibility(self, proposal: Dict[str, Any]) -> float:
        """Evaluate feasibility of integrating with existing programs"""
        timeline = float(proposal.get('timeline', '1').split()[0])  # Extract years
        
        # Score based on implementation timeline (shorter is better, but not too short)
        if timeline < 1:
            return 0.5  # Too rushed
        elif timeline <= 3:
            return 0.9  # Ideal timeline
        else:
            return max(1.0 - ((timeline - 3) * 0.1), 0.6)  # Penalty for longer timelines
    
    def _generate_recommendation(self, evaluation: Dict[str, Any]) -> str:
        """Generate overall recommendation based on academic analysis"""
        try:
            # Extract scores from evaluation components
            quality_scores = [
                score for score in evaluation['academic_quality'].values()
                if isinstance(score, (int, float))
            ]
            impact_scores = [
                score for score in evaluation['faculty_impact'].values()
                if isinstance(score, (int, float))
            ]
            alignment_scores = [
                score for score in evaluation['curriculum_alignment'].values()
                if isinstance(score, (int, float))
            ]
            
            # Calculate average scores
            quality_score = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
            impact_score = sum(impact_scores) / len(impact_scores) if impact_scores else 0.5
            alignment_score = sum(alignment_scores) / len(alignment_scores) if alignment_scores else 0.5
            
            # Calculate weighted total
            total_score = (
                quality_score * 0.4 +
                impact_score * 0.3 +
                alignment_score * 0.3
            )
            
            # Generate recommendation based on score
            if total_score > 0.8:
                return "Strongly Support"
            elif total_score > 0.6:
                return "Support with Minor Revisions"
            elif total_score > 0.4:
                return "Support with Major Revisions"
            else:
                return "Cannot Support - Academic Concerns"
            
        except Exception as e:
            print(f"Warning: Error generating recommendation: {e}")
            return "Need More Information"
    
    async def _assess_tracking_complexity(self, proposal: Dict[str, Any]) -> float:
        """Assess complexity of tracking requirements"""
        factors = {
            'timeline_length': float(proposal.get('timeline', '1').split()[0]),
            'stakeholder_count': len(proposal.get('staffing', {})),
            'research_areas': len(proposal.get('research_areas', [])),
            'funding_sources': len(proposal.get('funding_sources', {}))
        }
        
        # Calculate complexity score
        complexity = (
            0.3 * min(factors['timeline_length'] / 5, 1.0) +
            0.3 * min(factors['stakeholder_count'] / 10, 1.0) +
            0.2 * min(factors['research_areas'] / 5, 1.0) +
            0.2 * min(len(factors['funding_sources']) / 3, 1.0)
        )
        
        return complexity
    
    async def _develop_record_strategy(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Develop strategy for record keeping"""
        return {
            'documentation_level': 'detailed',
            'tracking_frequency': 'weekly',
            'required_reports': [
                'progress updates',
                'milestone reports',
                'budget tracking'
            ],
            'archival_requirements': {
                'retention_period': '7 years',
                'access_level': 'board members',
                'backup_frequency': 'daily'
            }
        }
    
    async def _identify_transparency_measures(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify measures for ensuring transparency"""
        return [
            {
                'measure': 'regular updates',
                'frequency': 'monthly',
                'audience': 'stakeholders',
                'format': 'written report'
            },
            {
                'measure': 'milestone reviews',
                'frequency': 'quarterly',
                'audience': 'board members',
                'format': 'presentation'
            },
            {
                'measure': 'public summaries',
                'frequency': 'semi-annual',
                'audience': 'public',
                'format': 'website update'
            }
        ] 