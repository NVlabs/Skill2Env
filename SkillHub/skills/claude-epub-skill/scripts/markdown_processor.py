"""
Markdown processing module for converting markdown to EPUB-compatible structure.

This module handles:
- Parsing markdown into chapters and sections
- Converting markdown to HTML
- Extracting metadata and structure
- Building table of contents
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer, TextLexer
    from pygments.formatters import HtmlFormatter
    from pygments.util import ClassNotFound
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


class HeaderLevel(Enum):
    """Header hierarchy levels."""
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6


@dataclass
class Header:
    """Represents a markdown header."""
    level: HeaderLevel
    text: str
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            # Generate anchor from text
            self.anchor = re.sub(r'[^\w\s-]', '', self.text.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class Chapter:
    """Represents a chapter (H1 section)."""
    title: str
    content: str
    sections: List['Section']
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            self.anchor = re.sub(r'[^\w\s-]', '', self.title.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class Section:
    """Represents a section (H2-H6)."""
    title: str
    level: int
    content: str
    anchor: Optional[str] = None

    def __post_init__(self):
        if not self.anchor:
            self.anchor = re.sub(r'[^\w\s-]', '', self.title.lower())
            self.anchor = re.sub(r'[-\s]+', '-', self.anchor).strip('-')


@dataclass
class EbookMetadata:
    """Metadata for the ebook."""
    title: Optional[str] = None
    author: Optional[str] = "Unknown Author"
    language: str = "en"
    date: Optional[str] = None
    identifier: Optional[str] = None


class MarkdownProcessor:
    """Process markdown content into EPUB-compatible structure."""

    def __init__(self):
        """Initialize the markdown processor."""
        self.chapters: List[Chapter] = []
        self.metadata = EbookMetadata()
        self.front_matter: Dict[str, str] = {}

    def process(self, markdown_content: str) -> Dict:
        """
        Process markdown content into structured format.

        Args:
            markdown_content: Raw markdown text

        Returns:
            Dictionary containing chapters, metadata, and TOC
        """
        # Extract front matter if present
        content = self._extract_frontmatter(markdown_content)

        # Extract metadata from headers
        self._extract_metadata(content)

        # Parse content into chapters
        self.chapters = self._parse_chapters(content)

        # Build table of contents
        toc = self._build_toc()

        return {
            'chapters': self.chapters,
            'metadata': self.metadata,
            'toc': toc,
            'front_matter': self.front_matter
        }

    def _extract_frontmatter(self, content: str) -> str:
        """
        Extract YAML front matter if present.

        Args:
            content: Raw markdown content

        Returns:
            Markdown content without front matter
        """
        if not content.startswith('---'):
            return content

        # Find closing ---
        try:
            end_idx = content.index('---', 3)
            fm_text = content[3:end_idx].strip()

            # Parse simple key: value pairs
            for line in fm_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.front_matter[key.strip().lower()] = value.strip()

            # Update metadata from front matter
            if 'title' in self.front_matter:
                self.metadata.title = self.front_matter['title']
            if 'author' in self.front_matter:
                self.metadata.author = self.front_matter['author']
            if 'date' in self.front_matter:
                self.metadata.date = self.front_matter['date']
            if 'language' in self.front_matter:
                self.metadata.language = self.front_matter['language']

            return content[end_idx + 3:].lstrip()
        except ValueError:
            return content

    def _extract_metadata(self, content: str) -> None:
        """
        Extract metadata from document headers.

        Args:
            content: Markdown content
        """
        # If no title from front matter, use first H1
        if not self.metadata.title:
            h1_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if h1_match:
                self.metadata.title = h1_match.group(1).strip()

    def _parse_chapters(self, content: str) -> List[Chapter]:
        """
        Parse markdown into chapters.

        Chapters are delimited by H1 headers. Content between H1s
        becomes a chapter with potential subsections (H2-H6).

        Args:
            content: Markdown content

        Returns:
            List of Chapter objects
        """
        # First, remove code blocks to avoid matching headers inside them
        # We'll use a placeholder to mark where code blocks were
        code_blocks = []
        code_block_pattern = r'```[^\n]*\n.*?```'

        def save_code_block(match):
            code_blocks.append(match.group(0))
            return f'\n__CODE_BLOCK_{len(code_blocks)-1}__\n'

        content_no_code = re.sub(code_block_pattern, save_code_block, content, flags=re.DOTALL)

        # Split by H1 headers (now safe from code blocks)
        h1_pattern = r'^# (.+)$'
        chapters = []

        # Find all H1 headers and their positions in content WITHOUT code blocks
        h1_matches = list(re.finditer(h1_pattern, content_no_code, re.MULTILINE))

        if not h1_matches:
            # No chapters, treat entire content as single chapter
            if content.strip():
                sections = self._parse_sections(content, 2)  # Start from H2
                chapters.append(Chapter(
                    title="Untitled",
                    content="",
                    sections=sections
                ))
            return chapters

        # Process each chapter
        # We need to map positions from content_no_code back to original content
        for i, match in enumerate(h1_matches):
            title = match.group(1).strip()
            start_no_code = match.end()

            # Find next H1 or end of content
            if i + 1 < len(h1_matches):
                end_no_code = h1_matches[i + 1].start()
            else:
                end_no_code = len(content_no_code)

            # Get the chapter content from content_no_code
            chapter_content_no_code = content_no_code[start_no_code:end_no_code]

            # Restore code blocks
            def restore_code_block(match):
                idx = int(match.group(1))
                return code_blocks[idx]

            chapter_content = re.sub(r'__CODE_BLOCK_(\d+)__', restore_code_block, chapter_content_no_code).rstrip()

            # Parse sections within this chapter
            sections = self._parse_sections(chapter_content, 2)

            # Extract direct content (before first H2)
            direct_content = ""
            if sections:
                first_h2_pos = chapter_content.find('\n##')
                if first_h2_pos == -1:
                    direct_content = chapter_content
                else:
                    direct_content = chapter_content[:first_h2_pos].strip()
            else:
                direct_content = chapter_content

            chapters.append(Chapter(
                title=title,
                content=direct_content,
                sections=sections
            ))

        return chapters

    def _parse_sections(self, content: str, min_level: int = 2) -> List[Section]:
        """
        Parse sections from content (H2 and below).

        Args:
            content: Markdown content
            min_level: Minimum header level to parse (2-6)

        Returns:
            List of Section objects
        """
        sections = []

        # Build pattern for headers from min_level to 6
        header_pattern = r'^(#{' + str(min_level) + r',6}) (.+)$'
        matches = list(re.finditer(header_pattern, content, re.MULTILINE))

        if not matches:
            return sections

        for i, match in enumerate(matches):
            hashes = match.group(1)
            level = len(hashes)
            title = match.group(2).strip()
            start = match.end()

            # Find next header or end
            if i + 1 < len(matches):
                end = matches[i + 1].start()
            else:
                end = len(content)

            section_content = content[start:end].rstrip()

            sections.append(Section(
                title=title,
                level=level,
                content=section_content
            ))

        return sections

    def _build_toc(self) -> List[Dict]:
        """
        Build table of contents from chapters and sections.

        Returns:
            List of TOC entries with links and hierarchy
        """
        toc = []

        for chapter in self.chapters:
            chapter_entry = {
                'title': chapter.title,
                'anchor': chapter.anchor,
                'level': 1,
                'subsections': []
            }

            for section in chapter.sections:
                section_entry = {
                    'title': section.title,
                    'anchor': section.anchor,
                    'level': section.level
                }
                chapter_entry['subsections'].append(section_entry)

            toc.append(chapter_entry)

        return toc

    @staticmethod
    def markdown_to_html(markdown_text: str) -> str:
        """
        Convert markdown to HTML.

        This is a simplified converter for common markdown elements.

        Args:
            markdown_text: Markdown text

        Returns:
            HTML string
        """
        if not markdown_text or not markdown_text.strip():
            return "<p></p>"

        lines = markdown_text.split('\n')
        html_parts = []
        in_code_block = False
        code_block_content = []
        code_block_language = None
        in_table = False
        table_lines = []
        current_paragraph = []

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                if in_code_block:
                    # End code block
                    code_html = '\n'.join(code_block_content)
                    # Add line numbers and syntax highlighting
                    code_html = MarkdownProcessor._add_line_numbers_and_highlighting(
                        code_html, code_block_language
                    )
                    html_parts.append(code_html)
                    code_block_content = []
                    code_block_language = None
                    in_code_block = False
                else:
                    # Start code block
                    if current_paragraph:
                        paragraph_text = ' '.join(current_paragraph).strip()
                        if paragraph_text:
                            html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                        current_paragraph = []
                    # Extract language if specified
                    lang = line.strip()[3:].strip()
                    code_block_language = lang if lang else None
                    in_code_block = True
                continue

            if in_code_block:
                code_block_content.append(line)
                continue

            # Handle tables
            if '|' in line and line.strip().startswith('|') or (line.count('|') >= 2):
                if not in_table:
                    # Start table
                    if current_paragraph:
                        paragraph_text = ' '.join(current_paragraph).strip()
                        if paragraph_text:
                            html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                        current_paragraph = []
                    in_table = True
                table_lines.append(line)
                continue
            elif in_table:
                # End of table
                table_html = MarkdownProcessor._parse_table(table_lines)
                if table_html:
                    html_parts.append(table_html)
                table_lines = []
                in_table = False
                # Fall through to process current line

            # Handle blockquotes
            if line.strip().startswith('>'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                quote_text = line.lstrip('> ').strip()
                html_parts.append(f'<blockquote>{MarkdownProcessor._render_inline(quote_text)}</blockquote>')
                continue

            # Handle headers
            if line.startswith('#'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []

                level = len(line) - len(line.lstrip('#'))
                header_text = line.lstrip('# ').strip()
                if level <= 6:
                    html_parts.append(f'<h{level}>{MarkdownProcessor._render_inline(header_text)}</h{level}>')
                continue

            # Handle lists
            if line.strip().startswith(('- ', '* ')) or re.match(r'^\d+\.\s', line.strip()):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []

                list_item = re.sub(r'^[-*\d.]\s+', '', line.strip())
                html_parts.append(f'<li>{MarkdownProcessor._render_inline(list_item)}</li>')
                continue

            # Handle horizontal rules
            if line.strip() in ('---', '***', '___'):
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                html_parts.append('<hr/>')
                continue

            # Handle empty lines (paragraph break)
            if not line.strip():
                if current_paragraph:
                    paragraph_text = ' '.join(current_paragraph).strip()
                    if paragraph_text:
                        html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')
                    current_paragraph = []
                continue

            # Add to current paragraph
            current_paragraph.append(line.strip())

        # Finish any remaining paragraph
        if current_paragraph:
            paragraph_text = ' '.join(current_paragraph).strip()
            if paragraph_text:
                html_parts.append(f'<p>{MarkdownProcessor._render_inline(paragraph_text)}</p>')

        # Finish any remaining table
        if in_table and table_lines:
            table_html = MarkdownProcessor._parse_table(table_lines)
            if table_html:
                html_parts.append(table_html)

        html = '\n'.join(html_parts) if html_parts else '<p></p>'
        return html

    @staticmethod
    def _render_inline(text: str) -> str:
        """
        Render inline markdown elements (bold, italic, links, code).

        Args:
            text: Text with inline markdown

        Returns:
            HTML string
        """
        # Escape HTML special characters first, but be careful with our markers
        text = (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

        # Bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'__(.+?)__', r'<strong>\1</strong>', text)

        # Italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'_(.+?)_', r'<em>\1</em>', text)

        # Inline code
        text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)

        # Links
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)

        return text

    @staticmethod
    def _parse_table(table_lines: List[str]) -> str:
        """
        Parse markdown table into HTML.

        Args:
            table_lines: List of table lines

        Returns:
            HTML table string
        """
        if not table_lines or len(table_lines) < 2:
            return ""

        # Remove empty lines
        table_lines = [line.strip() for line in table_lines if line.strip()]

        if len(table_lines) < 2:
            return ""

        # Parse header
        header_line = table_lines[0]
        headers = [cell.strip() for cell in header_line.split('|')]
        headers = [h for h in headers if h]  # Remove empty cells

        # Skip separator line (second line with dashes)
        if len(table_lines) < 2:
            return ""

        # Check if second line is separator
        separator = table_lines[1]
        if not re.match(r'^[\s|:-]+$', separator):
            # Not a valid table
            return ""

        # Parse data rows
        rows = []
        for line in table_lines[2:]:
            cells = [cell.strip() for cell in line.split('|')]
            cells = [c for c in cells if c]  # Remove empty cells from leading/trailing pipes
            if cells:
                rows.append(cells)

        # Build HTML table
        html_parts = ['<table>']

        # Header
        html_parts.append('<thead><tr>')
        for header in headers:
            html_parts.append(f'<th>{MarkdownProcessor._render_inline(header)}</th>')
        html_parts.append('</tr></thead>')

        # Body
        if rows:
            html_parts.append('<tbody>')
            for row in rows:
                html_parts.append('<tr>')
                for i, cell in enumerate(row):
                    if i < len(headers):  # Don't exceed header count
                        html_parts.append(f'<td>{MarkdownProcessor._render_inline(cell)}</td>')
                # Fill missing cells
                for i in range(len(row), len(headers)):
                    html_parts.append('<td></td>')
                html_parts.append('</tr>')
            html_parts.append('</tbody>')

        html_parts.append('</table>')

        return '\n'.join(html_parts)

    @staticmethod
    def escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))

    @staticmethod
    def _add_line_numbers_and_highlighting(code: str, language: Optional[str] = None) -> str:
        """
        Add line numbers and syntax highlighting to code block using Pygments.

        Args:
            code: Raw code string
            language: Programming language identifier

        Returns:
            HTML string with line numbers and syntax highlighting
        """
        if PYGMENTS_AVAILABLE and language:
            try:
                # Get the appropriate lexer for the language
                lexer = get_lexer_by_name(language, stripall=False)

                # Use Pygments to tokenize and highlight
                from pygments import lex
                from pygments.token import Token

                lines = code.split('\n')
                html_lines = []

                for line_num, line in enumerate(lines, 1):
                    # Tokenize this line
                    tokens = list(lex(line + '\n', lexer))
                    highlighted_parts = []

                    for token_type, value in tokens:
                        # Skip the newline at the end
                        if value == '\n':
                            continue

                        # Escape HTML in the value
                        value = (value
                                .replace('&', '&amp;')
                                .replace('<', '&lt;')
                                .replace('>', '&gt;'))

                        # Map Pygments token types to our CSS classes
                        css_class = MarkdownProcessor._get_token_css_class(token_type)

                        if css_class:
                            highlighted_parts.append(f'<span class="{css_class}">{value}</span>')
                        else:
                            highlighted_parts.append(value)

                    # Add line number and content
                    html_lines.append(
                        f'<span class="line-number">{line_num:3d}</span>'
                        f'<span class="line-content">{"".join(highlighted_parts)}\n</span>'
                    )

                # Build final HTML
                safe_lang = re.sub(r'[^a-zA-Z0-9_-]', '', language)
                lang_class = f' language-{safe_lang}' if safe_lang else ''
                return f'<pre class="code-block{lang_class}"><code>{"".join(html_lines)}</code></pre>'

            except ClassNotFound:
                # Language not found, fall back to plain text
                pass
            except Exception:
                # Any other error, fall back to plain text
                pass

        # Fallback: no syntax highlighting, just line numbers and escaping
        code = (code
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))

        lines = code.split('\n')
        html_lines = []

        for i, line in enumerate(lines, 1):
            html_lines.append(
                f'<span class="line-number">{i:3d}</span>'
                f'<span class="line-content">{line}\n</span>'
            )

        # Build final HTML
        if language:
            safe_lang = re.sub(r'[^a-zA-Z0-9_-]', '', language)
            lang_class = f' language-{safe_lang}' if safe_lang else ''
        else:
            lang_class = ''

        return f'<pre class="code-block{lang_class}"><code>{"".join(html_lines)}</code></pre>'

    @staticmethod
    def _get_token_css_class(token_type) -> Optional[str]:
        """
        Map Pygments token types to our CSS classes.

        Args:
            token_type: Pygments token type

        Returns:
            CSS class name or None
        """
        from pygments.token import Token

        # Map token types to our simpler CSS classes
        if token_type in Token.Keyword:
            return 'syn-keyword'
        elif token_type in Token.String:
            return 'syn-string'
        elif token_type in Token.Comment:
            return 'syn-comment'
        elif token_type in Token.Number:
            return 'syn-number'
        elif token_type in Token.Name.Function:
            return 'syn-function'
        elif token_type in Token.Name.Class:
            return 'syn-class'
        else:
            return None

