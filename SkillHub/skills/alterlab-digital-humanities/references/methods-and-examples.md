# Digital Humanities — Worked Examples and Method Details

Detailed worked examples, code, and parameter tables for the methods summarized in `SKILL.md`. Grouped by capability. For tool comparison matrices, topic-modeling parameter tuning, AntConc/Voyant panels, OCR engine configuration, TEI element catalogues, QGIS georeferencing, and the full `stylo` R guide, see the companion `dh-tools-guide.md`.

## Text Mining and NLP

### Topic Modeling — LDA

LDA (Blei, Ng, & Jordan, 2003) models each document as a mixture of topics and each topic as a distribution over words. It is a bag-of-words model — word order does not matter.

**LDA workflow:**

1. **Corpus preparation** — Collect and clean texts (remove headers, footers, metadata)
2. **Preprocessing** — Tokenize, lowercase, remove stop words, lemmatize
3. **Feature extraction** — Create document-term matrix or bag-of-words representation
4. **Model training** — Run LDA with specified number of topics (k)
5. **Evaluation** — Assess coherence scores, inspect topic-word distributions
6. **Interpretation** — Label topics based on high-probability words and representative documents
7. **Analysis** — Track topic proportions across time, genres, authors, or other categories

**Example: LDA topic from a corpus of 19th-century British novels**

```
Topic 7 (labeled "Domestic Life"):
  Top words: room, house, door, table, fire, chair, window, sat,
             morning, evening, bed, garden, dinner, tea, kitchen

  Top documents: Cranford (Gaskell), Middlemarch (Eliot),
                 North and South (Gaskell)

  Interpretation: This topic captures domestic settings and daily
  routines. Its prevalence increases in novels by women authors
  and in novels published after 1850, suggesting a shift toward
  domestic realism in mid-Victorian fiction.
```

**Choosing the number of topics (k):**
- Coherence scores (higher is better) — compute for k = 5, 10, 15, 20, 25, 30, 40, 50
- Human interpretability — can you label each topic meaningfully?
- Research question alignment — does the granularity match your analytical needs?
- Common range: 15-50 topics for corpora of 1,000-10,000 documents

### Topic Modeling — BERTopic

BERTopic (Grootendorst, 2022) uses transformer-based sentence embeddings (BERT) to create document representations, then clusters them using HDBSCAN and extracts topic representations using c-TF-IDF. Unlike LDA, it captures semantic meaning beyond individual words.

**Advantages over LDA:**
- Captures semantic similarity (not just word co-occurrence)
- Handles short texts better (tweets, abstracts, metadata)
- Produces more coherent topics on modern text
- Does not require specifying the number of topics in advance

```python
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer

# Use a sentence transformer model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize and fit BERTopic
topic_model = BERTopic(
    embedding_model=embedding_model,
    min_topic_size=10,
    nr_topics="auto"
)

topics, probs = topic_model.fit_transform(documents)

# Inspect topics
topic_model.get_topic_info()

# Visualize topic distribution
topic_model.visualize_topics()

# Track topics over time
topics_over_time = topic_model.topics_over_time(
    documents, timestamps
)
topic_model.visualize_topics_over_time(topics_over_time)
```

### Sentiment Analysis

| Approach | How It Works | Best For | Limitations |
|----------|-------------|----------|------------|
| Lexicon-based (VADER, AFINN, NRC) | Counts words from sentiment dictionaries | Quick analysis, transparent | Misses context, sarcasm, domain-specific usage |
| Machine learning (Naive Bayes, SVM) | Trained on labeled examples | Domain-specific tasks | Requires labeled training data |
| Transformer-based (BERT, RoBERTa) | Fine-tuned language models | High accuracy, context-aware | Computationally expensive, may need fine-tuning |

**Cautions for humanities research:**
- Historical texts use language differently than modern training data — a sentiment model trained on product reviews will misclassify 18th-century prose
- Literary language uses irony, ambiguity, and indirection that confound automated classification
- Always validate automated sentiment against human annotation on a sample of your corpus
- Report the specific tool, model, and version used for reproducibility

