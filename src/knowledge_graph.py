"""
Knowledge Graph Construction and Analysis
Builds a knowledge graph from extracted triples
"""

import json
import pickle
from typing import List, Tuple, Dict, Set
from collections import defaultdict, Counter
import networkx as nx


class KnowledgeGraph:
    """
    Knowledge Graph representation using NetworkX
    Stores and analyzes entity-relation triples
    """

    def __init__(self):
        self.graph = nx.MultiDiGraph()  # Directed graph with multiple edges
        self.triples = []
        self.entity_types = {}  # Map entity to its type

    def add_triple(self, subject: str, predicate: str, obj: str,
                   subject_type: str = None, object_type: str = None):
        """
        Add a triple to the knowledge graph

        Args:
            subject: Subject entity
            predicate: Relation/predicate
            obj: Object entity
            subject_type: Type of subject entity (optional)
            object_type: Type of object entity (optional)
        """
        # Add nodes
        self.graph.add_node(subject, entity_type=subject_type or 'UNKNOWN')
        self.graph.add_node(obj, entity_type=object_type or 'UNKNOWN')

        # Add edge with relation as attribute
        self.graph.add_edge(subject, obj, relation=predicate)

        # Store triple
        self.triples.append((subject, predicate, obj))

        # Update entity types
        if subject_type:
            self.entity_types[subject] = subject_type
        if object_type:
            self.entity_types[obj] = object_type

    def add_triples_batch(self, triples: List[Tuple[str, str, str]]):
        """Add multiple triples at once"""
        for subject, predicate, obj in triples:
            self.add_triple(subject, predicate, obj)

    def get_statistics(self) -> Dict:
        """
        Compute statistics about the knowledge graph

        Returns:
            Dictionary containing graph statistics
        """
        stats = {
            'num_nodes': self.graph.number_of_nodes(),
            'num_edges': self.graph.number_of_edges(),
            'num_triples': len(self.triples),
            'num_relations': len(self.get_all_relations()),
            'density': nx.density(self.graph),
            'is_connected': nx.is_weakly_connected(self.graph),
        }

        # Component analysis
        if self.graph.number_of_nodes() > 0:
            num_components = nx.number_weakly_connected_components(self.graph)
            stats['num_weakly_connected_components'] = num_components

            # Largest component size
            largest_component = max(nx.weakly_connected_components(self.graph), key=len)
            stats['largest_component_size'] = len(largest_component)

        # Degree statistics
        if self.graph.number_of_nodes() > 0:
            degrees = dict(self.graph.degree())
            in_degrees = dict(self.graph.in_degree())
            out_degrees = dict(self.graph.out_degree())

            stats['avg_degree'] = sum(degrees.values()) / len(degrees)
            stats['max_degree'] = max(degrees.values())
            stats['avg_in_degree'] = sum(in_degrees.values()) / len(in_degrees)
            stats['avg_out_degree'] = sum(out_degrees.values()) / len(out_degrees)

        return stats

    def get_all_relations(self) -> Set[str]:
        """Get all unique relations in the graph"""
        relations = set()
        for _, _, data in self.graph.edges(data=True):
            relations.add(data.get('relation', 'UNKNOWN'))
        return relations

    def get_entity_types_distribution(self) -> Dict[str, int]:
        """Get distribution of entity types"""
        type_counts = Counter()
        for node, data in self.graph.nodes(data=True):
            entity_type = data.get('entity_type', 'UNKNOWN')
            type_counts[entity_type] += 1
        return dict(type_counts)

    def get_relation_distribution(self) -> Dict[str, int]:
        """Get distribution of relations"""
        relation_counts = Counter()
        for _, _, data in self.graph.edges(data=True):
            relation = data.get('relation', 'UNKNOWN')
            relation_counts[relation] += 1
        return dict(relation_counts)

    def get_top_entities(self, n: int = 10, metric: str = 'degree') -> List[Tuple[str, float]]:
        """
        Get top entities by various centrality metrics

        Args:
            n: Number of top entities to return
            metric: One of 'degree', 'in_degree', 'out_degree', 'pagerank', 'betweenness'

        Returns:
            List of (entity, score) tuples
        """
        if self.graph.number_of_nodes() == 0:
            return []

        if metric == 'degree':
            scores = dict(self.graph.degree())
        elif metric == 'in_degree':
            scores = dict(self.graph.in_degree())
        elif metric == 'out_degree':
            scores = dict(self.graph.out_degree())
        elif metric == 'pagerank':
            scores = nx.pagerank(self.graph)
        elif metric == 'betweenness':
            scores = nx.betweenness_centrality(self.graph)
        else:
            raise ValueError(f"Unknown metric: {metric}")

        # Sort by score
        sorted_entities = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_entities[:n]

    def get_neighbors(self, entity: str, direction: str = 'both') -> List[Tuple[str, str, str]]:
        """
        Get neighboring entities and their relations

        Args:
            entity: Target entity
            direction: 'in', 'out', or 'both'

        Returns:
            List of (relation, neighbor, direction) tuples
        """
        if entity not in self.graph:
            return []

        neighbors = []

        if direction in ['out', 'both']:
            for neighbor in self.graph.successors(entity):
                # Get all edges (in case of multiple relations)
                edges = self.graph.get_edge_data(entity, neighbor)
                for edge_data in edges.values():
                    relation = edge_data.get('relation', 'UNKNOWN')
                    neighbors.append((relation, neighbor, 'out'))

        if direction in ['in', 'both']:
            for neighbor in self.graph.predecessors(entity):
                edges = self.graph.get_edge_data(neighbor, entity)
                for edge_data in edges.values():
                    relation = edge_data.get('relation', 'UNKNOWN')
                    neighbors.append((relation, neighbor, 'in'))

        return neighbors

    def query_triples(self, subject: str = None, predicate: str = None, obj: str = None) -> List[Tuple[str, str, str]]:
        """
        Query triples matching the given pattern
        Use None as wildcard

        Args:
            subject: Subject to match (or None for any)
            predicate: Predicate to match (or None for any)
            obj: Object to match (or None for any)

        Returns:
            List of matching triples
        """
        results = []

        for s, p, o in self.triples:
            if subject is not None and s != subject:
                continue
            if predicate is not None and p != predicate:
                continue
            if obj is not None and o != obj:
                continue

            results.append((s, p, o))

        return results

    def save_graph(self, filepath: str):
        """Save graph to file"""
        data = {
            'triples': self.triples,
            'entity_types': self.entity_types
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load_graph(self, filepath: str):
        """Load graph from file"""
        with open(filepath, 'r') as f:
            data = json.load(f)

        self.triples = data['triples']
        self.entity_types = data.get('entity_types', {})

        # Rebuild graph
        self.graph = nx.MultiDiGraph()
        for subject, predicate, obj in self.triples:
            self.add_triple(
                subject, predicate, obj,
                self.entity_types.get(subject),
                self.entity_types.get(obj)
            )

    def save_networkx(self, filepath: str):
        """Save NetworkX graph object"""
        with open(filepath, 'wb') as f:
            pickle.dump(self.graph, f)

    def export_to_csv(self, filepath: str):
        """Export triples to CSV"""
        import csv

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Subject', 'Predicate', 'Object'])
            for subject, predicate, obj in self.triples:
                writer.writerow([subject, predicate, obj])

    def export_to_rdf(self, filepath: str, namespace: str = "http://tariffs.kg/"):
        """Export to RDF N-Triples format"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for subject, predicate, obj in self.triples:
                # Create URIs
                subj_uri = f"<{namespace}{subject.replace(' ', '_')}>"
                pred_uri = f"<{namespace}{predicate}>"
                obj_uri = f"<{namespace}{obj.replace(' ', '_')}>"

                # Write N-Triple
                f.write(f"{subj_uri} {pred_uri} {obj_uri} .\n")

    def get_subgraph(self, entities: List[str], max_depth: int = 1) -> 'KnowledgeGraph':
        """
        Extract a subgraph containing specified entities and their neighbors

        Args:
            entities: List of entity names
            max_depth: Maximum distance from seed entities

        Returns:
            New KnowledgeGraph containing the subgraph
        """
        # Find all nodes within max_depth
        nodes_to_include = set(entities)

        for entity in entities:
            if entity not in self.graph:
                continue

            # BFS to find neighbors
            visited = {entity}
            queue = [(entity, 0)]

            while queue:
                node, depth = queue.pop(0)

                if depth >= max_depth:
                    continue

                # Add neighbors
                for neighbor in self.graph.neighbors(node):
                    nodes_to_include.add(neighbor)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))

                # Add predecessors too
                for neighbor in self.graph.predecessors(node):
                    nodes_to_include.add(neighbor)
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))

        # Create subgraph
        subgraph_kg = KnowledgeGraph()

        for s, p, o in self.triples:
            if s in nodes_to_include and o in nodes_to_include:
                subgraph_kg.add_triple(
                    s, p, o,
                    self.entity_types.get(s),
                    self.entity_types.get(o)
                )

        return subgraph_kg


if __name__ == "__main__":
    # Test the knowledge graph
    kg = KnowledgeGraph()

    # Add some test triples
    test_triples = [
        ("Trump", "ANNOUNCES", "25% tariff"),
        ("Trump", "TARGETS", "China"),
        ("China", "EXPORTS", "Steel"),
        ("BBC", "REPORTS", "Trump"),
        ("25% tariff", "IMPACTS", "Manufacturing"),
    ]

    print("Testing Knowledge Graph\n" + "="*50)
    print("\nAdding triples...")
    for s, p, o in test_triples:
        kg.add_triple(s, p, o)
        print(f"  Added: ({s}, {p}, {o})")

    # Get statistics
    print("\nGraph Statistics:")
    stats = kg.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Get top entities
    print("\nTop Entities (by degree):")
    top_entities = kg.get_top_entities(n=5, metric='degree')
    for entity, score in top_entities:
        print(f"  {entity}: {score}")

    # Query triples
    print("\nTriples involving 'Trump':")
    trump_triples = kg.query_triples(subject="Trump")
    for s, p, o in trump_triples:
        print(f"  ({s}, {p}, {o})")
