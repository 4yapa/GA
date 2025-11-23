"""
Knowledge Graph Visualization Module
Creates visual representations of the knowledge graph
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import Counter
from typing import Tuple
import networkx as nx
from knowledge_graph import KnowledgeGraph


class KGVisualizer:
    """Visualize Knowledge Graph"""

    def __init__(self, kg: KnowledgeGraph):
        self.kg = kg

    def plot_graph(self, output_path: str, max_nodes: int = 100,
                   layout: str = 'spring', figsize: Tuple[int, int] = (20, 16)):
        """
        Plot the knowledge graph

        Args:
            output_path: Path to save the figure
            max_nodes: Maximum number of nodes to display
            layout: Layout algorithm ('spring', 'circular', 'kamada_kawai')
            figsize: Figure size
        """
        G = self.kg.graph

        # If graph is too large, use subgraph of top entities
        if G.number_of_nodes() > max_nodes:
            top_entities = self.kg.get_top_entities(n=max_nodes, metric='degree')
            entity_names = [e for e, _ in top_entities]
            subgraph_kg = self.kg.get_subgraph(entity_names, max_depth=1)
            G = subgraph_kg.graph

        # Create figure
        plt.figure(figsize=figsize)

        # Choose layout
        if layout == 'spring':
            pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        elif layout == 'circular':
            pos = nx.circular_layout(G)
        elif layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(G)
        else:
            pos = nx.spring_layout(G, seed=42)

        # Color nodes by entity type
        entity_type_colors = {
            'PERSON': '#FF6B6B',
            'LOCATION': '#4ECDC4',
            'ORGANIZATION': '#45B7D1',
            'POLICY': '#FFA07A',
            'ECONOMIC_SECTOR': '#98D8C8',
            'MONEY': '#FFD700',
            'PERCENTAGE': '#F7DC6F',
            'TARIFF_RATE': '#F39C12',
            'DATE': '#BB8FCE',
            'PRODUCT': '#85C1E2',
            'UNKNOWN': '#BDC3C7'
        }

        node_colors = []
        for node in G.nodes():
            node_type = G.nodes[node].get('entity_type', 'UNKNOWN')
            node_colors.append(entity_type_colors.get(node_type, '#BDC3C7'))

        # Calculate node sizes based on degree
        degrees = dict(G.degree())
        max_degree = max(degrees.values()) if degrees else 1
        node_sizes = [300 + (degrees[node] / max_degree) * 1500 for node in G.nodes()]

        # Draw nodes
        nx.draw_networkx_nodes(G, pos,
                               node_color=node_colors,
                               node_size=node_sizes,
                               alpha=0.8,
                               edgecolors='black',
                               linewidths=1.5)

        # Draw edges with varying widths based on relation frequency
        edge_relations = [data.get('relation', '') for _, _, data in G.edges(data=True)]
        relation_counts = Counter(edge_relations)

        # Group edges by relation
        edges_by_relation = {}
        for u, v, data in G.edges(data=True):
            relation = data.get('relation', 'UNKNOWN')
            if relation not in edges_by_relation:
                edges_by_relation[relation] = []
            edges_by_relation[relation].append((u, v))

        # Draw edges for each relation type
        relation_colors = plt.cm.Set3.colors
        for i, (relation, edges) in enumerate(edges_by_relation.items()):
            color = relation_colors[i % len(relation_colors)]
            nx.draw_networkx_edges(G, pos,
                                   edgelist=edges,
                                   edge_color=[color] * len(edges),
                                   alpha=0.5,
                                   arrows=True,
                                   arrowsize=15,
                                   arrowstyle='->',
                                   width=1.5,
                                   connectionstyle='arc3,rad=0.1')

        # Draw labels
        labels = {node: node for node in G.nodes()}
        nx.draw_networkx_labels(G, pos,
                                labels=labels,
                                font_size=8,
                                font_weight='bold',
                                font_color='black')

        # Create legend for entity types
        legend_elements = []
        entity_types_in_graph = set(G.nodes[node].get('entity_type', 'UNKNOWN') for node in G.nodes())
        for entity_type in sorted(entity_types_in_graph):
            color = entity_type_colors.get(entity_type, '#BDC3C7')
            legend_elements.append(mpatches.Patch(color=color, label=entity_type))

        plt.legend(handles=legend_elements,
                   loc='upper left',
                   fontsize=10,
                   framealpha=0.9)

        plt.title('Knowledge Graph: Tariffs Discussion Network',
                  fontsize=18,
                  fontweight='bold',
                  pad=20)
        plt.axis('off')
        plt.tight_layout()

        # Save figure
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"Graph visualization saved to {output_path}")

    def plot_statistics(self, output_path: str, figsize: Tuple[int, int] = (16, 10)):
        """
        Plot statistics about the knowledge graph

        Args:
            output_path: Path to save the figure
            figsize: Figure size
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)

        # 1. Entity Type Distribution
        entity_types = self.kg.get_entity_types_distribution()
        if entity_types:
            axes[0, 0].bar(entity_types.keys(), entity_types.values(), color='skyblue', edgecolor='black')
            axes[0, 0].set_title('Entity Type Distribution', fontsize=14, fontweight='bold')
            axes[0, 0].set_xlabel('Entity Type', fontsize=11)
            axes[0, 0].set_ylabel('Count', fontsize=11)
            axes[0, 0].tick_params(axis='x', rotation=45)
            axes[0, 0].grid(axis='y', alpha=0.3)

        # 2. Relation Distribution
        relations = self.kg.get_relation_distribution()
        if relations:
            # Sort by frequency and take top 15
            sorted_relations = sorted(relations.items(), key=lambda x: x[1], reverse=True)[:15]
            rel_names = [r[0] for r in sorted_relations]
            rel_counts = [r[1] for r in sorted_relations]

            axes[0, 1].barh(rel_names, rel_counts, color='lightcoral', edgecolor='black')
            axes[0, 1].set_title('Top 15 Relation Types', fontsize=14, fontweight='bold')
            axes[0, 1].set_xlabel('Count', fontsize=11)
            axes[0, 1].set_ylabel('Relation', fontsize=11)
            axes[0, 1].grid(axis='x', alpha=0.3)
            axes[0, 1].invert_yaxis()

        # 3. Degree Distribution
        degrees = dict(self.kg.graph.degree())
        if degrees:
            degree_counts = Counter(degrees.values())
            sorted_degrees = sorted(degree_counts.items())

            axes[1, 0].bar([d[0] for d in sorted_degrees],
                           [d[1] for d in sorted_degrees],
                           color='lightgreen',
                           edgecolor='black')
            axes[1, 0].set_title('Degree Distribution', fontsize=14, fontweight='bold')
            axes[1, 0].set_xlabel('Degree', fontsize=11)
            axes[1, 0].set_ylabel('Number of Nodes', fontsize=11)
            axes[1, 0].grid(axis='y', alpha=0.3)

        # 4. Top Entities by PageRank
        top_entities = self.kg.get_top_entities(n=15, metric='pagerank')
        if top_entities:
            entity_names = [e[0] for e in top_entities]
            entity_scores = [e[1] for e in top_entities]

            axes[1, 1].barh(entity_names, entity_scores, color='plum', edgecolor='black')
            axes[1, 1].set_title('Top 15 Entities by PageRank', fontsize=14, fontweight='bold')
            axes[1, 1].set_xlabel('PageRank Score', fontsize=11)
            axes[1, 1].set_ylabel('Entity', fontsize=11)
            axes[1, 1].grid(axis='x', alpha=0.3)
            axes[1, 1].invert_yaxis()

        plt.suptitle('Knowledge Graph Statistics', fontsize=18, fontweight='bold', y=1.00)
        plt.tight_layout()

        # Save figure
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"Statistics visualization saved to {output_path}")

    def plot_relation_network(self, output_path: str, figsize: Tuple[int, int] = (14, 10)):
        """
        Plot a network showing only relations and their frequencies

        Args:
            output_path: Path to save the figure
            figsize: Figure size
        """
        relation_dist = self.kg.get_relation_distribution()

        if not relation_dist:
            print("No relations to plot")
            return

        # Sort by frequency
        sorted_relations = sorted(relation_dist.items(), key=lambda x: x[1], reverse=True)

        # Create bar chart
        plt.figure(figsize=figsize)

        relations = [r[0] for r in sorted_relations]
        counts = [r[1] for r in sorted_relations]

        bars = plt.barh(relations, counts, color='steelblue', edgecolor='black', linewidth=1.5)

        # Color bars by frequency
        colors = plt.cm.YlOrRd([c / max(counts) for c in counts])
        for bar, color in zip(bars, colors):
            bar.set_color(color)

        plt.xlabel('Frequency', fontsize=13, fontweight='bold')
        plt.ylabel('Relation Type', fontsize=13, fontweight='bold')
        plt.title('Distribution of Relations in Knowledge Graph',
                  fontsize=16,
                  fontweight='bold',
                  pad=15)
        plt.grid(axis='x', alpha=0.3, linestyle='--')
        plt.gca().invert_yaxis()

        # Add count labels on bars
        for i, (relation, count) in enumerate(sorted_relations):
            plt.text(count + max(counts) * 0.01, i, str(count),
                     va='center', fontsize=10, fontweight='bold')

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()

        print(f"Relation network visualization saved to {output_path}")


if __name__ == "__main__":
    from typing import Tuple
    # Test visualization
    kg = KnowledgeGraph()

    # Add test data
    test_triples = [
        ("Trump", "ANNOUNCES", "Tariff"),
        ("Trump", "TARGETS", "China"),
        ("China", "EXPORTS", "Steel"),
        ("Biden", "OPPOSES", "Tariff"),
        ("BBC", "REPORTS", "Trump"),
    ]

    for s, p, o in test_triples:
        kg.add_triple(s, p, o)

    visualizer = KGVisualizer(kg)

    print("Testing visualization...")
    # Note: These will only work if matplotlib is properly configured
    # visualizer.plot_graph('test_graph.png')
    # visualizer.plot_statistics('test_stats.png')
