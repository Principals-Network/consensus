import asyncio
import logging
from src.utils.logging import setup_logger
from src.orchestration.board_orchestrator import BoardOrchestrator
from src.visualization.consensus_dashboard import ConsensusDashboard
import streamlit as st

logger = setup_logger("discussion_runner")

async def run_discussion():
    # Create test proposal
    proposal = {
        'title': 'New Research Center Establishment',
        'description': """
        Proposal to establish a new AI Ethics Research Center at the university.
        
        Budget: $5M over 3 years
        Space: 5000 sq ft in the Science Building
        Staff: 10 new faculty positions
        Impact: Cross-disciplinary research in AI ethics, policy, and social impact
        """,
        'budget': 5000000,
        'timeline': '3 years',
        'department': 'Computer Science',
        'space_requirements': {
            'research_labs': 2000,
            'offices': 2000,
            'common_areas': 1000
        },
        'staffing': {
            'faculty': 10,
            'staff': 5,
            'graduate_students': 15
        },
        'funding_sources': {
            'university': 0.4,
            'grants': 0.4,
            'industry': 0.2
        }
    }

    # Initialize orchestrator
    orchestrator = BoardOrchestrator()
    
    # Run discussion
    logger.info("Starting board discussion...")
    result = await orchestrator.initiate_discussion(proposal)
    
    # Display results
    st.title("Board Discussion Results")
    
    # Overview
    st.header("Discussion Overview")
    st.metric("Consensus Score", f"{result['consensus_score']:.2f}")
    
    # Voting Results
    st.header("Voting Results")
    vote_analysis = result['weighted_voting']['vote_analysis']
    st.write(f"Support: {vote_analysis['support']}")
    st.write(f"Oppose: {vote_analysis['oppose']}")
    st.write(f"Abstain: {vote_analysis['abstain']}")
    
    # Key Disagreements
    st.header("Key Disagreements")
    for disagreement in result['key_disagreements']:
        st.write(f"**{disagreement['aspect']}**")
        st.write(f"Severity: {disagreement['severity']:.2f}")
        st.write("Positions:")
        for agent, position in disagreement['positions'].items():
            st.write(f"- {agent}: {position}")
            
    # Suggested Compromises
    st.header("Suggested Compromises")
    for suggestion in result['suggested_compromises']:
        st.write(f"**{suggestion['description']}**")
        st.write(f"Supporting Agents: {', '.join(suggestion['supporting_agents'])}")
        st.write(f"Expected Impact: {suggestion['expected_impact']}")
        st.progress(suggestion['acceptance_likelihood'])

if __name__ == "__main__":
    asyncio.run(run_discussion()) 