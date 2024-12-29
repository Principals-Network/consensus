from typing import Dict, List, Any
from src.agents.base import BoardAgent
import yaml
from src.utils.logging import setup_logger

class ResearchInnovationAgent(BoardAgent):
    def __init__(self, config: Dict[str, Any]):
        with open('src/prompts/research_innovation.yaml', 'r') as file:
            role_config = yaml.safe_load(file)
        
        super().__init__(
            role="Research and Innovation Officer",
            priorities=role_config['priorities'],
            config=config
        )
        self.prompts = role_config['prompts']
        self.evaluation_criteria = role_config['evaluation_criteria']
        self.logger = setup_logger(f"{__name__}.{self.__class__.__name__}")
    
    async def evaluate_proposal(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate proposals with focus on research and innovation impact"""
        try:
            evaluation = {
                'research_potential': await self._assess_research_potential(proposal),
                'innovation_impact': await self._assess_innovation_impact(proposal),
                'collaboration_opportunities': await self._assess_collaboration_opportunities(proposal),
                'knowledge_transfer': await self._assess_knowledge_transfer(proposal)
            }
            evaluation['overall_recommendation'] = self._generate_recommendation(evaluation)
            return evaluation
        except Exception as e:
            self.logger.error(f"Error in research evaluation: {str(e)}")
            return {
                'overall_recommendation': "Need More Information",
                'error': str(e)
            }

    async def _assess_research_potential(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess research potential and impact"""
        return {
            'research_alignment': self._evaluate_research_alignment(proposal),
            'funding_potential': await self._evaluate_grant_potential(proposal),
            'publication_potential': self._estimate_publication_potential(proposal),
            'research_infrastructure': self._assess_research_infrastructure(proposal)
        }
    
    async def _assess_innovation_impact(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess innovation and technological impact"""
        return {
            'innovation_level': self._evaluate_innovation_level(proposal),
            'market_relevance': self._assess_market_relevance(proposal),
            'technology_advancement': self._evaluate_tech_advancement(proposal),
            'commercialization_potential': self._assess_commercialization(proposal)
        }
    
    async def _assess_collaboration_opportunities(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential collaborations and partnerships"""
        return {
            'industry_partnerships': self._identify_industry_partners(proposal),
            'academic_collaborations': self._identify_academic_collaborations(proposal),
            'interdisciplinary_potential': self._evaluate_interdisciplinary_scope(proposal),
            'network_expansion': self._assess_network_growth(proposal)
        }
    
    async def _assess_knowledge_transfer(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Assess knowledge transfer and application potential"""
        return {
            'technology_transfer': self._evaluate_tech_transfer(proposal),
            'industry_application': self._assess_industry_application(proposal),
            'societal_impact': self._evaluate_societal_impact(proposal),
            'educational_benefits': self._assess_educational_benefits(proposal)
        }
    
    def _evaluate_research_alignment(self, proposal: Dict[str, Any]) -> float:
        """Evaluate alignment with university research priorities"""
        department = proposal.get('department', '')
        research_areas = proposal.get('research_areas', [])
        strategic_alignment = self._calculate_strategic_alignment(department, research_areas)
        return strategic_alignment
    
    async def _evaluate_grant_potential(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate potential for securing research grants"""
        try:
            funding_sources = proposal.get('funding_sources', {})
            opportunities = self._identify_grant_opportunities(proposal)
            success_prob = self._estimate_grant_success(proposal)
            potential_funding = self._estimate_potential_funding(proposal)
            
            return {
                'grant_opportunities': opportunities,
                'success_probability': success_prob,
                'potential_funding': potential_funding
            }
        except Exception as e:
            self.logger.error(f"Error evaluating grant potential: {str(e)}")
            return {
                'grant_opportunities': [],
                'success_probability': 0.5,
                'potential_funding': 0
            }
    
    def _generate_recommendation(self, evaluation: Dict[str, Any]) -> str:
        """Generate overall recommendation based on research and innovation analysis"""
        try:
            research_score = self._calculate_research_score(evaluation['research_potential'])
            innovation_score = self._calculate_innovation_score(evaluation['innovation_impact'])
            impact_score = self._calculate_impact_score(evaluation)
            
            total_score = (research_score + innovation_score + impact_score) / 3
            
            if total_score > 0.8:
                return "Strongly Support"
            elif total_score > 0.6:
                return "Support"
            elif total_score > 0.4:
                return "Support with Modifications"
            else:
                return "Need Major Revisions"
        except Exception as e:
            self.logger.error(f"Error generating recommendation: {str(e)}")
            return "Need More Information"
    
    def _calculate_research_score(self, research_potential: Dict[str, Any]) -> float:
        """Calculate overall research potential score"""
        weights = {
            'research_alignment': 0.3,
            'funding_potential': 0.3,
            'publication_potential': 0.2,
            'research_infrastructure': 0.2
        }
        
        return sum(
            weights[key] * self._normalize_score(value)
            for key, value in research_potential.items()
            if key in weights
        )
    
    def _calculate_innovation_score(self, innovation_impact: Dict[str, Any]) -> float:
        """Calculate overall innovation impact score"""
        weights = {
            'innovation_level': 0.3,
            'market_relevance': 0.2,
            'technology_advancement': 0.3,
            'commercialization_potential': 0.2
        }
        
        return sum(
            weights[key] * self._normalize_score(value)
            for key, value in innovation_impact.items()
            if key in weights
        )
    
    def _normalize_score(self, value: Any) -> float:
        """Normalize various score types to 0-1 range"""
        try:
            if isinstance(value, dict):
                # Handle dictionary values that might be lists or numbers
                scores = []
                for v in value.values():
                    if isinstance(v, (int, float)):
                        scores.append(v)
                    elif isinstance(v, list):
                        scores.extend([x for x in v if isinstance(x, (int, float))])
                    elif isinstance(v, dict):
                        scores.append(self._normalize_score(v))
                return sum(scores) / len(scores) if scores else 0.5
            elif isinstance(value, (int, float)):
                return min(max(value, 0), 1)
            elif isinstance(value, list):
                # Handle list values
                scores = [x for x in value if isinstance(x, (int, float))]
                return sum(scores) / len(scores) if scores else 0.5
            else:
                return 0.5  # Default for unhandled types
        except Exception as e:
            print(f"Warning: Error normalizing score: {e}")
            return 0.5
        
    async def generate_feedback(self, context: Dict[str, Any]) -> str:
        """Generate research-focused feedback"""
        try:
            return self._generate_structured_feedback(context)
        except Exception as e:
            self.logger.error(f"Error generating feedback: {str(e)}")
            return "Unable to generate feedback at this time."
        
    async def vote(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """Cast vote with research and innovation rationale"""
        evaluation = await self.evaluate_proposal(proposal)
        return self._make_vote_decision(evaluation)

    def _calculate_strategic_alignment(self, department: str, research_areas: List[str]) -> float:
        """Calculate alignment with strategic research priorities"""
        # Define strategic research priorities by department
        department_priorities = {
            'Computer Science': [
                'AI Ethics', 'Machine Learning', 'Cybersecurity',
                'Data Science', 'Software Engineering'
            ],
            'Engineering': [
                'Robotics', 'Sustainable Energy', 'Materials Science',
                'Bioengineering', 'Smart Systems'
            ],
            'Business': [
                'Digital Innovation', 'Entrepreneurship', 'Sustainable Business',
                'Finance Technology', 'Management Analytics'
            ]
        }
        
        # Get priorities for the department
        dept_priorities = department_priorities.get(department, [])
        if not dept_priorities:
            return 0.5  # Default alignment if department not found
        
        # Calculate alignment score
        matching_areas = sum(
            any(area.lower() in priority.lower() or priority.lower() in area.lower()
                for priority in dept_priorities)
            for area in research_areas
        )
        
        return min(matching_areas / len(dept_priorities), 1.0)

    def _identify_grant_opportunities(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential grant opportunities"""
        research_areas = proposal.get('research_areas', [])
        department = proposal.get('department', '')
        
        opportunities = []
        
        # Government grants
        if any('AI' in area or 'Ethics' in area for area in research_areas):
            opportunities.append({
                'source': 'NSF',
                'program': 'AI Research Initiatives',
                'potential_amount': 2000000,
                'probability': 0.7
            })
        
        # Industry partnerships
        if any('Innovation' in area or 'Technology' in area for area in research_areas):
            opportunities.append({
                'source': 'Industry Partners',
                'program': 'Tech Innovation Fund',
                'potential_amount': 1000000,
                'probability': 0.8
            })
        
        # Academic collaborations
        opportunities.append({
            'source': 'Inter-University Network',
            'program': 'Collaborative Research Grant',
            'potential_amount': 500000,
            'probability': 0.6
        })
        
        return opportunities

    def _estimate_grant_success(self, proposal: Dict[str, Any]) -> float:
        """Estimate probability of securing grants"""
        factors = {
            'research_strength': self._evaluate_research_strength(proposal),
            'team_expertise': self._evaluate_team_expertise(proposal),
            'innovation_level': self._evaluate_innovation_level(proposal),
            'infrastructure': self._evaluate_infrastructure_readiness(proposal)
        }
        
        weights = {
            'research_strength': 0.4,
            'team_expertise': 0.3,
            'innovation_level': 0.2,
            'infrastructure': 0.1
        }
        
        return sum(score * weights[factor] for factor, score in factors.items())

    def _evaluate_research_strength(self, proposal: Dict[str, Any]) -> float:
        """Evaluate strength of research proposal"""
        research_areas = proposal.get('research_areas', [])
        faculty = proposal.get('staffing', {}).get('faculty', 0)
        
        # Score based on research breadth and faculty strength
        research_breadth = min(len(research_areas) * 0.2, 1.0)
        faculty_strength = min(faculty * 0.1, 1.0)
        
        return (research_breadth + faculty_strength) / 2

    def _evaluate_team_expertise(self, proposal: Dict[str, Any]) -> float:
        """Evaluate research team expertise"""
        faculty = proposal.get('staffing', {}).get('faculty', 0)
        staff = proposal.get('staffing', {}).get('staff', 0)
        students = proposal.get('staffing', {}).get('graduate_students', 0)
        
        # Calculate team composition score
        team_size = faculty + staff + students
        if team_size == 0:
            return 0.5
        
        faculty_ratio = faculty / team_size
        return min(faculty_ratio + 0.3, 1.0)  # Value faculty presence but cap the score

    def _evaluate_innovation_level(self, proposal: Dict[str, Any]) -> float:
        """Evaluate innovation potential"""
        research_areas = proposal.get('research_areas', [])
        funding_mix = len(proposal.get('funding_sources', {}))
        
        # Innovation factors
        research_novelty = min(len(research_areas) * 0.15, 0.6)
        funding_diversity = min(funding_mix * 0.1, 0.4)
        
        return research_novelty + funding_diversity

    def _evaluate_infrastructure_readiness(self, proposal: Dict[str, Any]) -> float:
        """Evaluate infrastructure readiness"""
        space_reqs = proposal.get('space_requirements', {})
        
        # Calculate space readiness
        research_space = space_reqs.get('research_labs', 0)
        total_space = sum(space_reqs.values())
        
        if total_space == 0:
            return 0.5
        
        return min(research_space / total_space + 0.3, 1.0)

    def _estimate_potential_funding(self, proposal: Dict[str, Any]) -> float:
        """Estimate potential funding amount"""
        base_budget = proposal.get('budget', 0)
        opportunities = self._identify_grant_opportunities(proposal)
        
        potential_funding = sum(
            opp['potential_amount'] * opp['probability']
            for opp in opportunities
        )
        
        return potential_funding 

    def _estimate_publication_potential(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Estimate potential for academic publications"""
        research_areas = proposal.get('research_areas', [])
        faculty = proposal.get('staffing', {}).get('faculty', 0)
        grad_students = proposal.get('staffing', {}).get('graduate_students', 0)
        
        # Calculate potential based on team size and research areas
        team_size_score = min((faculty + grad_students * 0.5) / 10, 1.0)
        research_breadth = min(len(research_areas) * 0.2, 1.0)
        
        return {
            'annual_publications': team_size_score * 5,  # Estimated publications per year
            'quality_score': research_breadth * 0.8,     # Estimated publication quality
            'impact_potential': (team_size_score + research_breadth) / 2
        } 

    def _assess_research_infrastructure(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess research infrastructure requirements and readiness"""
        space_reqs = proposal.get('space_requirements', {})
        
        # Calculate infrastructure metrics
        research_space = space_reqs.get('research_labs', 0)
        total_space = sum(space_reqs.values())
        
        # Calculate space allocation score
        space_score = research_space / total_space if total_space > 0 else 0.5
        
        # Assess equipment and facilities
        equipment_score = self._assess_equipment_needs(proposal)
        facility_score = self._assess_facility_readiness(proposal)
        
        return {
            'space_adequacy': space_score,
            'equipment_readiness': equipment_score,
            'facility_readiness': facility_score,
            'overall_readiness': (space_score + equipment_score + facility_score) / 3
        }

    def _assess_equipment_needs(self, proposal: Dict[str, Any]) -> float:
        """Assess research equipment requirements"""
        research_areas = proposal.get('research_areas', [])
        
        # Base score on research complexity
        base_score = min(len(research_areas) * 0.2, 0.8)
        
        # Add bonus for technical areas
        tech_bonus = 0.2 if any(
            area.lower() in ['ai', 'machine learning', 'computing']
            for area in research_areas
        ) else 0
        
        return min(base_score + tech_bonus, 1.0)

    def _assess_facility_readiness(self, proposal: Dict[str, Any]) -> float:
        """Assess facility readiness for research activities"""
        space_reqs = proposal.get('space_requirements', {})
        
        # Calculate readiness based on space distribution
        lab_space = space_reqs.get('research_labs', 0)
        office_space = space_reqs.get('offices', 0)
        common_space = space_reqs.get('common_areas', 0)
        
        total_space = lab_space + office_space + common_space
        if total_space == 0:
            return 0.5
        
        # Ideal ratios: 50% labs, 30% offices, 20% common areas
        lab_ratio = lab_space / total_space
        office_ratio = office_space / total_space
        common_ratio = common_space / total_space
        
        # Calculate deviation from ideal ratios
        deviation = (
            abs(lab_ratio - 0.5) +
            abs(office_ratio - 0.3) +
            abs(common_ratio - 0.2)
        ) / 3
        
        return 1.0 - deviation 

    def _assess_market_relevance(self, proposal: Dict[str, Any]) -> float:
        """Assess market relevance and potential commercial impact"""
        research_areas = proposal.get('research_areas', [])
        funding_sources = proposal.get('funding_sources', {})
        
        # Calculate market relevance score
        industry_funding = funding_sources.get('industry', 0)
        market_oriented_areas = sum(
            1 for area in research_areas
            if any(term in area.lower() for term in 
                  ['ai', 'ethics', 'innovation', 'technology', 'application'])
        )
        
        # Combine factors
        industry_score = industry_funding * 2  # Weight industry funding
        area_score = min(market_oriented_areas * 0.2, 0.8)  # Cap area score
        
        return min((industry_score + area_score) / 2, 1.0) 

    def _evaluate_tech_advancement(self, proposal: Dict[str, Any]) -> float:
        """Evaluate technological advancement potential"""
        research_areas = proposal.get('research_areas', [])
        
        # Define tech advancement indicators
        tech_indicators = {
            'ai': 0.9,
            'machine learning': 0.85,
            'ethics': 0.7,
            'innovation': 0.8,
            'security': 0.75,
            'privacy': 0.75,
            'computing': 0.8,
            'technology': 0.7
        }
        
        # Calculate advancement score based on research areas
        advancement_scores = []
        for area in research_areas:
            area_lower = area.lower()
            matching_scores = [
                score for keyword, score in tech_indicators.items()
                if keyword in area_lower
            ]
            if matching_scores:
                advancement_scores.append(max(matching_scores))
        
        # Calculate final score
        if not advancement_scores:
            return 0.5  # Default score if no tech indicators found
        
        base_score = sum(advancement_scores) / len(advancement_scores)
        
        # Add bonus for interdisciplinary tech research
        unique_tech_areas = len(set(
            keyword for keyword in tech_indicators.keys()
            for area in research_areas
            if keyword in area.lower()
        ))
        interdisciplinary_bonus = min(unique_tech_areas * 0.1, 0.2)
        
        return min(base_score + interdisciplinary_bonus, 1.0) 

    def _assess_commercialization(self, proposal: Dict[str, Any]) -> float:
        """Assess potential for commercialization of research outcomes"""
        research_areas = proposal.get('research_areas', [])
        funding_sources = proposal.get('funding_sources', {})
        
        # Factors that indicate commercialization potential
        commercial_indicators = {
            'ai': 0.9,
            'technology': 0.8,
            'innovation': 0.85,
            'application': 0.8,
            'security': 0.75,
            'computing': 0.8,
            'ethics': 0.6  # Lower but still valuable for consulting/policy
        }
        
        # Calculate base commercialization score from research areas
        area_scores = []
        for area in research_areas:
            area_lower = area.lower()
            matching_scores = [
                score for keyword, score in commercial_indicators.items()
                if keyword in area_lower
            ]
            if matching_scores:
                area_scores.append(max(matching_scores))
        
        base_score = sum(area_scores) / len(area_scores) if area_scores else 0.5
        
        # Industry funding indicates commercial interest
        industry_funding = funding_sources.get('industry', 0)
        funding_score = min(industry_funding * 2, 1.0)  # Double industry funding percentage
        
        # Consider team composition
        team_score = self._assess_commercialization_team_strength(proposal)
        
        # Weight the factors
        weighted_score = (
            base_score * 0.4 +          # Research area relevance
            funding_score * 0.3 +       # Industry interest
            team_score * 0.3            # Team capability
        )
        
        return min(weighted_score, 1.0)

    def _assess_commercialization_team_strength(self, proposal: Dict[str, Any]) -> float:
        """Assess team's capability for commercialization"""
        staffing = proposal.get('staffing', {})
        
        # Calculate team composition scores
        faculty = staffing.get('faculty', 0)
        staff = staffing.get('staff', 0)
        students = staffing.get('graduate_students', 0)
        
        # Ideal ratios for commercialization
        total_team = faculty + staff + students
        if total_team == 0:
            return 0.5
        
        # Calculate scores based on team composition
        faculty_ratio = faculty / total_team
        staff_ratio = staff / total_team
        student_ratio = students / total_team
        
        # Ideal ratios: 30% faculty, 40% staff, 30% students
        composition_score = 1.0 - (
            abs(faculty_ratio - 0.3) +
            abs(staff_ratio - 0.4) +
            abs(student_ratio - 0.3)
        ) / 2
        
        return max(min(composition_score, 1.0), 0.0) 

    def _identify_industry_partners(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential industry partnership opportunities"""
        research_areas = proposal.get('research_areas', [])
        funding_sources = proposal.get('funding_sources', {})
        
        # Industry sectors interested in AI ethics
        industry_sectors = {
            'ai': {
                'sector': 'Tech Companies',
                'interest_level': 0.9,
                'potential_partners': ['Major Tech Firms', 'AI Startups'],
                'collaboration_areas': ['AI Ethics Guidelines', 'Bias Detection']
            },
            'ethics': {
                'sector': 'Consulting',
                'interest_level': 0.8,
                'potential_partners': ['Ethics Consultancies', 'Policy Think Tanks'],
                'collaboration_areas': ['Policy Development', 'Ethics Training']
            },
            'security': {
                'sector': 'Cybersecurity',
                'interest_level': 0.85,
                'potential_partners': ['Security Firms', 'Financial Institutions'],
                'collaboration_areas': ['Security Protocols', 'Risk Assessment']
            },
            'privacy': {
                'sector': 'Data Protection',
                'interest_level': 0.85,
                'potential_partners': ['Privacy Tech Companies', 'Legal Tech Firms'],
                'collaboration_areas': ['Privacy Tools', 'Compliance Solutions']
            }
        }
        
        # Identify relevant partnerships based on research areas
        partnerships = []
        for area in research_areas:
            area_lower = area.lower()
            for keyword, sector_info in industry_sectors.items():
                if keyword in area_lower:
                    partnership = sector_info.copy()
                    partnership['relevance'] = sector_info['interest_level']
                    partnership['funding_potential'] = funding_sources.get('industry', 0) * 1000000  # Convert to amount
                    partnerships.append(partnership)
        
        return partnerships

    def _identify_academic_collaborations(self, proposal: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Identify potential academic collaboration opportunities"""
        research_areas = proposal.get('research_areas', [])
        
        # Academic disciplines relevant to AI ethics
        academic_fields = {
            'ai': ['Computer Science', 'Data Science', 'Robotics'],
            'ethics': ['Philosophy', 'Law', 'Social Sciences'],
            'policy': ['Public Policy', 'Government', 'International Relations'],
            'security': ['Information Security', 'Risk Management'],
            'privacy': ['Law', 'Information Systems', 'Digital Rights']
        }
        
        collaborations = []
        for area in research_areas:
            area_lower = area.lower()
            for keyword, fields in academic_fields.items():
                if keyword in area_lower:
                    collaborations.append({
                        'field': fields,
                        'research_area': area,
                        'collaboration_type': 'Joint Research',
                        'potential_impact': 0.8,
                        'resource_sharing': True
                    })
        
        return collaborations

    def _evaluate_interdisciplinary_scope(self, proposal: Dict[str, Any]) -> float:
        """Evaluate potential for interdisciplinary research"""
        research_areas = proposal.get('research_areas', [])
        
        # Define discipline categories
        disciplines = {
            'technical': ['ai', 'computing', 'technology', 'data'],
            'social': ['ethics', 'policy', 'social', 'impact'],
            'business': ['innovation', 'market', 'industry'],
            'legal': ['compliance', 'regulation', 'privacy']
        }
        
        # Count unique discipline categories covered
        covered_disciplines = set()
        for area in research_areas:
            area_lower = area.lower()
            for category, keywords in disciplines.items():
                if any(keyword in area_lower for keyword in keywords):
                    covered_disciplines.add(category)
        
        # Calculate interdisciplinary score
        discipline_count = len(covered_disciplines)
        base_score = min(discipline_count / len(disciplines), 1.0)
        
        # Bonus for balanced coverage
        balance_score = len(covered_disciplines) / len(disciplines)
        
        return (base_score * 0.7 + balance_score * 0.3)

    def _assess_network_growth(self, proposal: Dict[str, Any]) -> Dict[str, float]:
        """Assess potential for research network growth"""
        industry_partners = self._identify_industry_partners(proposal)
        academic_collabs = self._identify_academic_collaborations(proposal)
        
        return {
            'industry_network': len(industry_partners) * 0.2,
            'academic_network': len(academic_collabs) * 0.15,
            'growth_potential': min(
                (len(industry_partners) + len(academic_collabs)) * 0.1,
                1.0
            )
        } 

    def _make_vote_decision(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Make voting decision based on evaluation results"""
        # Calculate weighted scores
        weights = {
            'research_potential': 0.3,
            'innovation_impact': 0.3,
            'collaboration_opportunities': 0.2,
            'knowledge_transfer': 0.2
        }
        
        scores = {}
        for aspect, weight in weights.items():
            if aspect in evaluation:
                aspect_scores = [
                    score for score in evaluation[aspect].values()
                    if isinstance(score, (int, float))
                ]
                scores[aspect] = sum(aspect_scores) / len(aspect_scores) if aspect_scores else 0.5
        
        total_score = sum(score * weights[aspect] for aspect, score in scores.items())
        
        # Determine vote and rationale
        if total_score > 0.8:
            vote = "support"
            rationale = "Strong research potential and innovation impact"
        elif total_score > 0.6:
            vote = "support"
            rationale = "Good potential with some areas for improvement"
        elif total_score > 0.4:
            vote = "abstain"
            rationale = "Mixed evaluation, needs significant revisions"
        else:
            vote = "oppose"
            rationale = "Insufficient research and innovation potential"
        
        # Identify key concerns
        concerns = []
        for aspect, score in scores.items():
            if score < 0.6:
                concerns.append(f"Low {aspect.replace('_', ' ')} score: {score:.2f}")
        
        # Generate suggestions
        suggestions = []
        if scores.get('research_potential', 0) < 0.7:
            suggestions.append("Strengthen research methodology and objectives")
        if scores.get('innovation_impact', 0) < 0.7:
            suggestions.append("Enhance innovation and technology transfer aspects")
        if scores.get('collaboration_opportunities', 0) < 0.7:
            suggestions.append("Develop more concrete collaboration plans")
        if scores.get('knowledge_transfer', 0) < 0.7:
            suggestions.append("Improve knowledge transfer mechanisms")
        
        return {
            'vote': vote,
            'rationale': rationale,
            'concerns': concerns,
            'suggestions': suggestions,
            'confidence': total_score
        } 

    def _generate_structured_feedback(self, context: Dict[str, Any]) -> str:
        """Generate structured feedback based on evaluation context"""
        try:
            evaluations = context.get('evaluations', [])
            consensus_analysis = context.get('consensus_analysis', {})
            
            feedback = []
            
            # Add research-focused feedback
            feedback.append("Research and Innovation Perspective:")
            
            # Comment on research potential
            research_potential = context.get('research_potential', {})
            if research_potential:
                score = self._normalize_score(research_potential)
                if score > 0.8:
                    feedback.append("- Strong research potential identified")
                elif score > 0.6:
                    feedback.append("- Good research foundation with room for enhancement")
                else:
                    feedback.append("- Research methodology needs strengthening")
            
            # Comment on innovation aspects
            innovation_impact = context.get('innovation_impact', {})
            if innovation_impact:
                score = self._normalize_score(innovation_impact)
                if score > 0.8:
                    feedback.append("- Excellent innovation potential")
                elif score > 0.6:
                    feedback.append("- Promising innovation aspects that could be expanded")
                else:
                    feedback.append("- Innovation components need more development")
            
            # Add collaboration suggestions
            feedback.append("\nCollaboration Opportunities:")
            industry_partners = self._identify_industry_partners(context.get('proposal', {}))
            academic_collabs = self._identify_academic_collaborations(context.get('proposal', {}))
            
            if industry_partners:
                feedback.append("- Potential industry partnerships identified:")
                for partner in industry_partners[:3]:  # Top 3 partners
                    feedback.append(f"  * {partner['sector']}: {', '.join(partner['collaboration_areas'])}")
            
            if academic_collabs:
                feedback.append("- Academic collaboration possibilities:")
                for collab in academic_collabs[:3]:  # Top 3 collaborations
                    feedback.append(f"  * {collab['field'][0]}: {collab['research_area']}")
            
            # Add recommendations
            feedback.append("\nRecommendations:")
            if context.get('consensus_analysis', {}).get('consensus_score', 1.0) < 0.7:
                feedback.append("- Consider strengthening interdisciplinary connections")
                feedback.append("- Develop more concrete collaboration plans")
                feedback.append("- Enhance innovation and technology transfer mechanisms")
            
            return "\n".join(feedback)
        except Exception as e:
            self.logger.error(f"Error generating structured feedback: {str(e)}")
            return "Error generating feedback. Please check the evaluation data."

    def _evaluate_tech_transfer(self, proposal: Dict[str, Any]) -> float:
        """Evaluate technology transfer potential"""
        research_areas = proposal.get('research_areas', [])
        funding_sources = proposal.get('funding_sources', {})
        
        # Define tech transfer indicators
        tech_transfer_potential = {
            'ai': 0.9,
            'technology': 0.85,
            'application': 0.8,
            'computing': 0.8,
            'security': 0.75,
            'innovation': 0.85
        }
        
        # Calculate base score from research areas
        area_scores = []
        for area in research_areas:
            area_lower = area.lower()
            matching_scores = [
                score for keyword, score in tech_transfer_potential.items()
                if keyword in area_lower
            ]
            if matching_scores:
                area_scores.append(max(matching_scores))
        
        base_score = sum(area_scores) / len(area_scores) if area_scores else 0.5
        
        # Industry funding indicates better tech transfer potential
        industry_funding = funding_sources.get('industry', 0)
        funding_score = min(industry_funding * 2, 1.0)
        
        # Weight the components
        return (base_score * 0.6 + funding_score * 0.4)

    def _assess_industry_application(self, proposal: Dict[str, Any]) -> float:
        """Assess potential for industry application"""
        research_areas = proposal.get('research_areas', [])
        
        # Define application-oriented keywords
        application_keywords = {
            'application': 1.0,
            'industry': 0.9,
            'practical': 0.8,
            'implementation': 0.8,
            'solution': 0.7
        }
        
        # Score based on application orientation
        area_scores = []
        for area in research_areas:
            area_lower = area.lower()
            matching_scores = [
                score for keyword, score in application_keywords.items()
                if keyword in area_lower
            ]
            if matching_scores:
                area_scores.append(max(matching_scores))
        
        return sum(area_scores) / len(area_scores) if area_scores else 0.5

    def _evaluate_societal_impact(self, proposal: Dict[str, Any]) -> float:
        """Evaluate potential societal impact"""
        research_areas = proposal.get('research_areas', [])
        
        # Define societal impact indicators
        impact_indicators = {
            'ethics': 1.0,
            'social': 0.9,
            'policy': 0.8,
            'public': 0.8,
            'impact': 0.7
        }
        
        # Calculate impact score
        area_scores = []
        for area in research_areas:
            area_lower = area.lower()
            matching_scores = [
                score for keyword, score in impact_indicators.items()
                if keyword in area_lower
            ]
            if matching_scores:
                area_scores.append(max(matching_scores))
        
        return sum(area_scores) / len(area_scores) if area_scores else 0.5

    def _assess_educational_benefits(self, proposal: Dict[str, Any]) -> float:
        """Assess educational benefits of knowledge transfer"""
        staffing = proposal.get('staffing', {})
        
        # Calculate educational impact factors
        students = staffing.get('graduate_students', 0)
        faculty = staffing.get('faculty', 0)
        
        # Score based on student involvement
        student_ratio = students / (faculty + 1)  # Add 1 to avoid division by zero
        student_score = min(student_ratio / 3, 1.0)  # Ideal ratio of 3 students per faculty
        
        # Consider research areas for educational value
        research_areas = proposal.get('research_areas', [])
        educational_score = min(len(research_areas) * 0.2, 1.0)
        
        return (student_score * 0.6 + educational_score * 0.4) 

    def _calculate_impact_score(self, evaluation: Dict[str, Any]) -> float:
        """Calculate overall impact score"""
        try:
            # Extract scores from evaluation
            collaboration_score = evaluation.get('collaboration_opportunities', {}).get('interdisciplinary_potential', 0.5)
            knowledge_transfer = evaluation.get('knowledge_transfer', {})
            societal_score = knowledge_transfer.get('societal_impact', 0.5)
            educational_score = knowledge_transfer.get('educational_benefits', 0.5)
            network_growth = evaluation.get('collaboration_opportunities', {}).get('network_expansion', {})
            
            # Weight the different impact factors
            weights = {
                'collaboration': 0.3,
                'societal': 0.3,
                'educational': 0.2,
                'network': 0.2
            }
            
            # Calculate weighted score
            impact_score = (
                collaboration_score * weights['collaboration'] +
                societal_score * weights['societal'] +
                educational_score * weights['educational'] +
                network_growth.get('growth_potential', 0.5) * weights['network']
            )
            
            return min(impact_score, 1.0)
        except Exception as e:
            self.logger.error(f"Error calculating impact score: {str(e)}")
            return 0.5 