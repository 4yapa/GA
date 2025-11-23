"""
Relation Extraction Module
Extracts relationships between entities to form triples
Built from scratch without using pretrained models
"""

import re
from typing import List, Tuple, Set
from custom_ner import CustomNER


class RelationExtractor:
    """
    Rule-based relation extraction system
    Identifies relationships between entities to form (subject, predicate, object) triples
    """

    def __init__(self):
        self.ner = CustomNER()
        self.relation_patterns = self._build_relation_patterns()

    def _build_relation_patterns(self) -> List[dict]:
        """
        Build patterns for relation extraction
        Each pattern contains entity types and connecting words/phrases
        """

        patterns = [
            # ANNOUNCES patterns
            {
                'subject_types': ['PERSON', 'ORGANIZATION', 'LOCATION'],
                'predicate': 'ANNOUNCES',
                'object_types': ['POLICY', 'TARIFF_RATE', 'MONEY', 'PERCENTAGE'],
                'connecting_words': [
                    r'announce[sd]?',
                    r'propose[sd]?',
                    r'introduce[sd]?',
                    r'implement[sd]?',
                    r'impose[sd]?',
                    r'declare[sd]?'
                ]
            },

            # INCREASES/DECREASES patterns
            {
                'subject_types': ['PERSON', 'ORGANIZATION', 'LOCATION'],
                'predicate': 'INCREASES',
                'object_types': ['TARIFF_RATE', 'PERCENTAGE', 'MONEY'],
                'connecting_words': [
                    r'increase[sd]?',
                    r'raise[sd]?',
                    r'boost[sd]?',
                    r'hike[sd]?',
                    r'up',
                    r'raise[sd]?'
                ]
            },

            {
                'subject_types': ['PERSON', 'ORGANIZATION', 'LOCATION'],
                'predicate': 'DECREASES',
                'object_types': ['TARIFF_RATE', 'PERCENTAGE', 'MONEY'],
                'connecting_words': [
                    r'decrease[sd]?',
                    r'reduce[sd]?',
                    r'lower[sd]?',
                    r'cut[s]?',
                    r'slash(?:es)?',
                    r'drop[s]?'
                ]
            },

            # REPORTS patterns
            {
                'subject_types': ['ORGANIZATION'],
                'predicate': 'REPORTS',
                'object_types': ['POLICY', 'PERSON', 'LOCATION', 'ORGANIZATION'],
                'connecting_words': [
                    r'report[sd]?',
                    r'state[sd]?',
                    r'announce[sd]?',
                    r'say[s]?',
                    r'claim[sd]?',
                    r'indicate[sd]?'
                ]
            },

            # TRADES_WITH patterns
            {
                'subject_types': ['LOCATION', 'ORGANIZATION'],
                'predicate': 'TRADES_WITH',
                'object_types': ['LOCATION', 'ORGANIZATION'],
                'connecting_words': [
                    r'trade[sd]?\s+with',
                    r'trading\s+with',
                    r'export[sd]?\s+to',
                    r'import[sd]?\s+from',
                    r'deal[s]?\s+with'
                ]
            },

            # IMPACTS patterns
            {
                'subject_types': ['POLICY', 'TARIFF_RATE', 'PERSON'],
                'predicate': 'IMPACTS',
                'object_types': ['ECONOMIC_SECTOR', 'LOCATION', 'ORGANIZATION', 'PRODUCT'],
                'connecting_words': [
                    r'impact[sd]?',
                    r'affect[sd]?',
                    r'influence[sd]?',
                    r'hurt[s]?',
                    r'harm[s]?',
                    r'damage[sd]?',
                    r'benefit[s]?',
                    r'help[s]?'
                ]
            },

            # SUPPORTS/OPPOSES patterns
            {
                'subject_types': ['PERSON', 'ORGANIZATION', 'LOCATION'],
                'predicate': 'SUPPORTS',
                'object_types': ['POLICY', 'PERSON'],
                'connecting_words': [
                    r'support[s]?',
                    r'back[s]?',
                    r'endorse[sd]?',
                    r'favor[s]?',
                    r'promote[sd]?',
                    r'champion[s]?'
                ]
            },

            {
                'subject_types': ['PERSON', 'ORGANIZATION', 'LOCATION'],
                'predicate': 'OPPOSES',
                'object_types': ['POLICY', 'PERSON'],
                'connecting_words': [
                    r'oppose[sd]?',
                    r'against',
                    r'reject[sd]?',
                    r'resist[s]?',
                    r'fight[s]?',
                    r'criticize[sd]?',
                    r'condemn[s]?'
                ]
            },

            # NEGOTIATES patterns
            {
                'subject_types': ['PERSON', 'LOCATION', 'ORGANIZATION'],
                'predicate': 'NEGOTIATES',
                'object_types': ['POLICY', 'PERSON', 'LOCATION'],
                'connecting_words': [
                    r'negotiate[sd]?',
                    r'discuss(?:es)?',
                    r'talk[s]?\s+with',
                    r'meet[s]?\s+with',
                    r'negotiating\s+with'
                ]
            },

            # TARGETS patterns
            {
                'subject_types': ['POLICY', 'TARIFF_RATE', 'PERSON'],
                'predicate': 'TARGETS',
                'object_types': ['LOCATION', 'PRODUCT', 'ECONOMIC_SECTOR', 'ORGANIZATION'],
                'connecting_words': [
                    r'target[s]?',
                    r'aim[s]?\s+at',
                    r'focus(?:es)?\s+on',
                    r'directed\s+at',
                    r'against'
                ]
            },

            # LEADS patterns
            {
                'subject_types': ['PERSON'],
                'predicate': 'LEADS',
                'object_types': ['ORGANIZATION', 'LOCATION'],
                'connecting_words': [
                    r'lead[s]?',
                    r'head[s]?',
                    r'run[s]?',
                    r'president\s+of',
                    r'leader\s+of',
                    r'prime\s+minister\s+of'
                ]
            },

            # EXPORTS/IMPORTS patterns
            {
                'subject_types': ['LOCATION', 'ORGANIZATION'],
                'predicate': 'EXPORTS',
                'object_types': ['PRODUCT', 'ECONOMIC_SECTOR', 'MONEY'],
                'connecting_words': [
                    r'export[s]?',
                    r'sell[s]?',
                    r'ship[s]?',
                    r'send[s]?'
                ]
            },

            {
                'subject_types': ['LOCATION', 'ORGANIZATION'],
                'predicate': 'IMPORTS',
                'object_types': ['PRODUCT', 'ECONOMIC_SECTOR', 'MONEY'],
                'connecting_words': [
                    r'import[s]?',
                    r'buy[s]?',
                    r'purchase[s]?',
                    r'receive[s]?'
                ]
            },
        ]

        return patterns

    def _find_connecting_phrase(self, text: str, start_pos: int, end_pos: int,
                                  connecting_words: List[str]) -> Tuple[bool, str]:
        """
        Check if there's a connecting phrase between two entity positions

        Returns:
            (found, matching_phrase) tuple
        """
        middle_text = text[start_pos:end_pos].lower()

        for pattern_str in connecting_words:
            pattern = re.compile(pattern_str, re.IGNORECASE)
            if pattern.search(middle_text):
                return True, pattern_str

        return False, ""

    def extract_relations(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract relations from text

        Args:
            text: Input text

        Returns:
            List of (subject, predicate, object) triples
        """
        if not text or not isinstance(text, str):
            return []

        # Extract entities with positions
        entities = self.ner.extract_entities_with_positions(text)

        if len(entities) < 2:
            return []

        triples = []
        seen_triples = set()  # To avoid duplicates

        # Try to match relation patterns
        for i, (subj_type, subj_text, subj_start, subj_end) in enumerate(entities):
            for j, (obj_type, obj_text, obj_start, obj_end) in enumerate(entities):
                if i == j:
                    continue

                # Ensure subject comes before object
                if subj_start >= obj_start:
                    continue

                # Check against each relation pattern
                for pattern in self.relation_patterns:
                    if subj_type in pattern['subject_types'] and obj_type in pattern['object_types']:
                        # Check if there's a connecting phrase
                        found, _ = self._find_connecting_phrase(
                            text,
                            subj_end,
                            obj_start,
                            pattern['connecting_words']
                        )

                        if found:
                            triple = (subj_text, pattern['predicate'], obj_text)
                            triple_key = (subj_text.lower(), pattern['predicate'], obj_text.lower())

                            if triple_key not in seen_triples:
                                triples.append(triple)
                                seen_triples.add(triple_key)

        return triples

    def extract_simple_triples(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract simple entity co-occurrence triples
        When explicit relations aren't found, create MENTIONED_WITH relations

        Args:
            text: Input text

        Returns:
            List of (subject, predicate, object) triples
        """
        if not text or not isinstance(text, str):
            return []

        entities = self.ner.extract_entities(text)

        if len(entities) < 2:
            return []

        triples = []
        seen_pairs = set()

        # Create triples for entity pairs based on types
        for i, (type1, text1) in enumerate(entities):
            for j, (type2, text2) in enumerate(entities):
                if i >= j:
                    continue

                pair_key = (text1.lower(), text2.lower())
                if pair_key in seen_pairs:
                    continue

                # Create meaningful relations based on entity types
                predicate = self._infer_relation(type1, type2)
                if predicate:
                    triples.append((text1, predicate, text2))
                    seen_pairs.add(pair_key)

        return triples

    def _infer_relation(self, type1: str, type2: str) -> str:
        """Infer a relation based on entity types"""

        # Mapping of entity type pairs to likely relations
        type_relations = {
            ('PERSON', 'POLICY'): 'ASSOCIATED_WITH',
            ('PERSON', 'LOCATION'): 'ASSOCIATED_WITH',
            ('PERSON', 'ORGANIZATION'): 'ASSOCIATED_WITH',
            ('LOCATION', 'LOCATION'): 'RELATED_TO',
            ('LOCATION', 'POLICY'): 'RELATED_TO',
            ('LOCATION', 'ECONOMIC_SECTOR'): 'HAS_SECTOR',
            ('LOCATION', 'PRODUCT'): 'PRODUCES',
            ('ORGANIZATION', 'POLICY'): 'RELATED_TO',
            ('ORGANIZATION', 'LOCATION'): 'OPERATES_IN',
            ('POLICY', 'ECONOMIC_SECTOR'): 'AFFECTS',
            ('POLICY', 'PRODUCT'): 'AFFECTS',
            ('TARIFF_RATE', 'PRODUCT'): 'APPLIES_TO',
            ('TARIFF_RATE', 'LOCATION'): 'APPLIES_TO',
            ('PERCENTAGE', 'PRODUCT'): 'APPLIES_TO',
            ('MONEY', 'LOCATION'): 'RELATED_TO',
        }

        return type_relations.get((type1, type2), 'MENTIONED_WITH')


if __name__ == "__main__":
    # Test the relation extraction system
    extractor = RelationExtractor()

    test_texts = [
        "Trump announces 25% tariff on Chinese imports",
        "Biden and Modi discuss trade deal",
        "BBC reports that steel tariffs impact manufacturing sector",
        "China exports aluminum to USA",
        "The White House opposes the trade agreement"
    ]

    print("Testing Relation Extraction System\n" + "="*50)
    for text in test_texts:
        print(f"\nText: {text}")

        # Extract entities
        entities = extractor.ner.extract_entities(text)
        print("Entities:", entities)

        # Extract relations
        relations = extractor.extract_relations(text)
        print("Relations (triples):")
        for subj, pred, obj in relations:
            print(f"  ({subj}, {pred}, {obj})")

        # If no relations found, try simple triples
        if not relations:
            simple_triples = extractor.extract_simple_triples(text)
            print("Simple triples:")
            for subj, pred, obj in simple_triples:
                print(f"  ({subj}, {pred}, {obj})")