**Example: Sentiment arc analysis of a novel**

```python
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize VADER
sid = SentimentIntensityAnalyzer()

# Split novel into chunks (e.g., 1000-word windows)
chunks = split_text(novel_text, window_size=1000)

# Calculate sentiment for each chunk
sentiments = []
for chunk in chunks:
    scores = sid.polarity_scores(chunk)
    sentiments.append(scores["compound"])

# Plot the sentiment arc
import matplotlib.pyplot as plt
plt.plot(range(len(sentiments)), sentiments)
plt.xlabel("Narrative Position")
plt.ylabel("Sentiment (VADER compound)")
plt.title("Emotional Arc: Pride and Prejudice")
plt.axhline(y=0, color="gray", linestyle="--")
plt.show()
```

### Named Entity Recognition (NER)

| Tool | Language | Strengths | Notes |
|------|----------|----------|-------|
| spaCy | Python | Fast, accurate, multiple languages | Best general-purpose NER |
| NLTK | Python | Educational, well-documented | Older, less accurate than spaCy |
| Stanza (Stanford NLP) | Python | Research-grade, many languages | Good for non-English texts |
| Flair | Python | State-of-the-art, flexible | Can fine-tune for historical text |
| BookNLP | Python/Java | Designed for literary texts | Character identification, coreference |

**Fine-tuning NER for historical texts:** Pre-trained NER models are trained on modern text (news articles, Wikipedia) and perform poorly on historical text with archaic spelling, different naming conventions, and unfamiliar entities. Fine-tuning on manually annotated historical text dramatically improves accuracy.

```python
import spacy
from spacy.training import Example

# Load base model
nlp = spacy.load("en_core_web_sm")

# Prepare training data (manually annotated historical text)
TRAIN_DATA = [
    ("Mr. Darcy arrived at Pemberley in the autumn of 1811.",
     {"entities": [(0, 10, "PERSON"), (22, 31, "LOC"), (50, 54, "DATE")]}),
    ("The East India Company dispatched three vessels from Calcutta.",
     {"entities": [(4, 22, "ORG"), (53, 61, "LOC")]}),
]

# Fine-tune the NER component
# (simplified -- production code needs more examples and proper training loop)
```

## Corpus Linguistics

### Concordance (KWIC)

A concordance displays every occurrence of a search term in its immediate context (typically 5-10 words on each side), creating a Key Word in Context (KWIC) view. This reveals patterns of usage, collocates, and semantic prosody.

**Example: KWIC concordance for "liberty" in 18th-century political texts**

```
...the natural  LIBERTY  of mankind is to be free from...
...that civil   LIBERTY  consists in the security of...
...enemies of   LIBERTY  who would enslave the nation...
...religious    LIBERTY  and freedom of conscience...
...took up arms for  LIBERTY  against tyrannical oppression...
```

Patterns visible: "liberty" collocates with "natural," "civil," "religious" — different conceptual frames for the same word.

### Collocation

Collocation analysis identifies words that co-occur with a target word more frequently than chance would predict.

| Measure | Favors | Best For |
|---------|--------|----------|
| MI (Mutual Information) | Rare, exclusive collocates | Finding fixed phrases |
| t-score | Frequent collocates | Common usage patterns |
| Log-likelihood (G2) | Statistically significant collocates | Balanced analysis |
| Log Dice | Stable across corpus sizes | Comparing corpora |

### Frequency and Keyness

**Word frequency** counts how often each word appears (raw, normalized per million words, or relative). **Keyness** compares word frequencies between two corpora to identify words statistically over- or under-represented in one relative to the other, revealing what is distinctive.

**Example: Keyness comparing male vs. female authored Victorian novels**

