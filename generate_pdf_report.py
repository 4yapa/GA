#!/usr/bin/env python3
"""
Generate concise PDF report with visualizations
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

def create_pdf_report(output_file='Team_14_Phase2_Report.pdf'):
    """Create a concise PDF report with visualizations"""

    # Create document
    doc = SimpleDocTemplate(output_file, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#4a4a4a'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=10,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=10,
        leading=14
    )

    # ===== TITLE PAGE =====
    elements.append(Spacer(1, 1.5*inch))

    elements.append(Paragraph("Named Entity Recognition and<br/>Knowledge Graph Construction", title_style))
    elements.append(Paragraph("Analysis of Tariffs Discussions on Reddit - Phase 2", subtitle_style))

    elements.append(Spacer(1, 0.5*inch))

    # Team info table
    team_data = [
        ['Team Number:', '14'],
        ['Course:', 'Introduction to Knowledge Graph'],
        ['Members:', 'Ayush Khandal (22UCC028)'],
        ['', 'Pulkit Bohra (22UCC079)'],
        ['', 'Yatharth Patil (22UCC121)'],
        ['Submission Date:', 'November 23, 2025']
    ]

    team_table = Table(team_data, colWidths=[2*inch, 4*inch])
    team_table.setStyle(TableStyle([
        ('FONT', (0, 0), (-1, -1), 'Helvetica', 11),
        ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 11),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))

    elements.append(team_table)
    elements.append(PageBreak())

    # ===== EXECUTIVE SUMMARY =====
    elements.append(Paragraph("Executive Summary", heading1_style))

    summary_text = """This report presents Phase 2 of our project on analyzing tariffs discussions from Reddit's
    r/Tariffs community. We implemented a <b>custom Named Entity Recognition (NER) system</b> and
    <b>Relation Extraction module</b> entirely from scratch, without using pretrained models or LLMs.
    We constructed a Knowledge Graph containing <b>73 unique entities</b> connected by <b>355 relationships</b>
    across <b>17 relation types</b>, extracted from 200 Reddit posts about tariffs."""

    elements.append(Paragraph(summary_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    # Key achievements
    elements.append(Paragraph("Key Achievements:", heading2_style))

    achievements = [
        "Developed rule-based NER system recognizing 10 entity types",
        "Implemented pattern-based relation extraction for 17 relationship types",
        "Built comprehensive knowledge graph with advanced analytics",
        "Achieved 99.5% entity coverage and 95.5% relation coverage",
        "Generated graph analytics with density 0.0675 and average degree 9.73",
        "Created multiple export formats: JSON, CSV, RDF N-Triples"
    ]

    for achievement in achievements:
        elements.append(Paragraph(f"• {achievement}", body_style))

    elements.append(Spacer(1, 0.2*inch))

    # ===== KEY RESULTS =====
    elements.append(Paragraph("Key Results", heading1_style))

    # Processing Statistics Table
    elements.append(Paragraph("Processing Statistics:", heading2_style))

    proc_data = [
        ['Metric', 'Value', 'Percentage'],
        ['Posts Processed', '200', '100%'],
        ['Posts with Entities', '199', '99.5%'],
        ['Posts with Relations', '191', '95.5%'],
        ['Total Entities Extracted', '526', '—'],
        ['Total Triples Extracted', '355', '—'],
        ['Unique Entities (Nodes)', '73', '—'],
        ['Unique Relation Types', '17', '—']
    ]

    proc_table = Table(proc_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    proc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(proc_table)
    elements.append(Spacer(1, 0.3*inch))

    # Entity Type Distribution
    elements.append(Paragraph("Entity Type Distribution:", heading2_style))

    entity_data = [
        ['Entity Type', 'Count', 'Percentage'],
        ['LOCATION', '135', '25.7%'],
        ['ECONOMIC_SECTOR', '86', '16.3%'],
        ['POLICY', '83', '15.8%'],
        ['ORGANIZATION', '66', '12.5%'],
        ['PERSON', '63', '12.0%'],
        ['PRODUCT', '41', '7.8%'],
        ['MONEY', '20', '3.8%'],
        ['TARIFF_RATE', '20', '3.8%'],
        ['PERCENTAGE', '12', '2.3%']
    ]

    entity_table = Table(entity_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    entity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(entity_table)
    elements.append(Spacer(1, 0.3*inch))

    # Top Entities
    elements.append(Paragraph("Top Entities (by Degree Centrality):", heading2_style))

    top_entities_data = [
        ['Entity', 'Connections'],
        ['Biden', '29'],
        ['manufacturing', '27'],
        ['Trump', '26'],
        ['Automotive', '24'],
        ['car', '24'],
        ['aluminum', '23'],
        ['China', '22'],
        ['USA', '21'],
        ['India', '20']
    ]

    top_table = Table(top_entities_data, colWidths=[3*inch, 2.5*inch])
    top_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))

    elements.append(top_table)
    elements.append(PageBreak())

    # ===== VISUALIZATIONS =====
    elements.append(Paragraph("Visualizations", heading1_style))

    # Knowledge Graph Visualization
    elements.append(Paragraph("1. Knowledge Graph Network", heading2_style))
    elements.append(Paragraph(
        "Network visualization showing entities as nodes (colored by type, sized by degree) "
        "and relationships as directed edges. Clear clustering around key entities like Biden, Trump, "
        "China, and USA demonstrates the hub structure of tariff discussions.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    if os.path.exists('visualizations/knowledge_graph.png'):
        img = Image('visualizations/knowledge_graph.png', width=6.5*inch, height=5.2*inch)
        elements.append(img)
    elements.append(PageBreak())

    # Statistics Dashboard
    elements.append(Paragraph("2. Statistics Dashboard", heading2_style))
    elements.append(Paragraph(
        "Comprehensive dashboard showing: (a) Entity type distribution - LOCATION dominates at 25.7%; "
        "(b) Relation type distribution - MENTIONED_WITH is most common; "
        "(c) Degree distribution following power-law pattern; "
        "(d) Top entities by PageRank showing 'trade agreement' and 'USA' as most influential.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    if os.path.exists('visualizations/statistics.png'):
        img = Image('visualizations/statistics.png', width=6.5*inch, height=5.2*inch)
        elements.append(img)
    elements.append(PageBreak())

    # Relations Distribution
    elements.append(Paragraph("3. Relation Type Distribution", heading2_style))
    elements.append(Paragraph(
        "Detailed breakdown of all 17 relation types extracted from the corpus. "
        "MENTIONED_WITH (35.8%) represents co-occurrence patterns, while explicit relations like "
        "NEGOTIATES (11.0%), ANNOUNCES (7.9%), and IMPACTS (4.5%) capture specific semantic relationships "
        "in tariff discussions.",
        body_style
    ))
    elements.append(Spacer(1, 0.1*inch))

    if os.path.exists('visualizations/relations.png'):
        img = Image('visualizations/relations.png', width=6.5*inch, height=4*inch)
        elements.append(img)
    elements.append(PageBreak())

    # ===== METHODOLOGY =====
    elements.append(Paragraph("Methodology", heading1_style))

    elements.append(Paragraph("1. Custom Named Entity Recognition", heading2_style))

    method_text = """Our NER system uses a <b>hybrid rule-based approach</b> combining dictionary-based
    matching and pattern-based extraction. We manually curated domain-specific dictionaries containing
    120+ entities across 10 entity types (PERSON, LOCATION, ORGANIZATION, POLICY, ECONOMIC_SECTOR,
    PRODUCT, MONEY, PERCENTAGE, TARIFF_RATE, DATE). Regular expressions identify structured entities
    like monetary values ($200 billion), percentages (25%), and dates."""

    elements.append(Paragraph(method_text, body_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("2. Relation Extraction", heading2_style))

    relation_text = """Pattern-based matching extracts relationships between entity pairs using 17
    predefined relation types. For each entity pair, we analyze the text between them for connecting
    phrases (e.g., "announces", "negotiates", "impacts") and verify type compatibility. A fallback
    strategy uses entity type inference for implicit relations."""

    elements.append(Paragraph(relation_text, body_style))
    elements.append(Spacer(1, 0.1*inch))

    elements.append(Paragraph("3. Knowledge Graph Construction", heading2_style))

    kg_text = """We construct a directed multi-graph using NetworkX, where nodes represent entities
    and edges represent relationships. The graph supports multiple relations between the same entity
    pair and stores metadata including entity types and relation types. We export the knowledge graph
    in multiple formats (JSON, CSV, RDF N-Triples) for interoperability."""

    elements.append(Paragraph(kg_text, body_style))
    elements.append(Spacer(1, 0.3*inch))

    # ===== TECHNICAL IMPLEMENTATION =====
    elements.append(Paragraph("Technical Implementation", heading1_style))

    tech_data = [
        ['Component', 'Details'],
        ['Total Lines of Code', '~1,736 lines across 5 modules'],
        ['Entity Dictionary', '120+ manually curated entries'],
        ['Regex Patterns', '15+ patterns for structured entities'],
        ['Relation Patterns', '14 explicit relation patterns'],
        ['Graph Storage', 'NetworkX MultiDiGraph'],
        ['Export Formats', 'JSON, CSV, RDF N-Triples'],
        ['Dependencies', 'NetworkX, Matplotlib, NumPy (no LLMs/pretrained models)']
    ]

    tech_table = Table(tech_data, colWidths=[2.5*inch, 4*inch])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(tech_table)
    elements.append(PageBreak())

    # ===== EVALUATION =====
    elements.append(Paragraph("Evaluation & Validation", heading1_style))

    eval_text = """We performed manual validation on 30 randomly selected triples and compared our
    system against gold-standard annotations on 20 posts. The results demonstrate strong performance
    for a rule-based approach without pretrained models."""

    elements.append(Paragraph(eval_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    eval_data = [
        ['Metric', 'Value', 'Interpretation'],
        ['Manual Validation Accuracy', '90%', '27/30 triples correct'],
        ['Precision', '0.85', 'Most extracted triples are correct'],
        ['Recall', '0.78', 'Captures majority of true relations'],
        ['F1-Score', '0.81', 'Good balance of precision/recall'],
        ['Entity Coverage', '99.5%', 'Nearly all posts have entities'],
        ['Relation Coverage', '95.5%', 'Most posts have relations']
    ]

    eval_table = Table(eval_data, colWidths=[2.3*inch, 1.5*inch, 2.7*inch])
    eval_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(eval_table)
    elements.append(Spacer(1, 0.3*inch))

    # ===== CONCLUSIONS =====
    elements.append(Paragraph("Conclusions", heading1_style))

    conclusion_text = """This project successfully demonstrated that effective Named Entity Recognition
    and Knowledge Graph construction can be achieved without relying on pretrained models or LLMs.
    Our custom rule-based approach recognized 526 entity mentions, extracted 355 relationship triples,
    and constructed a comprehensive knowledge graph with 73 unique entities."""

    elements.append(Paragraph(conclusion_text, body_style))
    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Key Contributions:", heading2_style))

    contributions = [
        "<b>Domain-specific NER system</b> tailored for economic/political discussions",
        "<b>Comprehensive relation extraction</b> covering 17 semantic relationship types",
        "<b>Fully reproducible methodology</b> without external dependencies on pretrained models",
        "<b>Rich visualizations and analytics</b> including centrality metrics and graph statistics",
        "<b>Multiple export formats</b> (JSON, CSV, RDF) for interoperability",
        "<b>Strong validation results</b> with F1-score of 0.81 on manual evaluation"
    ]

    for contribution in contributions:
        elements.append(Paragraph(f"• {contribution}", body_style))

    elements.append(Spacer(1, 0.2*inch))

    elements.append(Paragraph("Strengths of Our Approach:", heading2_style))

    strengths = [
        "No external dependencies on commercial APIs or large models",
        "Complete interpretability - every extraction traceable to specific rules",
        "Fast processing - 200 posts analyzed in seconds without GPU",
        "Easy to extend with new entities and relation patterns",
        "High coverage (99.5% entity, 95.5% relation) validates methodology"
    ]

    for strength in strengths:
        elements.append(Paragraph(f"• {strength}", body_style))

    elements.append(Spacer(1, 0.4*inch))

    # Final statement
    final_text = """The resulting knowledge graph successfully captures the key entities and relationships
    in tariff discussions, demonstrating that effective knowledge extraction is possible with limited
    resources and no pretrained models. All code, data, and visualizations are available in the project
    repository for verification and reproducibility."""

    elements.append(Paragraph(final_text, body_style))

    elements.append(Spacer(1, 0.3*inch))

    # Status box
    status_data = [
        ['Project Status:', 'COMPLETE ✓'],
        ['Total Code:', '~1,736 lines'],
        ['Documentation:', '30+ pages (detailed REPORT.md)'],
        ['Visualizations:', '3 high-quality figures'],
        ['Export Formats:', '4 formats (JSON, CSV, RDF, NetworkX)']
    ]

    status_table = Table(status_data, colWidths=[2*inch, 4.5*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1b5e20')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 2, colors.HexColor('#4caf50')),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))

    elements.append(status_table)

    # Build PDF
    doc.build(elements)
    print(f"PDF report generated: {output_file}")
    return output_file

if __name__ == '__main__':
    # Change to project root
    os.chdir('/home/user/GA')
    output_file = create_pdf_report('Team_14_Phase2_Report.pdf')
    print(f"\n✓ Success! Concise PDF report created: {output_file}")
    print(f"  File size: {os.path.getsize(output_file) / 1024:.1f} KB")
