import asyncio
import logging
import streamlit as st
from src.config.config_loader import ConfigLoader
from src.orchestration.board_orchestrator import BoardOrchestrator
from src.visualization.consensus_visualizer import ConsensusVisualizer
from src.utils.logging import setup_logger

# Set up logging
logger = setup_logger("consensus_system", logging.DEBUG)

async def run_consensus_system():
    try:
        logger.info("Starting consensus system...")
        
        # Initialize system
        config = ConfigLoader().get_ai_config()
        orchestrator = BoardOrchestrator()
        visualizer = ConsensusVisualizer(config)

        # Create test proposal
        proposal = {
            'title': 'New AI Ethics Research Center',
            'description': """
            Proposal to establish a new AI Ethics Research Center at the university.
            
            Budget: $5M over 3 years
            Space: 5000 sq ft in the Science Building
            Staff: 10 new faculty positions
            Impact: Cross-disciplinary research in AI ethics, policy, and social impact
            """,
            'department': 'Computer Science',
            'budget': 5000000,
            'timeline': '3 years',
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
            },
            'research_areas': [
                'AI Ethics',
                'Policy Research',
                'Algorithmic Bias',
                'Privacy and Security'
            ]
        }

        # Run discussion
        result = await orchestrator.initiate_discussion(proposal)
        
        # Display results in Streamlit
        st.title("Board Discussion Results")

        # Show proposal details
        logger.info("Displaying proposal details...")
        with st.expander("Proposal Details", expanded=True):
            st.write(f"**Title:** {proposal['title']}")
            st.write(f"**Department:** {proposal['department']}")
            st.write(f"**Budget:** ${proposal['budget']:,}")
            st.write(f"**Timeline:** {proposal['timeline']}")
            st.write("**Description:**")
            st.write(proposal['description'])

        # Display results
        logger.info("Displaying discussion results...")
        try:
            st.header("Discussion Results")

            # Overview metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Consensus Score", f"{result['consensus_score']:.2f}")
            with col2:
                st.metric("Number of Clusters", len(result['opinion_clusters']))
            with col3:
                st.metric("Key Disagreements", len(result['key_disagreements']))

            # Agreement Network
            logger.debug("Creating agreement network visualization...")
            st.subheader("Agreement Network")
            network_fig = visualizer.create_agreement_network(result['opinion_clusters'])
            st.plotly_chart(network_fig, use_container_width=True)

            # Opinion Distribution
            logger.debug("Creating opinion distribution visualization...")
            st.subheader("Opinion Distribution")
            opinion_fig = visualizer.create_opinion_distribution(result['weighted_voting'])
            st.plotly_chart(opinion_fig, use_container_width=True)

            # Key Disagreements
            logger.debug("Displaying key disagreements...")
            st.subheader("Key Disagreements")
            for disagreement in result['key_disagreements']:
                with st.expander(f"Disagreement: {disagreement['aspect']}"):
                    st.write(f"**Severity:** {disagreement['severity']:.2f}")
                    st.write("**Positions:**")
                    for agent, position in disagreement['positions'].items():
                        st.write(f"- {agent}: {position}")

            # Suggested Compromises
            logger.debug("Displaying suggested compromises...")
            st.subheader("Suggested Compromises")
            for suggestion in result['suggested_compromises']:
                with st.expander(f"Compromise: {suggestion['description']}"):
                    st.write(f"**Supporting Agents:** {', '.join(suggestion['supporting_agents'])}")
                    st.write(f"**Expected Impact:** {suggestion['expected_impact']}")
                    st.progress(suggestion['acceptance_likelihood'])

            logger.info("Results displayed successfully")
            
        except Exception as e:
            logger.error(f"Error displaying results: {str(e)}", exc_info=True)
            st.error("An error occurred while displaying the results.")

    except Exception as e:
        logger.error(f"System error: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_consensus_system()) 