```
Words overrepresented in female-authored novels:
  she, her, room, mother, child, dress, felt, tears, home

Words overrepresented in male-authored novels:
  he, his, money, business, gentleman, sir, political, war

Interpretation: Keyness analysis reveals gendered thematic emphases
in Victorian fiction, with female authors more frequently writing about
domestic spaces and emotional states, and male authors more frequently
addressing public life and commerce. However, these are statistical
tendencies, not absolute divisions -- individual authors cross these
patterns in interesting ways.
```

**Corpus linguistics software:**

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| AntConc | Desktop application | Free | Concordance, collocation, keyness |
| Voyant Tools | Web-based | Free | Quick visualization, no installation |
| Sketch Engine | Web-based | Paid (free for academics) | Large corpora, SketchDiff |
| CQPweb | Web-based | Free (institutional) | Corpus query language |
| NLTK | Python library | Free | Programmable analysis |
| quanteda | R package | Free | Statistical text analysis |

## Digital Archives and Metadata

### Dublin Core — the 15 elements

| Element | Description | Example |
|---------|-------------|---------|
| Title | Name of the resource | "Letter from Thomas Jefferson to John Adams" |
| Creator | Entity primarily responsible | "Jefferson, Thomas" |
| Subject | Topic of the resource | "American politics; Enlightenment philosophy" |
| Description | Account of the resource | "Personal letter discussing agrarian policy..." |
| Publisher | Entity making resource available | "Library of Congress" |
| Contributor | Entity contributing to the resource | "Adams, John (recipient)" |
| Date | Date associated with the resource | "1812-06-11" |
| Type | Nature or genre | "Text; Correspondence" |
| Format | Physical or digital format | "image/tiff; 2 pages" |
| Identifier | Unambiguous reference | "loc.gov/item/mtjbib024567" |
| Source | Derived-from resource | "Thomas Jefferson Papers, Series 1" |
| Language | Language of the resource | "en" |
| Relation | Related resources | "Reply to Adams letter of 1812-05-28" |
| Coverage | Spatial or temporal coverage | "Monticello, Virginia; 1812" |
| Rights | Rights information | "Public domain" |

### TEI XML

The Text Encoding Initiative (TEI) provides an XML-based standard for encoding literary, historical, and linguistic texts with rich structural and interpretive markup. TEI is the standard for digital scholarly editions.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Letter from Mary Shelley to Leigh Hunt</title>
        <author>Shelley, Mary Wollstonecraft, 1797-1851</author>
        <editor>Digital editor name</editor>
      </titleStmt>
      <publicationStmt>
        <publisher>Digital Archive Name</publisher>
        <date>2026</date>
        <availability>
          <licence target="https://creativecommons.org/licenses/by/4.0/">
            CC-BY 4.0
          </licence>
        </availability>
      </publicationStmt>
      <sourceDesc>
        <msDesc>
          <msIdentifier>
            <repository>Bodleian Library</repository>
            <idno>MS. Shelley c.1, f.234</idno>
          </msIdentifier>
        </msDesc>
      </sourceDesc>
    </fileDesc>
  </teiHeader>
  <text>
    <body>
      <opener>
        <dateline><placeName>Genoa</placeName>,
          <date when="1823-02-15">15 February 1823</date>
        </dateline>
        <salute>My dear <persName ref="#hunt">Hunt</persName>,</salute>
      </opener>
      <p>I write to you in great haste, having just received
        your letter from <placeName ref="#london">London</placeName>.
        The news of <persName ref="#byron">Lord Byron</persName>'s
        departure for <placeName ref="#greece">Greece</placeName>
        has left us all in a state of considerable anxiety.</p>
      <closer>
        <salute>Yours most affectionately,</salute>
        <signed><persName ref="#mshelley">Mary Shelley</persName></signed>
      </closer>
    </body>
  </text>
