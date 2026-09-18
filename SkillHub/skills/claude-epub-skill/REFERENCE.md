# Markdown to EPUB Skill - Technical Reference

Advanced technical documentation for extending and customizing the Markdown to EPUB skill.

## Module Overview

### `markdown_processor.py`

Core module for parsing markdown and extracting document structure.

#### Main Classes

**MarkdownProcessor**
```python
processor = MarkdownProcessor()
result = processor.process(markdown_content)
```

Methods:
- `process(markdown_content: str) -> Dict` - Parse markdown and extract structure
- `_extract_frontmatter(content: str) -> str` - Extract YAML frontmatter
- `_extract_metadata(content: str)` - Extract metadata from document headers
- `_parse_chapters(content: str) -> List[Chapter]` - Parse into chapters
- `_parse_sections(content: str, min_level: int) -> List[Section]` - Parse sections
- `_build_toc() -> List[Dict]` - Build table of contents
- `markdown_to_html(markdown_text: str) -> str` - Convert markdown to HTML
- `_render_inline(text: str) -> str` - Process inline elements (bold, italic, links)

#### Data Classes

**EbookMetadata**
```python
metadata = EbookMetadata(
    title="My Book",
    author="John Doe",
    language="en",
    date="2025-01-15",
    identifier="unique-id"
)
```

**Chapter**
```python
chapter = Chapter(
    title="Chapter 1",
    content="Introduction text...",
    sections=[Section(...), ...],
    anchor="chapter-1"
)
```

**Section**
```python
section = Section(
    title="Section 1.1",
    level=2,
    content="Section content...",
    anchor="section-1-1"
)
```

### `epub_generator.py`

EPUB file creation and management using ebooklib.

#### Main Classes

**EPUBGenerator**
```python
generator = EPUBGenerator(metadata)
success = generator.generate(chapters, output_path)
```

Methods:
- `generate(chapters: List[Chapter], output_path: str) -> bool` - Main generation method
- `_create_book()` - Initialize EPUB book object
- `_add_chapters()` - Add chapters to book
- `_render_chapter(chapter: Chapter) -> str` - Render chapter to XHTML
- `_render_content(content: str) -> str` - Render markdown content to HTML
- `_add_style()` - Add CSS styling
- `_add_toc()` - Generate table of contents
- `_write_epub(output_path: str)` - Write EPUB file to disk

**Default CSS**
- Embedded in `EPUBGenerator.DEFAULT_CSS`
- Customizable by subclassing
- Responsive design for all screen sizes

#### Convenience Functions

```python
# Create EPUB from markdown string
create_epub_from_markdown(
    markdown_content: str,
    output_path: str,
    title: Optional[str] = None,
    author: Optional[str] = None
) -> bool
```

## HTML/XHTML Generation

### Markdown to HTML Conversion

The `markdown_to_html()` method converts markdown to semantic HTML:

```python
markdown = "# Title\n\nSome **bold** text"
html = MarkdownProcessor.markdown_to_html(markdown)
# Returns: <h1>Title</h1>\n<p>Some <strong>bold</strong> text</p>
```

### Supported Elements

- **Headers** (H1-H6): `# to ######`
- **Emphasis**: `**bold**`, `*italic*`, `__bold__`, `_italic_`
- **Links**: `[text](url)`
- **Lists**: `- item`, `* item`, `1. item`
- **Code**: `` `inline` ``, ` ``` ` ` ` (blocks)
- **Blockquotes**: `> quote`
- **Horizontal Rules**: `---`, `***`, `___`

### Special Handling

- HTML escaping: `&`, `<`, `>`, `"`, `'` are automatically escaped
- Code blocks: Content is escaped and preserved as-is
- Paragraphs: Double newlines create new `<p>` tags
- Links: Properly encoded href attributes

## EPUB Structure

### Generated File Layout

```
metadata.opf          # Package metadata
nav.xhtml             # EPUB3 navigation
toc.ncx               # NCBI NCX (compatibility)
OEBPS/
├── chap_001.xhtml    # Chapter files
├── chap_002.xhtml
├── ...
├── style/
│   └── main.css      # Embedded stylesheet
└── [other resources]
```

### Metadata Fields

From `EbookMetadata`:
- **identifier**: Unique ID (auto-generated UUID if not provided)
- **title**: Book title (required)
- **language**: Language code (default: "en")
- **author**: Author name
- **date**: Publication date (optional)

### Navigation

