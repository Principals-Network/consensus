import asyncio
from src.orchestration.board_orchestrator import BoardOrchestrator

async def test_full_discussion():
    # Create test proposal
    proposal = {
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
        
        Expected Outcomes:
        - Leading research in AI ethics
        - Industry partnerships
        - Graduate program development
        - Policy recommendations
        """,
        'department': 'Computer Science',
        'budget': 5000000,
        'timeline': '3 years',
        'priority': 'high'
    }
    
    # Initialize orchestrator
    orchestrator = BoardOrchestrator()
    
    # Run discussion
    result = await orchestrator.initiate_discussion(proposal)
    
    # Print results
    print("\nDiscussion Results:")
    print(f"Consensus Score: {result['consensus_score']}")
    print("\nKey Disagreements:")
    for disagreement in result['key_disagreements']:
        print(f"- {disagreement['aspect']}: {disagreement['severity']}")
    
    print("\nSuggested Compromises:")
    for compromise in result['suggested_compromises']:
        print(f"- {compromise['description']}")
        print(f"  Likelihood: {compromise['acceptance_likelihood']}")

if __name__ == "__main__":
    asyncio.run(test_full_discussion()) 