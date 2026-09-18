#!/usr/bin/env python3
"""
Content Optimizer - Phase 2
Rewrites content following GEO best practices (2025 research-backed)

Key optimizations:
- Paragraph length: 60-100 words
- Sentence length: 15-20 words
- TL;DR: First 40-60 words
- FAQ section: 40-60 word answers
- Evidence tables: Extractable facts
- H2→H3→bullet structure

Research: Statistics Addition (+41%), Quotation Addition (+28%)
"""

import re
import json
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import sys

# Use the shared text utilities so word-counting stays consistent
# with the rest of the audit pipeline.
sys.path.insert(0, str(Path(__file__).parent))
from shared.text_utils import count_words

class ContentStructureParser(HTMLParser):
    """Parse HTML to extract structural elements"""

    def __init__(self):
        super().__init__()
        self.content = {
            'title': '',
            'h1': [],
            'h2': [],
            'h3': [],
            'paragraphs': [],
            'lists': []
        }
        self.in_body = False
        self.current_tag = None
        self.current_text = ''
        
    def handle_starttag(self, tag, attrs):
        if tag == 'body':
            self.in_body = True
        if self.in_body:
            self.current_tag = tag
            
    def handle_endtag(self, tag):
        if tag == 'body':
            self.in_body = False
        if self.current_tag and self.current_text.strip():
            text = self.current_text.strip()
            if tag == 'title':
                self.content['title'] = text
            elif tag == 'h1':
                self.content['h1'].append(text)
            elif tag == 'h2':
                self.content['h2'].append(text)
            elif tag == 'h3':
                self.content['h3'].append(text)
            elif tag == 'p':
                self.content['paragraphs'].append(text)
        self.current_text = ''
        self.current_tag = None
        
    def handle_data(self, data):
        if self.current_tag:
            self.current_text += data

def optimize_paragraph_length(text: str, target_max: int = 100, target_min: int = 60) -> List[str]:
    """
    Split long paragraphs into 60-100 word chunks
    
    Args:
        text: Paragraph text
        target_max: Maximum words per paragraph
        target_min: Minimum words per paragraph
        
    Returns:
        List of optimized paragraphs
    """
    word_count = count_words(text)
    
    # If within range, return as-is
    if target_min <= word_count <= target_max:
        return [text]
    
    # If too short, return as-is (don't pad)
    if word_count < target_min:
        return [text]
    
    # If too long, split at natural break points
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_word_count = 0
    
    for sentence in sentences:
        sentence_words = count_words(sentence)
        
        if current_word_count + sentence_words > target_max and current_chunk:
            # Start new chunk
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentence]
            current_word_count = sentence_words
        else:
            current_chunk.append(sentence)
            current_word_count += sentence_words
    
    # Add remaining
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

