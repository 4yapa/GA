"""
Custom Named Entity Recognition System
Built from scratch without using pretrained NER models
"""

import re
from collections import defaultdict
from typing import List, Tuple, Dict, Set

class CustomNER:
    """
    Rule-based Named Entity Recognition system
    Identifies entities without using pretrained models
    """

    def __init__(self):
        # Initialize entity dictionaries and patterns
        self.entity_patterns = self._build_patterns()
        self.entity_dictionaries = self._build_dictionaries()

    def _build_dictionaries(self) -> Dict[str, Set[str]]:
        """Build entity dictionaries from domain knowledge"""

        dictionaries = {
            'PERSON': {
                # Political figures
                'trump', 'donald trump', 'biden', 'joe biden', 'xi jinping',
                'modi', 'narendra modi', 'trudeau', 'justin trudeau',
                'macron', 'emmanuel macron', 'johnson', 'boris johnson',
                'putin', 'vladimir putin', 'obama', 'barack obama',
                # Economists and analysts
                'yellen', 'janet yellen', 'powell', 'jerome powell'
            },

            'LOCATION': {
                # Countries
                'usa', 'united states', 'america', 'us', 'china', 'india',
                'canada', 'mexico', 'japan', 'germany', 'france', 'uk',
                'united kingdom', 'britain', 'russia', 'australia', 'brazil',
                'south korea', 'italy', 'spain', 'eu', 'european union',
                # Regions
                'asia', 'europe', 'north america', 'africa', 'middle east',
                # Cities
                'washington', 'beijing', 'new delhi', 'london', 'tokyo',
                'brussels', 'moscow', 'ottawa'
            },

            'ORGANIZATION': {
                # News organizations
                'bbc', 'cnn', 'fox news', 'reuters', 'bloomberg', 'wsj',
                'wall street journal', 'new york times', 'nyt', 'washington post',
                'financial times', 'economist', 'al jazeera', 'abc news',
                'nbc', 'msnbc', 'cnbc', 'forbes', 'politico',
                # International organizations
                'wto', 'world trade organization', 'imf', 'world bank',
                'un', 'united nations', 'nato', 'oecd',
                # Companies
                'apple', 'google', 'amazon', 'microsoft', 'tesla', 'walmart',
                'general motors', 'gm', 'ford', 'boeing', 'caterpillar',
                'harley davidson', 'samsung', 'huawei', 'alibaba',
                # Government bodies
                'congress', 'senate', 'house', 'white house', 'treasury',
                'commerce department', 'state department'
            },

            'POLICY': {
                'maga', 'make america great again', 'america first',
                'nafta', 'usmca', 'trade war', 'section 232', 'section 301',
                'reciprocal tariff', 'national security tariff', 'steel tariff',
                'aluminum tariff', 'auto tariff', 'trade deal', 'trade agreement',
                'free trade', 'protectionism', 'tariff policy'
            },

            'ECONOMIC_SECTOR': {
                'agriculture', 'manufacturing', 'automotive', 'steel', 'aluminum',
                'technology', 'tech', 'energy', 'oil', 'gas', 'solar',
                'semiconductor', 'electronics', 'textile', 'aerospace',
                'pharmaceuticals', 'chemicals'
            }
        }

        return dictionaries

    def _build_patterns(self) -> Dict[str, List[re.Pattern]]:
        """Build regex patterns for entity recognition"""

        patterns = {
            'MONEY': [
                re.compile(r'\$\s*\d+(?:,\d{3})*(?:\.\d+)?\s*(?:billion|million|thousand|trillion|bn|mn|k|m|b)?', re.IGNORECASE),
                re.compile(r'\d+(?:,\d{3})*(?:\.\d+)?\s*(?:dollars|usd|yuan|euros?|pounds?)', re.IGNORECASE),
            ],

            'PERCENTAGE': [
                re.compile(r'\d+(?:\.\d+)?\s*%'),
                re.compile(r'\d+(?:\.\d+)?\s*percent', re.IGNORECASE),
            ],

            'DATE': [
                re.compile(r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
                re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'),
                re.compile(r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)\.?\s+\d{1,2},?\s+\d{4}\b', re.IGNORECASE),
                re.compile(r'\b\d{4}\b(?=\s+(?:tariff|trade|deal))', re.IGNORECASE),
            ],

            'TARIFF_RATE': [
                re.compile(r'\d+(?:\.\d+)?\s*%\s*tariff', re.IGNORECASE),
                re.compile(r'tariff\s+of\s+\d+(?:\.\d+)?\s*%', re.IGNORECASE),
            ],

            'PRODUCT': [
                re.compile(r'\b(?:steel|aluminum|cars?|automobile|solar panels?|washing machines?|electronics?|semiconductors?|chips?|soybeans?|pork|beef|wheat|corn)\b', re.IGNORECASE),
            ]
        }

        return patterns

    def _match_dictionary(self, text: str) -> List[Tuple[str, str, int, int]]:
        """Match entities using dictionary lookup"""
        entities = []
        text_lower = text.lower()

        for entity_type, dictionary in self.entity_dictionaries.items():
            for entity in dictionary:
                # Find all occurrences
                start = 0
                while True:
                    pos = text_lower.find(entity, start)
                    if pos == -1:
                        break

                    # Check word boundaries
                    if pos > 0 and text_lower[pos-1].isalnum():
                        start = pos + 1
                        continue

                    end_pos = pos + len(entity)
                    if end_pos < len(text_lower) and text_lower[end_pos].isalnum():
                        start = pos + 1
                        continue

                    # Get original case from text
                    original_text = text[pos:end_pos]
                    entities.append((entity_type, original_text, pos, end_pos))
                    start = end_pos

        return entities

    def _match_patterns(self, text: str) -> List[Tuple[str, str, int, int]]:
        """Match entities using regex patterns"""
        entities = []

        for entity_type, pattern_list in self.entity_patterns.items():
            for pattern in pattern_list:
                for match in pattern.finditer(text):
                    entities.append((
                        entity_type,
                        match.group(0),
                        match.start(),
                        match.end()
                    ))

        return entities

    def _capitalize_entity(self, text: str, entity_type: str) -> str:
        """Normalize entity capitalization"""
        if entity_type in ['MONEY', 'PERCENTAGE', 'DATE', 'TARIFF_RATE']:
            return text

        # Title case for names and organizations
        if entity_type in ['PERSON', 'LOCATION', 'ORGANIZATION']:
            # Special cases
            if text.upper() in ['USA', 'UK', 'EU', 'UN', 'WTO', 'IMF', 'NATO', 'OECD',
                                 'CNN', 'BBC', 'ABC', 'NBC', 'NYT', 'WSJ', 'MSNBC', 'CNBC']:
                return text.upper()
            if text.lower() in ['usmca', 'nafta']:
                return text.upper()
            return text.title()

        return text

    def _resolve_overlaps(self, entities: List[Tuple[str, str, int, int]]) -> List[Tuple[str, str, int, int]]:
        """Resolve overlapping entities by keeping longer matches"""
        if not entities:
            return []

        # Sort by start position, then by length (descending)
        sorted_entities = sorted(entities, key=lambda x: (x[2], -(x[3] - x[2])))

        resolved = []
        last_end = -1

        for entity in sorted_entities:
            entity_type, text, start, end = entity

            # If this entity doesn't overlap with the last kept entity
            if start >= last_end:
                resolved.append(entity)
                last_end = end

        return resolved

    def extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """
        Extract named entities from text

        Args:
            text: Input text

        Returns:
            List of (entity_type, entity_text) tuples
        """
        if not text or not isinstance(text, str):
            return []

        # Match using both dictionaries and patterns
        dict_entities = self._match_dictionary(text)
        pattern_entities = self._match_patterns(text)

        # Combine and resolve overlaps
        all_entities = dict_entities + pattern_entities
        resolved_entities = self._resolve_overlaps(all_entities)

        # Return normalized entities
        result = []
        for entity_type, entity_text, _, _ in resolved_entities:
            normalized_text = self._capitalize_entity(entity_text, entity_type)
            result.append((entity_type, normalized_text))

        return result

    def extract_entities_with_positions(self, text: str) -> List[Tuple[str, str, int, int]]:
        """
        Extract named entities with their positions

        Args:
            text: Input text

        Returns:
            List of (entity_type, entity_text, start_pos, end_pos) tuples
        """
        if not text or not isinstance(text, str):
            return []

        dict_entities = self._match_dictionary(text)
        pattern_entities = self._match_patterns(text)

        all_entities = dict_entities + pattern_entities
        resolved_entities = self._resolve_overlaps(all_entities)

        # Normalize entity text
        result = []
        for entity_type, entity_text, start, end in resolved_entities:
            normalized_text = self._capitalize_entity(entity_text, entity_type)
            result.append((entity_type, normalized_text, start, end))

        return result


if __name__ == "__main__":
    # Test the NER system
    ner = CustomNER()

    test_texts = [
        "Trump announces 25% tariff on Chinese imports worth $200 billion",
        "Biden and Modi discuss trade deal in New Delhi on January 15, 2024",
        "BBC reports steel tariffs impact manufacturing sector",
        "The USMCA replaced NAFTA as the trade agreement between USA, Mexico, and Canada"
    ]

    print("Testing Custom NER System\n" + "="*50)
    for text in test_texts:
        print(f"\nText: {text}")
        entities = ner.extract_entities(text)
        print("Entities:")
        for entity_type, entity_text in entities:
            print(f"  - {entity_type}: {entity_text}")