</TEI>
```

**Key TEI elements for humanities encoding:**

| Element | Purpose | Example Use |
|---------|---------|-------------|
| `<persName>` | Personal name | Tagging historical figures |
| `<placeName>` | Place name | Geographic references |
| `<date>` | Date (with @when for normalization) | Temporal references |
| `<note>` | Editorial annotation | Footnotes, commentary |
| `<app>` and `<rdg>` | Apparatus (textual variants) | Critical editions |
| `<del>` and `<add>` | Deletions and additions | Manuscript editing |
| `<unclear>` | Uncertain reading | Damaged or illegible text |
| `<gap>` | Omitted material | Lost or censored text |
| `<choice>` | Alternative encodings | Original/regularized spelling |

## GIS for Historical Research

**Common applications:** historical mapping (georeferencing old maps), event mapping, trade-route analysis, literary geography, urban history, environmental history, archaeological site mapping.

**GIS tools for humanities:**

| Tool | Type | Cost | Best For |
|------|------|------|----------|
| QGIS | Desktop | Free | Full GIS functionality, open source |
| ArcGIS | Desktop + cloud | Paid (free for students) | Industry standard, extensive tools |
| Google Earth Pro | Desktop | Free | Visualization, KML import |
| Palladio | Web-based | Free | Network + map visualization for humanities |
| Mapbox | Web + API | Free tier | Custom interactive web maps |
| Leaflet | JavaScript library | Free | Lightweight web maps |
| kepler.gl | Web-based | Free | Large-scale geospatial data visualization |

**Example: Georeferencing a historical map (QGIS)**

```
1. Load the scanned historical map as a raster layer
2. Add a modern basemap (OpenStreetMap) for reference
3. Identify Ground Control Points (GCPs) -- locations identifiable
   on both the historical map and modern basemap
4. Place at least 4 GCPs (more is better, spread across the map)
5. Choose a transformation type:
   - Linear: 3 GCPs minimum (shift, rotate, scale)
   - Polynomial 1: 3 GCPs minimum (affine transformation)
   - Polynomial 2: 6 GCPs minimum (handles distortion)
   - Thin Plate Spline: many GCPs (flexible, handles local distortion)
6. Run the transformation and inspect the result
7. Save the georeferenced map with spatial reference metadata
```

## Network Analysis for Historical Figures

**Types of historical networks:**

| Network Type | Nodes | Edges | Example |
|-------------|-------|-------|---------|
| Correspondence | People | Letters exchanged | Republic of Letters network |
| Co-occurrence | People | Mentioned in same document | Colonial administration officials |
| Citation | Texts/authors | One cites another | Intellectual influence networks |
| Kinship | People | Family relations | Dynastic networks |
| Trade | Places/merchants | Commercial exchange | Mediterranean trade network |
| Organizational | People/orgs | Membership/affiliation | Reform movement networks |

**Building a historical network from archival sources:**

```
Step 1: Define nodes and edges
  - What counts as a node? (person, place, text, organization)
  - What counts as an edge? (letter, co-occurrence, citation, transaction)
  - Is the edge directed or undirected?
  - What edge attributes to record? (date, type, weight)

Step 2: Extract data from sources
  - Manual extraction from archival documents
  - Semi-automated extraction using NER on digitized texts
  - Structured databases (EMLO for early modern letters, SNAP for prosopography)

Step 3: Create edge list
  Format: Source, Target, Weight, Date, Type
  "Jefferson", "Adams", 1, "1812-06-11", "letter"
  "Jefferson", "Madison", 1, "1812-06-15", "letter"

Step 4: Analyze in Gephi, NetworkX, or igraph
  - Calculate centrality measures
  - Detect communities (Louvain, modularity)
  - Visualize with meaningful layout (ForceAtlas2, geographic)
  - Filter by time period for temporal analysis