def optimize_sentence_length(text: str, target_max: int = 20) -> str:
    """
    Split long sentences at natural break points (commas, conjunctions)
    
    Args:
        text: Text with sentences
        target_max: Maximum words per sentence
        
    Returns:
        Optimized text with shorter sentences
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    optimized = []
    
    for sentence in sentences:
        word_count = count_words(sentence)
        
        if word_count <= target_max:
            optimized.append(sentence)
            continue
        
        # Try splitting at commas
        if ',' in sentence:
            parts = sentence.split(',')
            current_part = []
            current_words = 0
            
            for i, part in enumerate(parts):
                part_words = count_words(part)
                
                if current_words + part_words > target_max and current_part:
                    # End sentence, start new one
                    reconstructed = ','.join(current_part).strip()
                    if not reconstructed.endswith('.'):
                        reconstructed += '.'
                    optimized.append(reconstructed)
                    current_part = [part.strip()]
                    current_words = part_words
                else:
                    current_part.append(part if i == 0 else part.strip())
                    current_words += part_words
            
            if current_part:
                reconstructed = ','.join(current_part).strip()
                if not reconstructed.endswith(('.', '!', '?')):
                    reconstructed += '.'
                optimized.append(reconstructed)
        else:
            # Can't split easily, keep as-is
            optimized.append(sentence)
    
    return ' '.join(optimized)

def generate_tldr(content: Dict, word_limit: int = 60) -> str:
    """
    Generate TL;DR summary from content (40-60 words)
    
    Args:
        content: Parsed content structure
        word_limit: Maximum words for TL;DR
        
    Returns:
        TL;DR text
    """
    # Extract key information
    topic = content['h1'][0] if content['h1'] else content['title']
    
    # Get first paragraph or two that together make ~40-60 words
    summary_parts = []
    word_count = 0
    
    for para in content['paragraphs'][:3]:
        para_words = count_words(para)
        if word_count + para_words <= word_limit:
            # Take first sentence from paragraph
            sentences = re.split(r'(?<=[.!?])\s+', para)
            if sentences:
                summary_parts.append(sentences[0])
                word_count += count_words(sentences[0])
        
        if word_count >= 40:  # Minimum threshold
            break
    
    if not summary_parts:
        return f"{topic}. " + ' '.join(content['paragraphs'][:1])
    
    return ' '.join(summary_parts)

def convert_h2_to_question(h2_text: str) -> str:
    """
    Convert H2 heading to question format
    
    Args:
        h2_text: H2 heading text
        
    Returns:
        Question format
    """
    # Already a question
    if h2_text.strip().endswith('?'):
        return h2_text
    
    # Common patterns
    patterns = {
        r'^About (.+)': r'What is \1?',
        r'^(.+) Services?$': r'What \1 services do you offer?',
        r'^Our (.+)': r'What is your \1?',
        r'^Why (.+)': r'Why \1?',
        r'^How (.+)': r'How \1?',
        r'^Benefits?$': r'What are the benefits?',
        r'^Contact$': r'How do I contact you?',
    }
    
    for pattern, replacement in patterns.items():
        if re.match(pattern, h2_text, re.IGNORECASE):
            return re.sub(pattern, replacement, h2_text, flags=re.IGNORECASE)
    
    # Default: prepend "What is"
    return f"What is {h2_text.lower()}?"

def create_faq_section(content: Dict) -> List[Dict[str, str]]:
    """
    Generate FAQ from H2 headings and content
    
    Args:
        content: Parsed content structure
        
    Returns:
        List of FAQ items {question, answer}
    """
    faqs = []
    
    # Use H2 headings as question basis
    for i, h2 in enumerate(content['h2'][:5]):  # Max 5 FAQs
        question = convert_h2_to_question(h2)
        
        # Find associated paragraph (simple heuristic: next paragraph after H2)
        if i < len(content['paragraphs']):
            para = content['paragraphs'][i]
            
            # Extract first 40-60 words
            sentences = re.split(r'(?<=[.!?])\s+', para)
            answer_parts = []
            word_count = 0
            
            for sentence in sentences:
                sentence_words = count_words(sentence)
                if word_count + sentence_words <= 60:
                    answer_parts.append(sentence)
                    word_count += sentence_words
                
                if word_count >= 40:
                    break
            
            answer = ' '.join(answer_parts) if answer_parts else sentences[0] if sentences else para[:200]
            
            faqs.append({
                'question': question,
                'answer': answer
            })
    
    return faqs

def extract_statistics(text: str) -> List[Dict[str, str]]:
    """
    Extract statistics and numbers from text
    
    Args:
        text: Text to analyze
        
    Returns:
        List of extracted statistics
    """
    statistics = []
    
    # Pattern: number + unit/context
    patterns = [
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\s*(%|percent|years?|months?|patients?|people|users?|cases?)',
        r'(\d+(?:,\d{3})*(?:\.\d+)?)\+?\s+(experience|years of experience)',
        r'(\$\d+(?:,\d{3})*(?:\.\d+)?(?:M|K|B)?)',
        r'(\d+(?:,\d{3})*)\s+(\w+)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            statistics.append({
                'value': match.group(0),
                'context': text[max(0, match.start()-50):min(len(text), match.end()+50)]
            })
    
    return statistics

def create_evidence_table(statistics: List[Dict[str, str]]) -> str:
    """
    Create Markdown evidence table from statistics
    
    Args:
        statistics: List of extracted statistics
        
    Returns:
        Markdown table
    """
    if not statistics:
        return ""
    
    table = "| Metric | Value | Context |\n"
    table += "|--------|-------|----------|\n"
    
    for stat in statistics[:10]:  # Max 10 rows
        # Extract metric name from context
        context = stat['context'].strip()
        metric = context.split()[0] if context else "Data point"
        value = stat['value']
        context_short = context[:50] + "..." if len(context) > 50 else context
        
        table += f"| {metric} | {value} | {context_short} |\n"
    
    return table

def optimize_content(file_path: str, output_path: Optional[str] = None, config: Optional[Dict] = None) -> Dict:
    """
    Main optimization function
    
    Args:
        file_path: Path to HTML file
        output_path: Path for optimized file (None = auto-generate)
        config: Configuration options
        
    Returns:
        Optimization results
    """
    if config is None:
        config = {
            'add_tldr': True,
            'add_faq': True,
            'add_evidence_table': True,
            'optimize_paragraphs': True,
            'optimize_sentences': True,
        }
    
    # Read file
    with open(file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Parse structure
    parser = ContentStructureParser()
    parser.feed(html_content)
    content = parser.content
    
    # Track changes
    changes = []
    optimized_html = html_content
    
    # 1. Add meta description (TL;DR in metadata, not visible)
    if config.get('add_tldr', True):
        tldr = generate_tldr(content)

        # Add as meta description
        meta_desc = f'<meta name="description" content="{tldr[:160]}">\n'

        if '<head>' in optimized_html and '<meta name="description"' not in optimized_html:
            optimized_html = optimized_html.replace('</head>', f'{meta_desc}</head>')
            changes.append(f"Added meta description ({count_words(tldr)} words)")

        # Rewrite first paragraph to be direct (natural, no label)
        if content['paragraphs'] and '<p>' in optimized_html:
            # Make first paragraph more direct/concise
            first_p = content['paragraphs'][0]
            if count_words(first_p) > 60:
                sentences = re.split(r'(?<=[.!?])\s+', first_p)
                direct_intro = ' '.join(sentences[:2]) if len(sentences) > 1 else sentences[0]
                optimized_html = optimized_html.replace(f'<p>{first_p}</p>', f'<p>{direct_intro}</p>', 1)
                changes.append("Optimized first paragraph for directness")
    
    # 2. Add FAQ section
    if config.get('add_faq', True):
        faqs = create_faq_section(content)
        if faqs:
            faq_html = '\n<h2>Frequently Asked Questions</h2>\n\n'
            for faq in faqs:
                faq_html += f'<h3>{faq["question"]}</h3>\n'
                faq_html += f'<p>{faq["answer"]}</p>\n\n'
            
            # Insert before closing body tag
            optimized_html = optimized_html.replace('</body>', f'\n{faq_html}\n</body>')
            changes.append(f"Added FAQ section ({len(faqs)} questions)")
    
    # 3. Add evidence table (keep table, but natural heading)
    if config.get('add_evidence_table', True):
        # Extract statistics from all paragraphs
        all_text = ' '.join(content['paragraphs'])
        statistics = extract_statistics(all_text)

        if statistics and len(statistics) >= 3:  # Only if meaningful data
            table = create_evidence_table(statistics)
            # Natural heading, no "Key Data Points" label
            table_html = f'\n<h2>Data Summary</h2>\n\n{table}\n\n'

            # Insert before FAQ or before closing body
            if '<h2>Frequently Asked Questions</h2>' in optimized_html:
                optimized_html = optimized_html.replace(
                    '<h2>Frequently Asked Questions</h2>',
                    f'{table_html}\n<h2>Frequently Asked Questions</h2>'
                )
            else:
                optimized_html = optimized_html.replace('</body>', f'{table_html}\n</body>')

            changes.append(f"Added data summary table ({len(statistics)} points)")
    
    # Determine output path
    if output_path is None:
        base = file_path.rsplit('.', 1)[0]
        output_path = f"{base}-optimized.html"
    
    # Write optimized file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(optimized_html)
    
    return {
        'success': True,
        'input_file': file_path,
        'output_file': output_path,
        'changes': changes,
        'original_stats': {
            'word_count': sum(count_words(p) for p in content['paragraphs']),
            'paragraphs': len(content['paragraphs']),
            'h2_count': len(content['h2']),
            'h3_count': len(content['h3']),
        }
    }

def main():
    """CLI interface"""
    if len(sys.argv) < 2:
        print("Usage: python content_optimizer.py <file_path> [output_path]")
        print("\nOptimizes content following GEO best practices:")
        print("  - Adds TL;DR (40-60 words)")
        print("  - Generates FAQ section")
        print("  - Creates evidence table from statistics")
        print("  - Optimizes paragraph/sentence length")
        sys.exit(1)
    
    file_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    print(f"Optimizing: {file_path}")
    print("=" * 60)
    
    result = optimize_content(file_path, output_path)
    
    if result['success']:
        print(f"✓ Optimization complete")
        print(f"  Output: {result['output_file']}")
        print(f"\nChanges applied:")
        for change in result['changes']:
            print(f"  - {change}")
        
        print(f"\nOriginal stats:")
        for key, value in result['original_stats'].items():
            print(f"  {key}: {value}")
    else:
        print("✗ Optimization failed")
        sys.exit(1)

if __name__ == '__main__':
    main()
