import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any
import networkx as nx
import pandas as pd
from datetime import datetime

class ConsensusDashboard:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        
    def render_dashboard(self, analysis: Dict[str, Any]):
        """Render an interactive consensus analysis dashboard"""
        st.title("University Board Consensus Analysis Dashboard")
        
        # Overview metrics
        self._render_overview_metrics(analysis)
        
        # Main visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            self._render_agreement_network(analysis['opinion_clusters'])
            self._render_opinion_distribution(analysis['weighted_voting'])
        
        with col2:
            self._render_consensus_progress(analysis['consensus_score'])
            self._render_disagreement_analysis(analysis['key_disagreements'])
        
        # Detailed analysis sections
        st.header("Detailed Analysis")
        tabs = st.tabs(["Delphi Analysis", "Voting Analysis", "Compromise Suggestions"])
        
        with tabs[0]:
            self._render_delphi_analysis(analysis['delphi_analysis'])
        
        with tabs[1]:
            self._render_voting_analysis(analysis['weighted_voting'])
        
        with tabs[2]:
            self._render_compromise_suggestions(analysis['suggested_compromises'])
    
    def _render_overview_metrics(self, analysis: Dict[str, Any]):
        """Render overview metrics in cards"""
        cols = st.columns(4)
        
        with cols[0]:
            st.metric("Consensus Score", 
                     f"{analysis['consensus_score']:.2f}",
                     f"{analysis['consensus_score'] - 0.5:.2f}")
        
        with cols[1]:
            st.metric("Number of Clusters", 
                     len(analysis['opinion_clusters']))
        
        with cols[2]:
            st.metric("Key Disagreements", 
                     len(analysis['key_disagreements']))
        
        with cols[3]:
            st.metric("Discussion Round", 
                     analysis['delphi_analysis']['round_number'])
    
    def _render_agreement_network(self, clusters: Dict[str, Any]):
        """Render interactive agreement network"""
        st.subheader("Agreement Network")
        
        G = nx.Graph()
        
        # Add nodes and edges
        for cluster in clusters:
            for member in cluster['members']:
                G.add_node(member, group=cluster['id'])
                
        # Create edges between members of same cluster
        for cluster in clusters:
            members = cluster['members']
            for i, m1 in enumerate(members):
                for m2 in members[i+1:]:
                    G.add_edge(m1, m2, weight=cluster['cohesion'])
        
        # Create network layout
        pos = nx.spring_layout(G)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
            node_color.append(G.nodes[node]['group'])
            
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                color=node_color,
                size=20
            )
        )
        
        # Create edge trace
        edge_x = []
        edge_y = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                showlegend=False,
                hovermode='closest',
                margin=dict(b=0,l=0,r=0,t=0),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_consensus_progress(self, consensus_score: float):
        """Render consensus progress chart"""
        st.subheader("Consensus Progress")
        
        # Create a simple DataFrame with current score
        df = pd.DataFrame({
            'Round': [1],  # Current round
            'Score': [consensus_score]
        })
        
        fig = px.line(df, x='Round', y='Score',
                     title="Consensus Progress Over Time",
                     markers=True)  # Add markers for better visibility
        
        # Set axis ranges and labels
        fig.update_layout(
            xaxis_title="Discussion Round",
            yaxis_title="Consensus Score",
            yaxis_range=[0, 1],  # Consensus score is typically 0-1
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_delphi_analysis(self, delphi_data: Dict[str, Any]):
        """Render Delphi method analysis"""
        st.subheader("Delphi Analysis")
        
        # Convergence plot
        convergence_measure = delphi_data['analysis']['convergence_measure']
        if isinstance(convergence_measure, list):
            rounds = list(range(1, len(convergence_measure) + 1))
        else:
            rounds = [1]
            convergence_measure = [convergence_measure]
        
        convergence_data = pd.DataFrame({
            'Round': rounds,
            'Convergence': convergence_measure
        })
        
        fig = px.line(convergence_data, x='Round', y='Convergence',
                     title="Opinion Convergence in Delphi Rounds",
                     markers=True)  # Add markers for better visibility
        
        # Set axis ranges and labels
        fig.update_layout(
            xaxis_title="Discussion Round",
            yaxis_title="Convergence Score",
            yaxis_range=[0, 1],
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Key arguments and patterns
        col1, col2 = st.columns(2)
        with col1:
            st.write("Key Arguments")
            for arg in delphi_data['feedback']['key_arguments']:
                st.write(f"- {arg}")
        
        with col2:
            st.write("Emerging Patterns")
            for pattern in delphi_data['feedback']['emerging_patterns']:
                st.write(f"- {pattern}")
    
    def _render_voting_analysis(self, voting_data: Dict[str, Any]):
        """Render voting analysis section"""
        st.subheader("Voting Analysis")
        
        # Vote distribution
        vote_analysis = voting_data['vote_analysis']
        vote_data = [
            {'Vote': vote, 'Count': count}
            for vote, count in vote_analysis.items()
        ]
        vote_counts = pd.DataFrame(vote_data)
        
        fig = px.pie(vote_counts, values='Count', names='Vote',
                     title="Vote Distribution")
        st.plotly_chart(fig, use_container_width=True)
        
        # Weight distribution
        weight_data = pd.DataFrame([
            {'Agent': agent, 'Weight': weight}
            for agent, weight in voting_data['weight_distribution'].items()
        ])
        
        fig = px.bar(weight_data, x='Agent', y='Weight',
                     title="Agent Weight Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_compromise_suggestions(self, suggestions: List[Dict[str, Any]]):
        """Render compromise suggestions section"""
        st.subheader("Compromise Suggestions")
        
        for i, suggestion in enumerate(suggestions, 1):
            with st.expander(f"Suggestion {i}"):
                st.write("**Description:**", suggestion.get('description'))
                st.write("**Supporting Agents:**", ", ".join(suggestion.get('supporting_agents', [])))
                st.write("**Expected Impact:**", suggestion.get('expected_impact'))
                
                # Show acceptance likelihood
                acceptance = suggestion.get('acceptance_likelihood', 0)
                st.progress(acceptance)
                st.write(f"Acceptance Likelihood: {acceptance*100:.1f}%") 
    
    def _render_disagreement_analysis(self, disagreements: List[Dict[str, Any]]):
        """Render disagreement analysis section"""
        st.subheader("Key Disagreements")
        
        if not disagreements:
            st.write("No significant disagreements found.")
            return
            
        # Create disagreement heatmap
        disagreement_data = pd.DataFrame([
            {
                'Aspect': d['aspect'],
                'Severity': d['severity'],
                'Position Count': len(d['positions'])
            }
            for d in disagreements
        ])
        
        fig = px.imshow(
            disagreement_data.pivot(columns='Aspect', values='Severity'),
            title="Disagreement Severity Heatmap",
            color_continuous_scale="Reds"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Show detailed disagreement information
        for i, disagreement in enumerate(disagreements, 1):
            with st.expander(f"Disagreement {i}: {disagreement['aspect']}"):
                st.write("**Severity:**", f"{disagreement['severity']:.2f}")
                st.write("**Positions:**")
                for agent, position in disagreement['positions'].items():
                    st.write(f"- {agent}: {position}")
    
    def _render_opinion_distribution(self, voting_data: Dict[str, Any]):
        """Render opinion distribution visualization"""
        st.subheader("Opinion Distribution")
        
        # Create opinion distribution chart
        vote_analysis = voting_data['vote_analysis']
        opinions_data = [
            {'Opinion': opinion, 'Count': count}
            for opinion, count in vote_analysis.items()
        ]
        opinions = pd.DataFrame(opinions_data)
        
        fig = px.pie(
            opinions,
            values='Count',
            names='Opinion',
            title="Distribution of Opinions"
        )
        st.plotly_chart(fig, use_container_width=True) 