```

## Stylometry and Authorship Attribution

**Key stylometric features:**

| Feature | Description | Why It Works |
|---------|-------------|-------------|
| Function word frequencies | the, of, and, to, a, in, is, it | Unconscious, content-independent |
| Word length distribution | Average and variance of word lengths | Reflects vocabulary preferences |
| Sentence length | Average and variance | Reflects syntactic habits |
| Vocabulary richness | Type-token ratio, hapax legomena | Lexical diversity |
| Character n-grams | Sequences of n characters | Captures sub-word patterns |
| POS tag n-grams | Sequences of part-of-speech tags | Syntactic patterns |

**Stylometry tools:**

| Tool | Language | Method | Best For |
|------|----------|--------|----------|
| Stylo (R package) | R | Delta, PCA, cluster analysis | Literary stylometry |
| JGAAP | Java | Multiple classifiers | General authorship attribution |
| PyDelta | Python | Burrows Delta variants | Python-based workflows |
| Signature | Web-based | Visualization | Quick exploration |

**Burrows Delta method** (Burrows, 2002) is the most widely used stylometric method, measuring the "distance" between texts based on z-scores of the most frequent words:

```
Algorithm:
1. Select the n most frequent words across all texts (typically 100-500)
2. For each word, calculate z-scores across all texts
3. For each pair of texts, calculate the mean absolute difference
   of z-scores (this is Delta)
4. The text with the smallest Delta to the anonymous text is the
   most likely author

Variants:
- Classic Delta (Burrows, 2002): Mean absolute z-score difference
- Cosine Delta (Wurzburg group): Cosine distance on z-scores
- Eder Delta: Emphasis on very frequent words
- Argamon Linear Delta: Manhattan distance
```

**Example: Stylometric analysis in R (stylo package)**

```r
library(stylo)

# Place texts in corpus/ subdirectory
# Filename format: AuthorName_TextTitle.txt

# Run cluster analysis
results <- stylo(
  gui = FALSE,
  corpus.dir = "corpus",
  corpus.lang = "English",
  mfw.min = 100,        # Minimum most frequent words
  mfw.max = 500,        # Maximum most frequent words
  mfw.incr = 100,       # Increment
  analysis.type = "CA", # Cluster Analysis
  distance.measure = "wurzburg",  # Cosine Delta
  write.png.file = TRUE
)
```

## OCR Workflows

**OCR tools comparison:**

| Tool | Type | Best For | Languages | Historical Text |
|------|------|----------|-----------|----------------|
| Tesseract | Open source | General purpose | 100+ | Moderate (needs training) |
| Kraken | Open source | Historical/non-Latin scripts | Many | Excellent (designed for it) |
| Transkribus | Free platform | Handwritten text (HTR) | Many | Excellent |
| ABBYY FineReader | Commercial | High-volume production | Many | Good |
| Google Cloud Vision | API | Large-scale, cloud | Many | Good |
| Amazon Textract | API | Structured documents | English primarily | Moderate |

**OCR workflow for historical documents:**

```
1. IMAGE PREPARATION
   - Scan at 300-400 DPI minimum (600 DPI for small text)
   - Use grayscale or binary (not color unless needed)
   - Deskew rotated pages
   - Crop to text area
   - Binarize (convert to black and white) using adaptive thresholding

2. OCR PROCESSING
   - Select appropriate engine and language model
   - For historical text: use period-appropriate training data if available
   - Process page by page
   - Maintain page/document structure

3. POST-PROCESSING
   - Spell-check against period-appropriate dictionaries
   - Correct common OCR errors (rn -> m, cl -> d, etc.)
   - Validate against spot-checks of original images
   - Preserve original line/page breaks in metadata

4. QUALITY ASSESSMENT
   - Character Error Rate (CER): % of characters incorrectly recognized
   - Word Error Rate (WER): % of words with at least one error
   - Acceptable CER for research: < 5% (ideally < 2%)
   - Always report OCR quality in publications using the data
```

**Tesseract command-line example:**

```bash
# Basic OCR
tesseract input.tiff output -l eng

# With page segmentation mode for single column
tesseract input.tiff output -l eng --psm 6