- **NCX (Navigation Control File)**: For backward compatibility with older readers
- **NAV (EPUB3 Navigation Document)**: Standard for EPUB3 readers
- Automatic generation from chapter/section hierarchy

## Customization

### Extending the Classes

**Custom Styling**
```python
class CustomEPUBGenerator(EPUBGenerator):
    CUSTOM_CSS = """/* Your CSS here */"""

    def _add_style(self):
        # Custom styling logic
        super()._add_style()
```

**Custom Metadata**
```python
metadata = EbookMetadata()
metadata.title = "My Custom Title"
metadata.author = "Custom Author"
generator = EPUBGenerator(metadata)
```

**Custom HTML Rendering**
```python
class CustomProcessor(MarkdownProcessor):
    @staticmethod
    def markdown_to_html(markdown_text):
        # Custom conversion logic
        return html
```

### Adding New Markdown Features

1. Extend `markdown_to_html()` in `MarkdownProcessor`
2. Add parsing logic for new markdown syntax
3. Return proper HTML equivalent
4. Test with `test_epub_skill.py`

Example - Add strikethrough support:
```python
# In markdown_to_html()
text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
```

## Performance Considerations

### Large Documents
- Processing is O(n) where n = document length
- Memory usage: ~3-5x the markdown source size
- EPUB generation typically < 100ms for 100+ page documents

### Optimization Tips
1. **Batch processing**: Process multiple documents in one run
2. **Chapter splitting**: Break very large documents into smaller files
3. **Content optimization**: Remove unnecessary whitespace/formatting
4. **Lazy loading**: Generate EPUBs on-demand rather than precomputing

## Debugging

### Enable Debug Output

```python
import logging
logging.basicConfig(level=logging.DEBUG)

processor = MarkdownProcessor()
result = processor.process(markdown_content)
```

### Common Issues

**Empty chapters**
- Check that markdown has proper structure
- Verify no sections have completely empty content
- Use `_render_content()` to debug HTML output

**Invalid XHTML**
- Verify all tags are properly closed
- Check for unescaped special characters
- Use validator tools on generated EPUB

**Missing TOC**
- Ensure chapters/sections have proper headers
- Verify anchor generation works correctly
- Check that sections list is populated

## API Integration

### Using with Claude Skills

```python
# In your skill implementation
def generate_ebook(markdown_content, title=None, author=None):
    from epub_generator import create_epub_from_markdown

    success = create_epub_from_markdown(
        markdown_content,
        "output.epub",
        title=title,
        author=author
    )

    if success:
        # Return file_id or stream
        return read_epub_file("output.epub")
    else:
        return None
```

### File Handling

The skill can work with:
- Direct file paths
- File contents via Files API
- Markdown strings
- Chat message content

## Testing

### Unit Tests

```python
# Test markdown parsing
processor = MarkdownProcessor()
result = processor.process(test_markdown)
assert len(result['chapters']) == expected_count

# Test HTML generation
html = MarkdownProcessor.markdown_to_html(test_content)
assert '<h1>' in html
assert '<strong>' in html
```

### Integration Tests

```python
# Test end-to-end EPUB generation
success = create_epub_from_markdown(
    markdown_content,
    test_output_path,
    title="Test",
    author="Tester"
)
assert success
assert Path(test_output_path).exists()
```

### Test Coverage

Current test coverage:
- ✓ Markdown parsing with multiple header levels
- ✓ YAML frontmatter extraction
- ✓ HTML generation and escaping
- ✓ EPUB file creation
- ✓ Edge cases (empty content, special characters)
- ✓ Table of contents generation
- ✓ Large documents (100+ chapters)

## Version History

**v1.0.0** (Current)
- Initial release
- Full markdown to EPUB conversion
- YAML frontmatter support
- Automatic TOC generation
- EPUB3 compliance
- Complete test suite

## Future Roadmap

**v1.1.0** (Planned)
- Cover page generation
- Custom CSS templates
- Image embedding

**v2.0.0** (Future)
- Kindle format support (.mobi, .azw3)
- Advanced table support
- Footnotes and cross-references
- Experimental MCP integration for cover images

## Contributing

### Code Guidelines
- Follow PEP 8 style guide
- Add docstrings to all functions
- Include type hints
- Write tests for new features
- Update this reference documentation

### Adding Features
1. Create a feature branch
2. Implement with tests
3. Update SKILL.md and REFERENCE.md
4. Submit with test results

---

**Last Updated**: 2025-01-16
**Maintained By**: Skills Development Team
