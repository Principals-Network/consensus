from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import pandas as pd
import numpy as np
from datetime import datetime

class ConsensusVisualizer:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.color_scheme = {
            'support': '#2ecc71',
            'oppose': '#e74c3c',
            'abstain': '#95a5a6',
            'background': '#f8f9fa',
            'text': '#2c3e50'
        }
    
    def create_agreement_network(self, clusters: List[Dict[str, Any]]) -> go.Figure:
        """Create interactive network visualization of agent agreements"""
        G = nx.Graph()
        
        # Add nodes and edges from clusters
        for cluster in clusters:
            members = cluster['members']
            # Add nodes
            for member in members:
                G.add_node(member, cluster=cluster['id'])
            # Add edges between all members in cluster
            for i, m1 in enumerate(members):
                for m2 in members[i+1:]:
                    G.add_edge(m1, m2, weight=cluster['cohesion'])
        
        # Calculate layout
        pos = nx.spring_layout(G)
        
        # Create edge trace
        edge_x = []
        edge_y = []
        edge_weights = []
        
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_weights.append(edge[2]['weight'])
        
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=1, color='#888'),
            hoverinfo='none',
            mode='lines'
        )
        
        # Create node trace
        node_x = []
        node_y = []
        node_colors = []
        node_text = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_colors.append(G.nodes[node]['cluster'])
            node_text.append(f"Agent: {node}")
        
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            textposition="top center",
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                size=20,
                color=node_colors,
                line_width=2
            )
        )
        
        # Create figure
        fig = go.Figure(
            data=[edge_trace, node_trace],
            layout=go.Layout(
                title='Agreement Network',
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                plot_bgcolor=self.color_scheme['background'],
                paper_bgcolor=self.color_scheme['background'],
                font=dict(color=self.color_scheme['text'])
            )
        )
        
        return fig
    
    def create_opinion_distribution(self, voting_data: Dict[str, Any]) -> go.Figure:
        """Create visualization of opinion distribution"""
        vote_counts = pd.DataFrame([
            {'Vote': vote, 'Count': count}
            for vote, count in voting_data['vote_analysis'].items()
        ])
        
        fig = px.pie(
            vote_counts,
            values='Count',
            names='Vote',
            title='Opinion Distribution',
            color='Vote',
            color_discrete_map={
                'support': self.color_scheme['support'],
                'oppose': self.color_scheme['oppose'],
                'abstain': self.color_scheme['abstain']
            }
        )
        
        fig.update_layout(
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font=dict(color=self.color_scheme['text'])
        )
        
        return fig
    
    def create_consensus_progress(self, 
                                consensus_history: List[float],
                                rounds: List[int]) -> go.Figure:
        """Create visualization of consensus progress over time"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=rounds,
            y=consensus_history,
            mode='lines+markers',
            name='Consensus Score',
            line=dict(color=self.color_scheme['support']),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Consensus Progress Over Time',
            xaxis_title='Discussion Round',
            yaxis_title='Consensus Score',
            yaxis=dict(range=[0, 1]),
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font=dict(color=self.color_scheme['text'])
        )
        
        return fig
    
    def create_disagreement_heatmap(self, 
                                  disagreements: List[Dict[str, Any]]) -> go.Figure:
        """Create heatmap visualization of disagreements"""
        # Prepare data
        aspects = [d['aspect'] for d in disagreements]
        severities = [d['severity'] for d in disagreements]
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=[severities],
            x=aspects,
            colorscale='RdYlGn_r',
            showscale=True
        ))
        
        fig.update_layout(
            title='Disagreement Severity Heatmap',
            xaxis_title='Aspects',
            yaxis_showticklabels=False,
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font=dict(color=self.color_scheme['text'])
        )
        
        return fig
    
    def create_agent_influence(self, 
                             weight_distribution: Dict[str, float]) -> go.Figure:
        """Create visualization of agent influence/weights"""
        agents = list(weight_distribution.keys())
        weights = list(weight_distribution.values())
        
        fig = go.Figure(data=[
            go.Bar(
                x=agents,
                y=weights,
                marker_color=self.color_scheme['support']
            )
        ])
        
        fig.update_layout(
            title='Agent Influence Distribution',
            xaxis_title='Agents',
            yaxis_title='Influence Weight',
            plot_bgcolor=self.color_scheme['background'],
            paper_bgcolor=self.color_scheme['background'],
            font=dict(color=self.color_scheme['text'])
        )
        
        return fig 