# Digital Humanities Tools Guide -- Reference

## Text Analysis Tool Comparison Matrix

### NLP Libraries for Humanities Research

| Feature | spaCy | NLTK | Stanza | Flair | BookNLP |
|---------|-------|------|--------|-------|---------|
| Speed | Very fast | Moderate | Moderate | Slow (GPU helps) | Moderate |
| NER accuracy | High | Moderate | High | Very high | High (literary) |
| Languages | 25+ | 20+ | 66+ | 20+ | English |
| Dependency parsing | Yes | Limited | Yes | No | Yes |
| Coreference | Experimental (separate `spacy-experimental` pkg, `en_coreference_web_trf`; not in core `en_core_web_*` pipelines) | No | No | No | Yes |
| Sentiment | No (use extension) | Yes (VADER) | Yes | Yes | No |
| Ease of use | Easy | Easy | Easy | Moderate | Easy |
| Character detection | No | No | No | No | Yes |
| GPU support | Yes | No | Yes | Yes | Yes |
| Historical text | Needs fine-tuning | Needs fine-tuning | Needs fine-tuning | Good (fine-tunable) | Modern text only |

### Topic Modeling Parameters Guide

**LDA Parameter Tuning:**

| Parameter | Description | Recommended Range | Effect |
|-----------|-------------|------------------|--------|
| k (num_topics) | Number of topics | 10-100 | Too few = overly broad; too many = redundant |
| alpha | Document-topic density | 50/k or "auto" | Lower = documents have fewer topics |
| eta (beta) | Topic-word density | 0.01 or "auto" | Lower = topics have fewer words |
| iterations | Training iterations | 500-2000 | More = better convergence |
| passes | Passes through corpus | 10-20 | More = better quality |
| chunk_size | Documents per batch | 100-2000 | Affects memory and speed |

**LDA Implementation in Python (Gensim):**

```python
from gensim import corpora, models
from gensim.models import CoherenceModel
import pyLDAvis.gensim_models

# Prepare corpus
dictionary = corpora.Dictionary(tokenized_texts)
dictionary.filter_extremes(no_below=5, no_above=0.5)
corpus = [dictionary.doc2bow(text) for text in tokenized_texts]

# Find optimal number of topics
coherence_scores = []
for k in range(5, 55, 5):
    lda = models.LdaMulticore(
        corpus=corpus,
        id2word=dictionary,
        num_topics=k,
        passes=15,
        iterations=1000,
        random_state=42,
        workers=3
    )
    coherence = CoherenceModel(
        model=lda,
        texts=tokenized_texts,
        dictionary=dictionary,
        coherence="c_v"
    ).get_coherence()
    coherence_scores.append((k, coherence))
    print(f"k={k}: coherence={coherence:.4f}")

# Train final model with best k
best_k = max(coherence_scores, key=lambda x: x[1])[0]
lda_model = models.LdaMulticore(
    corpus=corpus,
    id2word=dictionary,
    num_topics=best_k,
    passes=20,
    iterations=1500,
    random_state=42
)

# Interactive visualization
vis = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, "lda_visualization.html")
```

**BERTopic Implementation:**

```python
from bertopic import BERTopic
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer

# Custom vectorizer for humanities text
vectorizer = CountVectorizer(
    stop_words="english",
    min_df=5,
    max_df=0.95,
    ngram_range=(1, 2)
)

# Embedding model (multilingual option for non-English)
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize BERTopic
topic_model = BERTopic(
    embedding_model=embedding_model,
    vectorizer_model=vectorizer,
    min_topic_size=10,
    nr_topics="auto",
    top_n_words=15,
    calculate_probabilities=True
)

# Fit and transform
topics, probs = topic_model.fit_transform(documents)

# Get topic information
print(topic_model.get_topic_info())

# Visualize
topic_model.visualize_barchart(top_n_topics=15)
topic_model.visualize_heatmap()
topic_model.visualize_hierarchy()

# Topics over time (requires timestamps)
topics_over_time = topic_model.topics_over_time(
    documents, timestamps, nr_bins=20
)
topic_model.visualize_topics_over_time(topics_over_time)
```

## Corpus Linguistics Reference

### AntConc Quick Reference

**File menu:**
- Open File(s): Load individual text files
- Open Dir: Load all files in a directory
- File types: .txt (plain text, UTF-8 recommended)

