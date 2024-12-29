import asyncio
import streamlit as st
from datetime import datetime
from src.config.config_loader import ConfigLoader
from src.orchestration.board_orchestrator import BoardOrchestrator
from src.visualization.consensus_dashboard import ConsensusDashboard

async def test_consensus_system():
    # Sample proposal for testing
    test_proposal = {
        'title': 'New Research Center Establishment',
        'description': """
        Proposal to establish a new AI Ethics Research Center at the university.
        
        Budget: $5M over 3 years
        Space: 5000 sq ft in the Science Building
        Staff: 10 new faculty positions
        Impact: Cross-disciplinary research in AI ethics, policy, and social impact
        
        Key Components:
        1. Research laboratories
        2. Collaborative workspace
        3. Conference facilities
        4. Computing infrastructure
        """,
        'timestamp': str(datetime.now()),
        'status': 'submitted'
    }

    # Initialize the system
    config = ConfigLoader().get_ai_config()
    orchestrator = BoardOrchestrator()
    dashboard = ConsensusDashboard(config)

    # Process the proposal
    print("Starting discussion process...")
    discussion_result = await orchestrator.initiate_discussion(test_proposal)
    
    # Display results using Streamlit
    st.title("University Board Consensus System - Test Run")
    
    # Show proposal
    st.header("Proposal Under Discussion")
    st.write(test_proposal['title'])
    st.text_area("Description", test_proposal['description'], height=200)
    
    # Show results
    dashboard.render_dashboard(discussion_result)

if __name__ == "__main__":
    asyncio.run(test_consensus_system()) 