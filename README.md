# Named Entity Recognition and Knowledge Graph Construction
## Analysis of Tariffs Discussions on Reddit (Phase 2)

**Team 14**
- Ayush Khandal (22UCC028)
- Pulkit Bohra (22UCC079)
- Yatharth Patil (22UCC121)

**Course:** Introduction to Knowledge Graph
**Submission Date:** November 23, 2025

---

## Project Overview

This project implements a **custom Named Entity Recognition (NER)** system and **Relation Extraction** module to build a **Knowledge Graph** from Reddit discussions about tariffs. The implementation is built from scratch without using pretrained NER models or LLMs.

### Key Features

- **Custom NER System**: Rule-based entity recognition using pattern matching and domain-specific dictionaries
- **Relation Extraction**: Pattern-based extraction of relationships between entities
- **Knowledge Graph Construction**: Graph-based representation of entities and their relationships
- **Comprehensive Visualization**: Multiple visualizations of the knowledge graph and statistics
- **Detailed Analytics**: Graph metrics, entity rankings, and relation distribution analysis

---

## Project Structure

```
GA/
├── data/
│   └── reddit_posts.csv          # Reddit posts dataset
├── src/
│   ├── custom_ner.py              # Custom NER implementation
│   ├── relation_extraction.py     # Relation extraction module
│   ├── knowledge_graph.py         # KG construction and analysis
│   ├── visualization.py           # Visualization module
│   └── main_pipeline.py           # Main processing pipeline
├── output/
│   ├── knowledge_graph.json       # KG in JSON format
│   ├── triples.csv                # Extracted triples
│   ├── knowledge_graph.nt         # RDF N-Triples format
│   └── analysis_report.json       # Detailed analysis report
├── visualizations/
│   ├── knowledge_graph.png        # Graph visualization
│   ├── statistics.png             # Statistics plots
│   └── relations.png              # Relation distribution
├── requirements.txt               # Python dependencies
├── REPORT.md                      # Comprehensive project report
└── README.md                      # This file
```

---

## Installation

### Prerequisites
- Python 3.7+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd GA
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Place the dataset:
- Download `reddit_posts.csv` from the Google Drive link
- Place it in the `data/` directory

---

## Usage

### Running the Complete Pipeline

```bash
cd src
python main_pipeline.py
```

This will:
1. Load the Reddit posts dataset
2. Extract named entities using custom NER
3. Extract relations to form triples
4. Build the knowledge graph
5. Generate visualizations
6. Create analysis reports

### Testing Individual Modules

#### Test NER System:
```bash
python custom_ner.py
```

#### Test Relation Extraction:
```bash
python relation_extraction.py
```

#### Test Knowledge Graph:
```bash
python knowledge_graph.py
```

---

## Methodology

### 1. Named Entity Recognition (NER)

Our custom NER system identifies the following entity types:

- **PERSON**: Political figures, economists (e.g., Trump, Biden, Modi)
- **LOCATION**: Countries, regions, cities (e.g., USA, China, India)
- **ORGANIZATION**: News outlets, companies, government bodies (e.g., BBC, CNN, WTO)
- **POLICY**: Trade policies and agreements (e.g., MAGA, NAFTA, USMCA)
- **ECONOMIC_SECTOR**: Industries and sectors (e.g., manufacturing, agriculture)
- **MONEY**: Monetary values (e.g., $200 billion)
- **PERCENTAGE**: Percentages (e.g., 25%)
- **TARIFF_RATE**: Specific tariff rates
- **DATE**: Temporal expressions
- **PRODUCT**: Goods and products (e.g., steel, aluminum)

**Approach:**
- Dictionary-based matching with domain-specific entity lists
- Regex pattern matching for structured entities (money, dates, percentages)
- Overlap resolution to handle nested entities
- Context-aware capitalization normalization

### 2. Relation Extraction

The system extracts relationships using pattern-based matching:

**Relation Types:**
- ANNOUNCES, INCREASES, DECREASES
- REPORTS, TRADES_WITH, IMPACTS
- SUPPORTS, OPPOSES, NEGOTIATES
- TARGETS, LEADS, EXPORTS, IMPORTS
- And fallback co-occurrence relations

**Approach:**
- Pattern matching between entity pairs
- Connecting word/phrase detection
- Entity type compatibility checking
- Simple co-occurrence for implicit relations

### 3. Knowledge Graph Construction

- **Graph Type**: Directed multi-graph (allows multiple relations between entities)
- **Storage**: NetworkX-based graph structure
- **Exports**: JSON, CSV, RDF N-Triples formats

**Graph Analytics:**
- Degree centrality
- PageRank
- Betweenness centrality
- Connected components analysis
- Relation and entity type distributions

---

## Results

The pipeline processes all 433 Reddit posts and generates:

1. **Knowledge Graph** with entities as nodes and relations as edges
2. **Triples Dataset** in (subject, predicate, object) format
3. **Visualizations** showing:
   - Network structure with colored nodes by entity type
   - Entity type and relation distributions
   - Top entities by various centrality metrics
4. **Analysis Report** containing comprehensive statistics

---

## Key Advantages of Our Approach

### No LLMs or Pretrained Models
- Built entirely from scratch using rule-based methods
- Full transparency and interpretability
- No dependency on external APIs or large models
- Complete control over entity types and relations

### Domain-Specific Customization
- Tailored to tariffs and trade policy discussions
- Specialized entity types (POLICY, ECONOMIC_SECTOR, TARIFF_RATE)
- Contextual relation patterns

### Scalable and Efficient
- Fast processing without GPU requirements
- Minimal dependencies
- Easy to extend with new patterns and entity types

---

## Limitations

1. **Coverage**: Dictionary-based approach may miss rare entities
2. **Ambiguity**: Limited context understanding compared to deep learning models
3. **Relation Complexity**: Pattern-based extraction may miss complex implicit relations
4. **Language**: English-only support

---

## Future Enhancements

1. Expand entity dictionaries with automatic discovery
2. Add coreference resolution
3. Implement entity linking to external knowledge bases
4. Multi-language support
5. Temporal relation extraction
6. Sentiment analysis for relations

---

## References

1. NetworkX Documentation: https://networkx.org/
2. Knowledge Graph Construction Methodologies
3. Rule-based NER Approaches
4. Reddit API and Data Collection

---

## License

This project is created for academic purposes as part of the Introduction to Knowledge Graph course.

---

## Contact

For questions or issues, please contact the team members through the course portal.