**Tool tabs:**

| Tab | Function | Key Settings |
|-----|----------|-------------|
| Concordance | KWIC display | Search term, context window, sort (L1, R1, etc.) |
| Concordance Plot | Dispersion visualization | Shows where term appears across text |
| File View | Full text view | Click concordance line to see full context |
| Clusters/N-Grams | Multi-word units | Min/max length, frequency threshold |
| Collocates | Co-occurring words | Window size (L5-R5), stat measure (MI, t-score) |
| Word List | Frequency lists | Alphabetical or frequency order |
| Keyword List | Keyness comparison | Reference corpus required, stat measure |

**Search operators in AntConc:**

| Operator | Meaning | Example |
|----------|---------|---------|
| * | Wildcard (any characters) | libert* matches liberty, liberties, liberation |
| ? | Single character wildcard | wom?n matches woman, women |
| \| | OR | king\|queen matches either |
| _ | Space (in n-grams) | in_the matches "in the" |
| @file | Use word list file | @positive_words.txt |

### Voyant Tools Panel Reference

**Default panels (Skin: Default):**

| Panel | Shows | Use For |
|-------|-------|---------|
| Cirrus | Word cloud | Quick overview of frequent terms |
| Reader | Full text with highlights | Close reading with computational support |
| Trends | Line graph of word frequency | Tracking terms across documents/segments |
| Summary | Corpus statistics | Document lengths, vocabulary size, distinctive words |
| Contexts | KWIC concordance | Examining word usage in context |

**Advanced panels:**

| Panel | Shows | Use For |
|-------|-------|---------|
| Topics | Topic model results | Unsupervised thematic analysis |
| Bubblelines | Term distribution across documents | Comparing term usage patterns |
| TermsBerry | Interactive term exploration | Visual collocation analysis |
| StreamGraph | Stacked frequency over time | Visualizing thematic evolution |
| Mandala | Radial term distribution | Document-level term patterns |
| MicroSearch | Miniature concordance plots | Quick dispersion overview |
| TextualArc | Circular text visualization | Narrative structure visualization |
| Knots | Co-occurrence visualization | Relationship between terms |

### Frequency and Statistical Measures

**Frequency measures:**

| Measure | Formula | Use |
|---------|---------|-----|
| Raw frequency | Count of occurrences | Basic counting |
| Normalized frequency | (Raw freq / Total words) * 1,000,000 | Comparing across corpora of different sizes |
| Relative frequency | Raw freq / Total words | Proportion |
| TF-IDF | tf * log(N/df) | Important words in a document vs. corpus |

**Association measures for collocation:**

| Measure | Favors | Interpretation |
|---------|--------|---------------|
| MI (Mutual Information) | Rare, exclusive pairs | > 3 = strong collocation |
| MI2 | Slightly less rare-favoring | Balanced measure |
| t-score | Frequent, reliable pairs | > 2 = significant |
| z-score | Medium-frequency pairs | > 3.29 = significant (p < .001) |
| Log-likelihood (G2) | Statistically robust | > 3.84 = p < .05; > 10.83 = p < .001 |
| Log Dice | Comparable across corpus sizes | 0-14 scale, higher = stronger |
| Delta P | Directional association | -1 to 1, direction of prediction |

## OCR Processing Reference

### Tesseract Configuration

**Page Segmentation Modes (PSM):**

| Mode | Description | Use Case |
|------|-------------|----------|
| 0 | Orientation and script detection only | Identifying script/rotation |
| 1 | Automatic page segmentation with OSD | General documents |
| 3 | Fully automatic page segmentation (default) | Most documents |
| 4 | Assume single column of variable sizes | Single-column text |
| 6 | Assume single uniform block of text | Dense text blocks |
| 7 | Treat image as a single text line | Captions, headings |
| 8 | Treat image as a single word | Labels, stamps |
| 11 | Sparse text, no particular order | Scattered text on images |
| 13 | Raw line, treat as single line | No Tesseract grouping |

**OCR Engine Modes (OEM):**

| Mode | Description |
|------|-------------|
| 0 | Legacy engine only |
| 1 | Neural nets LSTM engine only |
| 2 | Legacy + LSTM engines |
| 3 | Default (based on available models) |

