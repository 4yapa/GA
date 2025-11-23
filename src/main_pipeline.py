"""
Main Pipeline for NER and Knowledge Graph Construction
Processes Reddit tariffs dataset and builds knowledge graph
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict
from collections import Counter
import sys

from custom_ner import CustomNER
from relation_extraction import RelationExtractor
from knowledge_graph import KnowledgeGraph
from visualization import KGVisualizer


class Pipeline:
    """Main processing pipeline"""

    def __init__(self, output_dir: str = "output"):
        self.ner = CustomNER()
        self.relation_extractor = RelationExtractor()
        self.kg = KnowledgeGraph()
        self.output_dir = output_dir

        # Create output directory
        os.makedirs(output_dir, exist_ok=True)

        # Statistics
        self.stats = {
            'total_posts_processed': 0,
            'total_entities_extracted': 0,
            'total_triples_extracted': 0,
            'entity_type_counts': Counter(),
            'relation_type_counts': Counter(),
            'posts_with_entities': 0,
            'posts_with_relations': 0,
        }

    def load_reddit_data(self, csv_path: str) -> List[Dict]:
        """Load Reddit posts from CSV file"""
        posts = []

        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    posts.append(row)

            print(f"Loaded {len(posts)} posts from {csv_path}")
            return posts

        except FileNotFoundError:
            print(f"Error: File not found: {csv_path}")
            return []
        except Exception as e:
            print(f"Error loading data: {e}")
            return []

    def process_text(self, text: str) -> Dict:
        """
        Process a single text to extract entities and relations

        Returns:
            Dictionary containing entities and triples
        """
        if not text or not isinstance(text, str):
            return {'entities': [], 'triples': []}

        # Extract entities with positions
        entities_with_pos = self.ner.extract_entities_with_positions(text)
        entities = self.ner.extract_entities(text)

        # Extract relations
        triples = self.relation_extractor.extract_relations(text)

        # If no explicit relations found, try simple co-occurrence
        if not triples and len(entities) >= 2:
            triples = self.relation_extractor.extract_simple_triples(text)

        return {
            'entities': entities,
            'entities_with_positions': entities_with_pos,
            'triples': triples
        }

    def process_posts(self, posts: List[Dict], limit: int = None) -> None:
        """
        Process Reddit posts to build knowledge graph

        Args:
            posts: List of post dictionaries
            limit: Maximum number of posts to process (None for all)
        """
        if limit:
            posts = posts[:limit]

        print(f"\nProcessing {len(posts)} posts...")
        print("=" * 60)

        for i, post in enumerate(posts):
            # Get text content
            text = post.get('text_content', '')
            if not text:
                continue

            # Process text
            result = self.process_text(text)

            entities = result['entities']
            triples = result['triples']

            # Update statistics
            self.stats['total_posts_processed'] += 1

            if entities:
                self.stats['posts_with_entities'] += 1
                self.stats['total_entities_extracted'] += len(entities)

                for entity_type, entity_text in entities:
                    self.stats['entity_type_counts'][entity_type] += 1

            if triples:
                self.stats['posts_with_relations'] += 1
                self.stats['total_triples_extracted'] += len(triples)

                # Add triples to knowledge graph
                for subject, predicate, obj in triples:
                    # Find entity types
                    subject_type = None
                    object_type = None

                    for etype, etext in entities:
                        if etext == subject:
                            subject_type = etype
                        if etext == obj:
                            object_type = etype

                    self.kg.add_triple(subject, predicate, obj, subject_type, object_type)
                    self.stats['relation_type_counts'][predicate] += 1

            # Progress indicator
            if (i + 1) % 50 == 0:
                print(f"Processed {i + 1}/{len(posts)} posts...")

        print(f"\nCompleted processing {self.stats['total_posts_processed']} posts")
        print(f"Extracted {self.stats['total_entities_extracted']} entities")
        print(f"Extracted {self.stats['total_triples_extracted']} triples")

    def generate_analysis_report(self) -> Dict:
        """Generate comprehensive analysis report"""

        print("\n" + "=" * 60)
        print("KNOWLEDGE GRAPH ANALYSIS REPORT")
        print("=" * 60)

        # Get KG statistics
        kg_stats = self.kg.get_statistics()

        report = {
            'timestamp': datetime.now().isoformat(),
            'processing_stats': dict(self.stats),
            'knowledge_graph_stats': kg_stats,
            'entity_types': dict(self.kg.get_entity_types_distribution()),
            'relation_types': dict(self.kg.get_relation_distribution()),
            'top_entities_by_degree': self.kg.get_top_entities(n=20, metric='degree'),
            'top_entities_by_pagerank': self.kg.get_top_entities(n=20, metric='pagerank'),
            'top_entities_by_betweenness': self.kg.get_top_entities(n=20, metric='betweenness'),
        }

        # Print summary
        print("\n1. PROCESSING STATISTICS")
        print("-" * 60)
        print(f"Total posts processed: {self.stats['total_posts_processed']}")
        print(f"Posts with entities: {self.stats['posts_with_entities']}")
        print(f"Posts with relations: {self.stats['posts_with_relations']}")
        print(f"Total entities extracted: {self.stats['total_entities_extracted']}")
        print(f"Total triples extracted: {self.stats['total_triples_extracted']}")

        print("\n2. KNOWLEDGE GRAPH STATISTICS")
        print("-" * 60)
        print(f"Number of nodes (entities): {kg_stats['num_nodes']}")
        print(f"Number of edges (relationships): {kg_stats['num_edges']}")
        print(f"Number of unique relation types: {kg_stats['num_relations']}")
        print(f"Graph density: {kg_stats['density']:.4f}")
        print(f"Number of weakly connected components: {kg_stats.get('num_weakly_connected_components', 'N/A')}")
        print(f"Largest component size: {kg_stats.get('largest_component_size', 'N/A')}")
        print(f"Average degree: {kg_stats.get('avg_degree', 0):.2f}")
        print(f"Average in-degree: {kg_stats.get('avg_in_degree', 0):.2f}")
        print(f"Average out-degree: {kg_stats.get('avg_out_degree', 0):.2f}")

        print("\n3. ENTITY TYPE DISTRIBUTION")
        print("-" * 60)
        entity_types = sorted(self.stats['entity_type_counts'].items(),
                              key=lambda x: x[1], reverse=True)
        for entity_type, count in entity_types:
            print(f"{entity_type:20s}: {count:5d}")

        print("\n4. RELATION TYPE DISTRIBUTION")
        print("-" * 60)
        relation_types = sorted(self.stats['relation_type_counts'].items(),
                                key=lambda x: x[1], reverse=True)
        for relation_type, count in relation_types:
            print(f"{relation_type:25s}: {count:5d}")

        print("\n5. TOP 20 ENTITIES BY DEGREE")
        print("-" * 60)
        for entity, degree in report['top_entities_by_degree']:
            print(f"{entity:30s}: {degree}")

        print("\n6. TOP 20 ENTITIES BY PAGERANK")
        print("-" * 60)
        for entity, score in report['top_entities_by_pagerank']:
            print(f"{entity:30s}: {score:.6f}")

        return report

    def save_results(self):
        """Save all results to files"""

        print("\n" + "=" * 60)
        print("SAVING RESULTS")
        print("=" * 60)

        # 1. Save knowledge graph
        kg_json_path = os.path.join(self.output_dir, "knowledge_graph.json")
        self.kg.save_graph(kg_json_path)
        print(f"✓ Knowledge graph saved to {kg_json_path}")

        # 2. Save triples as CSV
        triples_csv_path = os.path.join(self.output_dir, "triples.csv")
        self.kg.export_to_csv(triples_csv_path)
        print(f"✓ Triples exported to {triples_csv_path}")

        # 3. Save as RDF
        rdf_path = os.path.join(self.output_dir, "knowledge_graph.nt")
        self.kg.export_to_rdf(rdf_path)
        print(f"✓ RDF triples saved to {rdf_path}")

        # 4. Generate and save analysis report
        report = self.generate_analysis_report()
        report_path = os.path.join(self.output_dir, "analysis_report.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        print(f"✓ Analysis report saved to {report_path}")

        # 5. Create visualizations
        print("\nGenerating visualizations...")
        visualizer = KGVisualizer(self.kg)

        # Create visualizations directory
        viz_dir = os.path.join(os.path.dirname(self.output_dir), "visualizations")
        os.makedirs(viz_dir, exist_ok=True)

        try:
            # Graph visualization
            graph_viz_path = os.path.join(viz_dir, "knowledge_graph.png")
            visualizer.plot_graph(graph_viz_path, max_nodes=100, layout='spring')
            print(f"✓ Graph visualization saved to {graph_viz_path}")
        except Exception as e:
            print(f"✗ Could not create graph visualization: {e}")

        try:
            # Statistics visualization
            stats_viz_path = os.path.join(viz_dir, "statistics.png")
            visualizer.plot_statistics(stats_viz_path)
            print(f"✓ Statistics visualization saved to {stats_viz_path}")
        except Exception as e:
            print(f"✗ Could not create statistics visualization: {e}")

        try:
            # Relation network
            relation_viz_path = os.path.join(viz_dir, "relations.png")
            visualizer.plot_relation_network(relation_viz_path)
            print(f"✓ Relation visualization saved to {relation_viz_path}")
        except Exception as e:
            print(f"✗ Could not create relation visualization: {e}")

        print("\n" + "=" * 60)
        print("ALL RESULTS SAVED SUCCESSFULLY")
        print("=" * 60)

    def run(self, csv_path: str, limit: int = None):
        """
        Run the complete pipeline

        Args:
            csv_path: Path to Reddit posts CSV file
            limit: Maximum number of posts to process (None for all)
        """
        print("\n" + "=" * 60)
        print("STARTING NER AND KNOWLEDGE GRAPH PIPELINE")
        print("=" * 60)
        print(f"Input file: {csv_path}")
        print(f"Output directory: {self.output_dir}")

        # Load data
        posts = self.load_reddit_data(csv_path)

        if not posts:
            print("No posts to process. Exiting.")
            return

        # Process posts
        self.process_posts(posts, limit=limit)

        # Save results
        self.save_results()

        print("\n" + "=" * 60)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("=" * 60)


def main():
    """Main entry point"""

    # Get script directory and project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)

    # Default paths
    csv_path = os.path.join(project_root, "data", "reddit_posts.csv")
    output_dir = os.path.join(project_root, "output")

    # Check if CSV exists
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        print("Please place your reddit_posts.csv file in the data/ directory")
        print("Or download it from the Google Drive link provided in your report")
        return

    # Create and run pipeline
    pipeline = Pipeline(output_dir=output_dir)
    pipeline.run(csv_path, limit=None)  # Process all posts


if __name__ == "__main__":
    main()