# With custom trained model for historical English
tesseract input.tiff output -l eng_hist --psm 6 --oem 1
```

## Digital Scholarly Editions

**Components:** transcription, TEI encoding, apparatus (textual variants), annotation, facsimile images, full-text search, visualization, stable/persistent identifiers.

**Digital edition platforms:**

| Platform | Type | Best For |
|----------|------|----------|
| Edition Visualization Technology (EVT) | Open source | TEI-based critical editions |
| Versioning Machine | Open source | Parallel text comparison |
| TextGrid | Platform | German-language editions |
| FromThePage | Web platform | Collaborative transcription |
| Scripto | Plugin (Omeka) | Crowdsourced transcription |
| IIIF (protocol) | Standard | Interoperable image delivery |

## Data Visualization for Humanities

| Tool | Best For | Output |
|------|----------|--------|
| Palladio | Historical data (maps, networks, timelines) | Interactive web |
| Gephi | Network visualization | Static images, interactive (via plugins) |
| Voyant Tools | Text visualization (word clouds, trends, contexts) | Interactive web |
| StoryMapJS | Narrative maps | Interactive web |
| TimelineJS | Chronological narratives | Interactive web |
| Flourish | General data storytelling | Interactive web |
| RAWGraphs | Unconventional chart types | SVG export |
| D3.js | Custom interactive visualizations | Web (requires JavaScript) |
| matplotlib/seaborn | Statistical plots | Static images |

**Visualization principles for humanities data:**

1. **Uncertainty is data** — Historical and humanities data are often incomplete, ambiguous, or contested. Represent uncertainty explicitly (confidence intervals, fuzzy boundaries, missing-data indicators).
2. **Context over decoration** — Every visual element should serve an analytical purpose.
3. **Narrative integration** — Visualizations belong inside interpretive arguments, not presented as self-explanatory evidence.
4. **Accessibility** — Use colorblind-safe palettes, provide alt text, ensure screen reader compatibility.
5. **Reproducibility** — Document data sources, processing steps, and visualization parameters.

## Distant Reading

Distant reading (Moretti 2005, 2013) analyzes large numbers of texts through quantitative and computational methods rather than close reading a few canonical works.

**Key methods:** quantitative genre analysis, title analysis, plot-structure analysis (sentiment trajectories), geographic imagination (mapping novel settings), character network analysis, stylistic change over literary history.

**Moretti's key arguments:**
- The literary canon is a tiny fraction of published literature — we need methods for the "great unread"
- Quantitative patterns reveal structures invisible to close reading
- Literary forms evolve through mechanisms analogous to biological evolution (variation, selection, drift)
- Maps, graphs, and trees are analytical tools, not mere illustrations

## Cultural Analytics

Cultural analytics (Manovich 2020) applies computational analysis to large collections of cultural artifacts — images, video, music, design, social media — extending distant reading beyond text.

**Methods:** image analysis (color histograms, composition, object detection), time series of visual features, media visualization (composite-image displays), social media analytics, interface analysis.

**Python tools:**

| Library | Purpose |
|---------|---------|
| OpenCV | Image processing, feature extraction |
| Pillow (PIL) | Image manipulation |
| scikit-image | Scientific image analysis |
| face_recognition | Face detection and recognition |
| ImageAI | Object detection |
| matplotlib / seaborn | Visualization |
| plotly | Interactive visualization |

## Python Tools for Humanities Computing

**spaCy — industrial-strength NLP:**

```python
import spacy

# Load English model
nlp = spacy.load("en_core_web_sm")

# Process text
doc = nlp("Mary Shelley wrote Frankenstein in Geneva in 1816.")

# Named entities
for ent in doc.ents:
    print(f"{ent.text} -> {ent.label_}")
# Mary Shelley -> PERSON
# Frankenstein -> WORK_OF_ART
# Geneva -> GPE
# 1816 -> DATE

# Part-of-speech tags
for token in doc:
    print(f"{token.text}: {token.pos_} ({token.dep_})")

# Sentence segmentation, dependency parsing, lemmatization
```

**NLTK — Natural Language Toolkit:**

```python
import nltk
from nltk.corpus import gutenberg
from nltk import FreqDist, ConditionalFreqDist

# Load a Gutenberg text
text = gutenberg.words("austen-emma.txt")