**Image preprocessing for better OCR:**

```python
import cv2
import numpy as np

def preprocess_for_ocr(image_path):
    # Read image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Deskew
    coords = np.column_stack(np.where(gray > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = gray.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    gray = cv2.warpAffine(gray, M, (w, h),
                          flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)
    
    # Adaptive thresholding (binarization)
    binary = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        blockSize=11,
        C=2
    )
    
    # Noise removal
    kernel = np.ones((1, 1), np.uint8)
    clean = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    clean = cv2.morphologyEx(clean, cv2.MORPH_OPEN, kernel)
    
    return clean
```

### Kraken for Historical Documents

Kraken is specifically designed for historical and non-Latin script documents:

```bash
# Segment the page into text lines
kraken -i input.png output.json segment -bl

# Recognize text using a pre-trained model
kraken -i input.png output.txt ocr -m en_best.mlmodel

# Train a custom model on ground truth data
ketos train -f alto *.xml -o my_model

# Fine-tune an existing model
ketos train -f alto *.xml -o my_finetuned --load en_best.mlmodel
```

**Available Kraken models:**
- Visit https://zenodo.org/communities/ocr_models for pre-trained models
- Models available for: Latin scripts (many periods), Arabic, Hebrew, Greek, Syriac, Ethiopic, and many more

### Transkribus for Handwritten Text

Transkribus uses Handwritten Text Recognition (HTR):

1. Upload document images
2. Perform layout analysis (automatic or manual correction)
3. Select or train an HTR model
4. Run recognition
5. Correct results using the built-in editor
6. Export as TEI XML, PDF, or plain text

**Public HTR models in Transkribus:**
- English Writing M1 (18th-20th century English handwriting)
- German Kurrent/Fraktur models
- French handwriting models
- Latin manuscript models
- Mixed print/handwriting models

## TEI XML Quick Reference

### Essential TEI Elements

**Document structure:**

```xml
<TEI>
  <teiHeader>...</teiHeader>  <!-- Metadata -->
  <text>
    <front>...</front>          <!-- Title page, preface -->
    <body>...</body>            <!-- Main text -->
    <back>...</back>            <!-- Appendices, index -->
  </text>
</TEI>
```

**Text division:**

```xml
<div type="chapter" n="1">
  <head>Chapter Title</head>
  <p>Paragraph text...</p>
  <p>Another paragraph...</p>
</div>
```

**Critical apparatus (parallel segmentation):**

```xml
<app>
  <lem wit="#A">original reading</lem>
  <rdg wit="#B">variant reading</rdg>
  <rdg wit="#C">another variant</rdg>
</app>
```

**Manuscript description:**

```xml
<msDesc>
  <msIdentifier>
    <settlement>Oxford</settlement>
    <repository>Bodleian Library</repository>
    <idno>MS. Bodl. 264</idno>
  </msIdentifier>
  <msContents>
    <summary>14th-century copy of Alexander Romance</summary>
  </msContents>
  <physDesc>
    <objectDesc>
      <supportDesc material="parchment">
        <extent>224 folios</extent>
      </supportDesc>
    </objectDesc>
    <handDesc>
      <handNote>Gothic bookhand</handNote>
    </handDesc>
  </physDesc>
  <history>
    <origin>
      <origDate notBefore="1338" notAfter="1344">c. 1338-1344</origDate>
      <origPlace>Flanders</origPlace>
    </origin>
  </history>
</msDesc>
```

## GIS for Humanities Reference

### QGIS Workflow for Historical Mapping

**Step-by-step georeferencing:**

```
1. Open QGIS
2. Add a modern basemap:
   - Web > QuickMapServices > OpenStreetMap
   (Install QuickMapServices plugin if needed)

3. Load historical map:
   - Layer > Add Layer > Add Raster Layer
   - Navigate to scanned map file

4. Open Georeferencer:
   - Raster > Georeferencer
   - Load the historical map raster

5. Add Ground Control Points (GCPs):
   - Click a recognizable point on historical map
   - Click corresponding point on modern basemap
   - Repeat for 6-20 points spread across the map

6. Configure transformation:
   - Settings > Transformation Settings
   - Type: Polynomial 2 or Thin Plate Spline
   - Resampling: Cubic
   - Target CRS: EPSG:4326 (WGS 84)

7. Run georeferencer:
   - File > Start Georeferencing
   - Result: georeferenced TIFF with world file
```

