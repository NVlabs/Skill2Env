# Python-Based Qualitative Analysis Workflows

Ready-to-run Python recipes for researchers who prefer open-source tools over NVivo/Atlas.ti. These support the workflows summarized in Section 7 of `SKILL.md`: keyword-based initial coding, word-frequency/collocation analysis, and thematic-network visualization.

**Basic Text Coding with Python:**

```python
import pandas as pd
from pathlib import Path

# Load transcripts (read_text closes the file handle automatically)

transcripts = {
    p.stem: p.read_text(encoding='utf-8')
    for p in sorted(Path('data').glob('P*_transcript.txt'))
}

# Define codebook
codebook = {
    'PEER_SUPPORT': [
        'colleague helped', 'learned from peers', 'informal mentoring',
        'asked a friend', 'peer advice'
    ],
    'ISOLATION': [
        'felt alone', 'no one to talk to', 'disconnected',
        'on my own', 'nobody understands'
    ],
    'INSTITUTIONAL_BARRIERS': [
        'red tape', 'bureaucracy', 'no support from admin',
        'policy prevented', 'institutional resistance'
    ],
}

# Simple keyword-based initial coding (supplement with manual coding)
def code_transcript(text, codebook):
    results = []
    sentences = text.split('.')
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower().strip()
        for code, keywords in codebook.items():
            for keyword in keywords:
                if keyword in sentence_lower:
                    results.append({
                        'sentence_num': i + 1,
                        'text': sentence.strip(),
                        'code': code,
                        'keyword_match': keyword
                    })
    return pd.DataFrame(results)

# Code all transcripts
all_coded = []
for pid, text in transcripts.items():
    coded = code_transcript(text, codebook)
    coded['participant'] = pid
    all_coded.append(coded)

coded_data = pd.concat(all_coded, ignore_index=True)

# Code frequency by participant
code_freq = coded_data.groupby(['participant', 'code']).size().unstack(fill_value=0)
print(code_freq)
```

**Word Frequency and Collocation Analysis:**

```python
from sklearn.feature_extraction.text import CountVectorizer

# Combine all transcripts
all_text = ' '.join(transcripts.values())

# Bigram/trigram frequency (useful for identifying recurring phrases).
# CountVectorizer's built-in 'english' stop-word list removes function words;
# treat output as a sensitizing aid, not a substitute for interpretive coding.
vectorizer = CountVectorizer(ngram_range=(2, 3), stop_words='english', max_features=50)
bigrams = vectorizer.fit_transform([all_text])
bigram_freq = dict(zip(vectorizer.get_feature_names_out(), bigrams.toarray()[0]))
sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)

print("Top 20 bigrams/trigrams:")
for phrase, count in sorted_bigrams[:20]:
    print(f"  {phrase}: {count}")
```

**Thematic Network Visualization:**

```python
import networkx as nx
import matplotlib.pyplot as plt

# Define theme relationships
G = nx.Graph()

# Add nodes (themes and subthemes)
themes = {
    'Navigating Uncertainty': ['Ambiguous expectations', 'Shifting goalposts', 'Information gaps'],
    'Building Support Networks': ['Peer mentoring', 'Online communities', 'Cross-departmental allies'],
    'Identity Transformation': ['Role conflict', 'Impostor feelings', 'Growing confidence'],
}

for theme, subthemes in themes.items():
    G.add_node(theme, node_type='global_theme', size=3000)
    for sub in subthemes:
        G.add_node(sub, node_type='organizing_theme', size=1500)
        G.add_edge(theme, sub)

# Cross-theme connections
G.add_edge('Ambiguous expectations', 'Impostor feelings')
G.add_edge('Peer mentoring', 'Growing confidence')

# Visualize
colors = ['#e74c3c' if G.nodes[n].get('node_type') == 'global_theme' else '#3498db' for n in G.nodes]
sizes = [G.nodes[n].get('size', 1000) for n in G.nodes]

plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=2, seed=42)
nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes,
        font_size=9, font_weight='bold', edge_color='#bdc3c7', width=2)
plt.title("Thematic Network")
plt.tight_layout()
plt.savefig('figures/thematic_network.png', dpi=300, bbox_inches='tight')
```