# Frequency distribution
fdist = FreqDist(text)
fdist.most_common(20)

# Concordance
from nltk.text import Text
emma = Text(text)
emma.concordance("marriage", width=80, lines=10)

# Collocations
emma.collocations()
```

**Voyant Tools (no-code):** browser-based text analysis (voyant-tools.org) — upload texts or URLs for word clouds, frequency graphs, KWIC concordances, trends, collocates, document similarity clustering, and embeddable visualizations.

**AntConc (desktop corpus tool):** (laurenceanthony.net/software/antconc) — KWIC concordance with sorting, collocation with multiple statistical measures, word/keyword frequency lists, n-grams, keyness comparison, and dispersion plots.

## Best Practices

### Starting a Digital Humanities Project

1. **Start with a humanistic question** — Technology is a means, not an end. What do you want to know about culture, history, or language?
2. **Choose the simplest tool that works** — Voyant Tools and AntConc answer many questions without programming.
3. **Learn iteratively** — Begin with existing tools and add technical skills as needed.
4. **Document everything** — Record every decision about corpus construction, preprocessing, parameter selection, and interpretation.
5. **Validate computationally derived patterns with close reading** — Distant and close reading are complementary, not competing.

### Data Quality and Preparation

1. **Corpus construction is an argument** — What you include and exclude shapes results. Document and justify corpus boundaries.
2. **OCR quality matters** — Always assess and report OCR error rates. Garbage in, garbage out.
3. **Metadata is essential** — Author, date, genre, publication context contextualize computational findings.
4. **Preprocessing choices are analytical choices** — Lemmatization, stop-word removal, and tokenization all affect results. Report what you did.
5. **Preserve originals** — Never modify source data. Keep raw and processed versions separate.

### Interpretation and Argumentation

1. **Computational results require interpretation** — A topic model does not speak for itself.
2. **Visualizations are arguments** — Be explicit about what each visualization chooses to show.
3. **Acknowledge limitations** — Discuss what your method cannot capture.
4. **Engage with disciplinary debates** — Situate findings within existing humanistic scholarship.
5. **Collaborate** — DH benefits from collaboration between domain experts and technical specialists.

## Common Pitfalls

**Text mining:** black-box use of NLP tools; anachronistic analysis (modern sentiment models on historical corpora without validation); overclaiming from topics (co-occurrence is not "meaning"); ignoring preprocessing effects.

**Corpus linguistics:** small corpus, big claims; frequency without context (always read concordance lines); ignoring genre and register effects.

**GIS and mapping:** false precision (exact modern coordinates for historical locations); projection distortion; empty maps (absence of data is not absence of activity).

**Stylometry:** insufficient text length (minimum 2,000-5,000 words per sample); genre contamination; circular reasoning (training on the disputed text then attributing it).

## References

- Moretti, F. (2005). *Graphs, Maps, Trees: Abstract Models for Literary History*. Verso.
- Moretti, F. (2013). *Distant Reading*. Verso.
- Manovich, L. (2020). *Cultural Analytics*. MIT Press.
- Jockers, M. L. (2013). *Macroanalysis: Digital Methods and Literary History*. University of Illinois Press.
- Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet Allocation. *Journal of Machine Learning Research*, 3, 993-1022.
- Grootendorst, M. (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure. *arXiv preprint*, arXiv:2203.05794.
- Burrows, J. (2002). Delta: A measure of stylistic difference and a guide to likely authorship. *Literary and Linguistic Computing*, 17(3), 267-287.
- Burnard, L., & Bauman, S. (Eds.). (2023). *TEI P5: Guidelines for Electronic Text Encoding and Interchange*. Text Encoding Initiative Consortium.
- Bodenhamer, D. J., Corrigan, J., & Harris, T. M. (Eds.). (2010). *The Spatial Humanities: GIS and the Future of Humanities Scholarship*. Indiana University Press.
- Graham, S., Milligan, I., & Weingart, S. (2015). *Exploring Big Historical Data: The Historian's Macroscope*. Imperial College Press.
