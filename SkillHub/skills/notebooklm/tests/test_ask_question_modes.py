from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import ask_question as aq  # noqa: E402


def test_extract_questions_single() -> None:
    args = SimpleNamespace(question="What is this?", questions=None, questions_file=None)
    questions, error = aq._extract_questions(args)
    assert error is None
    assert questions == ["What is this?"]


def test_extract_questions_mixed(tmp_path: Path) -> None:
    questions_file = tmp_path / "questions.txt"
    questions_file.write_text("first\n#ignore\nsecond\n", encoding="utf-8")

    args = SimpleNamespace(
        question="zero",
        questions="one||two",
        questions_file=str(questions_file),
    )
    questions, error = aq._extract_questions(args)
    assert error is None
    assert questions == ["zero", "one", "two", "first", "second"]


def test_resolve_compare_notebooks_from_library() -> None:
    library = {
        "notebooks": [
            {
                "id": "docs",
                "url": "https://notebooklm.google.com/notebook/11111111-1111-1111-1111-111111111111",
            }
        ]
    }
    args = SimpleNamespace(
        compare_notebook_ids="docs",
        compare_notebook_urls="https://notebooklm.google.com/notebook/22222222-2222-2222-2222-222222222222",
    )

    result = aq._resolve_compare_notebooks(args, library)
    assert "error" not in result
    targets = result["targets"]
    assert len(targets) == 2
    assert targets[0]["notebook_id"] == "docs"


def test_build_markdown_export_single() -> None:
    result = {
        "mode": "single",
        "notebook_url": "https://notebooklm.google.com/notebook/abc",
        "question": "Q?",
        "answer": "A",
        "citations": ["source 1"],
    }
    output = aq._build_markdown_export(result)
    assert "NotebookLM Export" in output
    assert "## Answer" in output
    assert "source 1" in output