**Creating a historical events map:**

```
Data format (CSV):
event_name,date,latitude,longitude,description,source
"Battle of Waterloo","1815-06-18",50.6801,4.4115,"Coalition victory","Wellington Papers"
"Congress of Vienna","1815-06-09",48.2082,16.3738,"Final Act signed","Metternich correspondence"

QGIS steps:
1. Layer > Add Layer > Add Delimited Text Layer
2. Select CSV file
3. Set X field = longitude, Y field = latitude
4. Set CRS = EPSG:4326
5. Style points by category (battle, treaty, etc.)
6. Add labels from event_name field
7. Create temporal animation if dates span a range
```

## Stylometry Reference

### Stylo Package (R) Complete Guide

**Basic cluster analysis:**

```r
library(stylo)

# Files must be in corpus/ directory
# Named: AuthorLastname_Title.txt

# Cluster analysis with Cosine Delta
stylo(
  gui = FALSE,
  corpus.dir = "corpus",
  corpus.lang = "English",
  analyzed.features = "w",     # words (not characters)
  mfw.min = 100,               # min MFW
  mfw.max = 300,               # max MFW
  mfw.incr = 100,              # step size
  analysis.type = "CA",        # Cluster Analysis
  distance.measure = "wurzburg", # Cosine Delta
  write.png.file = TRUE,
  plot.custom.height = 10,
  plot.custom.width = 8
)
```

**Rolling stylometry (for collaborative texts):**

```r
library(stylo)

# Detect style changes within a single text
rolling.classify(
  gui = FALSE,
  corpus.dir = "corpus",
  primary.set = "corpus/training/",
  slice.size = 5000,          # window size in words
  slice.overlap = 4500,       # overlap between windows
  classification.method = "delta",
  write.png.file = TRUE
)
```

**Oppose function (distinctive features):**

```r
library(stylo)

# Find words distinctive of each group
oppose(
  gui = FALSE,
  primary.corpus.dir = "corpus/group_A/",
  secondary.corpus.dir = "corpus/group_B/",
  slice.size = 5000
)
```

## Recommended DH Project Workflows

### Small Project (solo researcher, existing tools)

```
1. Research question formulation
2. Corpus collection and organization
3. Text cleaning (manual or semi-automated)
4. Analysis with Voyant Tools or AntConc
5. Supplementary analysis with Excel/Google Sheets
6. Visualization with Palladio or Flourish
7. Write-up integrating close and distant reading
```

### Medium Project (small team, some programming)

```
1. Research question and project planning
2. Corpus construction with metadata schema
3. OCR processing (Tesseract/Kraken) if needed
4. Text preprocessing pipeline (Python/R)
5. Computational analysis (topic modeling, NER, network analysis)
6. Interactive visualization (D3.js, Leaflet)
7. Digital output (website, interactive visualization)
8. Traditional publication with computational supplement
```

### Large Project (funded, multi-year)

```
1. Grant-funded project with DH center support
2. TEI encoding of primary sources
3. Custom database and web application
4. Multiple computational analyses
5. Digital scholarly edition or archive
6. API for data access
7. Long-term preservation plan (IIIF, persistent identifiers)
8. Multiple publications (traditional + digital)
9. Training and workshops for scholarly community
```

## Further Reading and Resources

### Online Learning
- The Programming Historian: https://programminghistorian.org/ (peer-reviewed tutorials)
- DARIAH-Campus: https://campus.dariah.eu/ (European DH training)
- DH+Lib: https://acrl.ala.org/dh/ (Library perspectives on DH)
- Humanities Data Analysis (Karsdorp, Kestemont, Riddell): https://www.humanitiesdataanalysis.org/

### DH Centers and Organizations
- Alliance of Digital Humanities Organizations (ADHO): https://adho.org/
- centerNet (international network of DH centers): https://dhcenternet.org/
- Digital Humanities Quarterly: https://www.digitalhumanities.org/dhq/

### Key Journals
- Digital Scholarship in the Humanities (Oxford University Press)
- Digital Humanities Quarterly (open access)
- Journal of Cultural Analytics (open access)
- International Journal of Digital Humanities
- Journal of the Text Encoding Initiative
