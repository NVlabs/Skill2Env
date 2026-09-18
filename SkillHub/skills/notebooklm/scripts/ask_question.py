#!/usr/bin/env python3
"""
Ask questions to NotebookLM notebooks via browser automation.
Supports single ask, batch ask, and multi-notebook comparison queries.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import Page, sync_playwright

from common import (
    get_active_notebook,
    get_artifacts_dir,
    get_notes_dir,
    get_notebook_by_id,
    get_notebook_by_url,
    is_valid_notebook_url,
    launch_persistent_context,
    load_library,
    now_iso,
    parse_csv_values,
    record_notebook_use,
    sanitize_profile_name,
)

FOLLOW_UP_REMINDER = (
    "\n\nEXTREMELY IMPORTANT: Is that ALL you need to know? You can always ask another question. "
    "Before replying to the user, check if anything is still unclear, and ask follow-up questions if needed."
)

CHAT_INPUT_SELECTORS = [
    "textarea.query-box-input",
    "textarea[aria-label*='Ask']",
    "textarea[aria-label*='Anfrage']",
]

RATE_LIMIT_KEYWORDS = [
    "rate limit",
    "limit exceeded",
    "quota exhausted",
    "daily limit",
    "too many requests",
]

PLACEHOLDER_PHRASES = [
    "analyzing your files",
    "analyzing your sources",
    "thinking",
    "loading",
    "just a moment",
    "working on it",
]

CITATION_SELECTORS = [
    ".citation-chip",
    ".source-chip",
    ".grounding-chip",
    ".source-link",
    "a[href*='source']",
    "a[href*='notebooklm']",
]

RETRYABLE_ERROR_KEYWORDS = [
    "timeout",
    "timed out",
    "connection",
    "target closed",
    "context closed",
    "execution context was destroyed",
    "protocol error",
    "page crashed",
    "browser has been closed",
]


def _safe_name(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-") or "item"


def _artifact_dir(args) -> Path:
    raw = args.artifacts_dir
    if raw:
        return Path(raw).expanduser().resolve()
    return get_artifacts_dir()


def _capture_debug_artifacts(page: Page, args, mode: str, attempt: int, error_message: str) -> Optional[Dict]:
    try:
        directory = _artifact_dir(args)
        directory.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        prefix = f"{stamp}-{_safe_name(mode)}-attempt{attempt}"

        screenshot_path = directory / f"{prefix}.png"
        html_path = directory / f"{prefix}.html"

        page.screenshot(path=str(screenshot_path), full_page=True)
        html_path.write_text(page.content(), encoding="utf-8")

        return {
            "attempt": attempt,
            "error": error_message,
            "url": page.url,
            "screenshot": str(screenshot_path),
            "html": str(html_path),
        }
    except Exception:  # noqa: BLE001
        return None


def _is_retryable_error(message: str) -> bool:
    lower = message.lower().strip()
    if any(keyword in lower for keyword in RATE_LIMIT_KEYWORDS):
        return False
    return any(keyword in lower for keyword in RETRYABLE_ERROR_KEYWORDS)


def _is_transient_placeholder(text: str) -> bool:
    lower = text.strip().lower()
    if not lower:
        return True
    return any(phrase in lower for phrase in PLACEHOLDER_PHRASES)


def _is_still_thinking(page: Page) -> bool:
    try:
        thinking = page.query_selector("div.thinking-message")
        if not thinking:
            return False
        return thinking.is_visible()
    except PlaywrightError:
        return False


def _find_chat_input(page: Page, timeout_ms: int = 30000) -> Optional[str]:
    for selector in CHAT_INPUT_SELECTORS:
        try:
            page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
            return selector
        except PlaywrightError:
            continue
    return None


def _collect_response_texts(page: Page) -> List[str]:
    texts: List[str] = []
    try:
        containers = page.query_selector_all(".to-user-container")
        for container in containers:
            text_el = container.query_selector(".message-text-content")
            if not text_el:
                continue
            text = text_el.inner_text().strip()
            if text:
                texts.append(text)
    except PlaywrightError:
        pass

    if texts:
        return texts

    fallback_selectors = [
        "[data-message-author='bot']",
        "[data-message-author='assistant']",
        "[data-testid*='response']",
    ]
    for selector in fallback_selectors:
        try:
            for element in page.query_selector_all(selector):
                text = element.inner_text().strip()
                if text:
                    texts.append(text)
        except PlaywrightError:
            continue
        if texts:
            break

    return texts


def _collect_citations(page: Page) -> List[str]:
    seen: set[str] = set()
    citations: List[str] = []
    for selector in CITATION_SELECTORS:
        try:
            elements = page.query_selector_all(selector)
        except PlaywrightError:
            continue
        for element in elements:
            try:
                text = element.inner_text().strip()
            except PlaywrightError:
                continue
            if not text:
                continue
            if text in seen:
                continue
            seen.add(text)
            citations.append(text)
    return citations


def _detect_rate_limit(page: Page) -> bool:
    try:
        body = page.inner_text("body").lower()
        return any(keyword in body for keyword in RATE_LIMIT_KEYWORDS)
    except PlaywrightError:
        return False


def _wait_for_new_answer(
    page: Page,
    question: str,
    existing_texts: List[str],
    timeout_sec: int,
) -> Optional[str]:
    seen = {text.strip() for text in existing_texts if text.strip()}
    normalized_question = question.strip().lower()
    deadline = time.time() + timeout_sec

    stable_value = None
    stable_count = 0
    required_stable_polls = 3

    while time.time() < deadline:
        if _is_still_thinking(page):
            page.wait_for_timeout(1000)
            continue

        if _detect_rate_limit(page):
            raise RuntimeError("NotebookLM rate limit reached. Try again later or re-authenticate.")

        candidate = None
        for text in _collect_response_texts(page):
            clean = text.strip()
            if not clean:
                continue
            if clean in seen:
                continue
            if clean.lower() == normalized_question:
                continue
            if _is_transient_placeholder(clean):
                continue
            candidate = clean
            break

        if candidate:
            if candidate == stable_value:
                stable_count += 1
            else:
                stable_value = candidate
                stable_count = 1

            if stable_count >= required_stable_polls:
                return candidate

        page.wait_for_timeout(1000)

    return None


def _resolve_notebook(args, library: Dict) -> Dict:
    notebook_id = None
    notebook_url = args.notebook_url

    if notebook_url:
        if not is_valid_notebook_url(notebook_url):
            return {"error": "Invalid --notebook-url format"}
        notebook = get_notebook_by_url(library, notebook_url)
        if notebook:
            notebook_id = notebook.get("id")
    elif args.notebook_id:
        notebook = get_notebook_by_id(library, args.notebook_id)
        if not notebook:
            return {"error": f"Notebook not found in library: {args.notebook_id}"}
        notebook_id = notebook.get("id")
        notebook_url = notebook.get("url")
    else:
        active = get_active_notebook(library)
        if not active:
            return {
                "error": (
                    "No notebook specified and no active notebook configured. "
                    "Use --notebook-url, --notebook-id, or activate a notebook first."
                )
            }
        notebook_id = active.get("id")
        notebook_url = active.get("url")

    if not notebook_url:
        return {"error": "Failed to resolve notebook URL"}

    return {
        "notebook_id": notebook_id,
        "notebook_url": notebook_url,
    }


def _resolve_compare_notebooks(args, library: Dict) -> Dict:
    ids = parse_csv_values(args.compare_notebook_ids)
    urls = parse_csv_values(args.compare_notebook_urls)
    if not ids and not urls:
        return {"targets": []}

    targets: List[Dict] = []
    seen_urls: set[str] = set()

    for notebook_id in ids:
        notebook = get_notebook_by_id(library, notebook_id)
        if not notebook:
            return {"error": f"Notebook not found in library: {notebook_id}"}
        notebook_url = str(notebook.get("url", "")).strip()
        if notebook_url in seen_urls:
            continue
        seen_urls.add(notebook_url)
        targets.append({"notebook_id": notebook_id, "notebook_url": notebook_url})

    for notebook_url in urls:
        if not is_valid_notebook_url(notebook_url):
            return {"error": f"Invalid notebook URL in --compare-notebook-urls: {notebook_url}"}
        notebook = get_notebook_by_url(library, notebook_url)
        notebook_id = notebook.get("id") if notebook else None
        if notebook_url in seen_urls:
            continue
        seen_urls.add(notebook_url)
        targets.append({"notebook_id": notebook_id, "notebook_url": notebook_url})

    return {"targets": targets}


def _extract_questions(args) -> Tuple[List[str], Optional[str]]:
    questions: List[str] = []

    if args.question:
        questions.append(args.question.strip())

    if args.questions:
        if "||" in args.questions:
            questions.extend([part.strip() for part in args.questions.split("||") if part.strip()])
        else:
            questions.extend(parse_csv_values(args.questions))

    if args.questions_file:
        path = Path(args.questions_file).expanduser().resolve()
        if not path.exists():
            return [], f"Questions file not found: {path}"
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            questions.append(stripped)

    cleaned = [q for q in (q.strip() for q in questions) if q]
    if not cleaned:
        return [], "Provide at least one question via --question, --questions, or --questions-file"

    return cleaned, None


def _ask_once_on_page(
    page: Page,
    notebook_url: str,
    question: str,
    timeout: int,
    input_timeout: int,
) -> Dict:
    page.goto(notebook_url, wait_until="domcontentloaded", timeout=90000)
    page.wait_for_timeout(2000)

    if "accounts.google.com" in page.url:
        return {
            "error": (
                "NotebookLM redirected to Google login. "
                "Run: python scripts/auth_manager.py setup"
            )
        }

    input_selector = _find_chat_input(page, timeout_ms=input_timeout * 1000)
    if not input_selector:
        return {
            "error": (
                "Could not find NotebookLM chat input. "
                "Notebook may still be loading or login may be required."
            )
        }

    existing_texts = _collect_response_texts(page)
    before_citations = set(_collect_citations(page))

    page.click(input_selector)
    page.fill(input_selector, question)
    page.press(input_selector, "Enter")

    answer = _wait_for_new_answer(
        page=page,
        question=question,
        existing_texts=existing_texts,
        timeout_sec=timeout,
    )
    if not answer:
        return {"error": f"Timed out waiting for answer after {timeout}s"}

    after_citations = _collect_citations(page)
    new_citations = [citation for citation in after_citations if citation not in before_citations]

    return {
        "status": "success",
        "question": question,
        "answer": f"{answer.rstrip()}{FOLLOW_UP_REMINDER}",
        "citations": new_citations,
        "timestamp_utc": now_iso(),
    }


def _ask_with_retries(
    args,
    notebook_url: str,
    question: str,
    mode: str,
) -> Dict:
    attempts = max(1, int(args.retries or 1))
    profile = sanitize_profile_name(args.profile)

    errors: List[str] = []
    artifacts: List[Dict] = []

    for attempt in range(1, attempts + 1):
        with sync_playwright() as p:
            context = launch_persistent_context(
                p,
                headless=not args.show_browser,
                profile=profile,
            )
            page = context.new_page()
            try:
                result = _ask_once_on_page(
                    page=page,
                    notebook_url=notebook_url,
                    question=question,
                    timeout=args.timeout,
                    input_timeout=args.input_timeout,
                )

                if result.get("error"):
                    error_message = str(result["error"])
                    if attempt < attempts and _is_retryable_error(error_message):
                        errors.append(error_message)
                        artifact = _capture_debug_artifacts(page, args, mode, attempt, error_message)
                        if artifact:
                            artifacts.append(artifact)
                        time.sleep(min(attempt * 1.5, 5.0))
                        continue

                    if errors:
                        result.setdefault("previous_errors", errors)
                    if artifacts:
                        result.setdefault("artifacts", artifacts)
                    if attempt > 1:
                        result.setdefault("attempts", attempt)
                    return result

                if errors:
                    result["previous_errors"] = errors
                if artifacts:
                    result["artifacts"] = artifacts
                if attempt > 1:
                    result["attempts"] = attempt
                return result
            except Exception as exc:  # noqa: BLE001
                error_message = str(exc)
                errors.append(error_message)
                artifact = _capture_debug_artifacts(page, args, mode, attempt, error_message)
                if artifact:
                    artifacts.append(artifact)
                if attempt >= attempts:
                    result: Dict = {
                        "error": f"ask failed after {attempts} attempts: {error_message}",
                        "errors": errors,
                        "attempts": attempts,
                    }
                    if artifacts:
                        result["artifacts"] = artifacts
                    return result
                time.sleep(min(attempt * 1.5, 5.0))
            finally:
                context.close()

    return {"error": "ask failed unexpectedly"}


def _build_markdown_export(result: Dict) -> str:
    mode = result.get("mode", "single")
    lines = [
        f"# NotebookLM Export ({mode})",
        "",
        f"Generated: {now_iso()}",
        "",
    ]

    if mode == "single":
        lines.extend(
            [
                f"Notebook: {result.get('notebook_url')}",
                f"Question: {result.get('question')}",
                "",
                "## Answer",
                "",
                result.get("answer", ""),
                "",
            ]
        )
        citations = result.get("citations") or []
        lines.append("## Citations")
        if citations:
            lines.extend([f"- {citation}" for citation in citations])
        else:
            lines.append("- (none detected)")
        lines.append("")
        return "\n".join(lines)

    if mode == "batch":
        lines.append(f"Notebook: {result.get('notebook_url')}")
        lines.append("")
        for idx, item in enumerate(result.get("results", []), start=1):
            lines.append(f"## Q{idx}: {item.get('question')}")
            lines.append("")
            if item.get("error"):
                lines.append(f"Error: {item['error']}")
                lines.append("")
                continue
            lines.append(item.get("answer", ""))
            lines.append("")
            citations = item.get("citations") or []
            lines.append("Citations:")
            if citations:
                lines.extend([f"- {citation}" for citation in citations])
            else:
                lines.append("- (none detected)")
            lines.append("")
        return "\n".join(lines)

    lines.append(f"Question: {result.get('question')}")
    lines.append("")
    for item in result.get("responses", []):
        lines.append(f"## Notebook: {item.get('notebook_url')}")
        lines.append("")
        if item.get("error"):
            lines.append(f"Error: {item['error']}")
            lines.append("")
            continue
        lines.append(item.get("answer", ""))
        lines.append("")
        citations = item.get("citations") or []
        lines.append("Citations:")
        if citations:
            lines.extend([f"- {citation}" for citation in citations])
        else:
            lines.append("- (none detected)")
        lines.append("")

    return "\n".join(lines)


def _write_export_if_requested(result: Dict, args, mode: str) -> Optional[str]:
    should_write = bool(args.export_file or args.save_notes)
    if not should_write:
        return None

    export_format = args.export_format.lower()
    if export_format not in {"json", "markdown"}:
        raise ValueError("--export-format must be json or markdown")

    if args.export_file:
        out_path = Path(args.export_file).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        extension = "json" if export_format == "json" else "md"
        stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        out_path = get_notes_dir() / f"notebooklm-{mode}-{stamp}.{extension}"

    if export_format == "json":
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    else:
        out_path.write_text(_build_markdown_export(result), encoding="utf-8")

    return str(out_path)


def _run_single_mode(args, library: Dict, questions: List[str]) -> Dict:
    if len(questions) != 1:
        return {"error": "Single mode requires exactly one question"}

    resolved = _resolve_notebook(args, library)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    question = questions[0]
    ask_result = _ask_with_retries(
        args,
        notebook_url=resolved["notebook_url"],
        question=question,
        mode="single",
    )
    if ask_result.get("error"):
        return {
            "mode": "single",
            "notebook_url": resolved["notebook_url"],
            "notebook_id": resolved.get("notebook_id"),
            **ask_result,
        }

    if resolved.get("notebook_id"):
        record_notebook_use(library, resolved["notebook_id"])

    return {
        "status": "success",
        "mode": "single",
        "question": question,
        "answer": ask_result["answer"],
        "citations": ask_result.get("citations", []),
        "timestamp_utc": ask_result.get("timestamp_utc", now_iso()),
        "notebook_url": resolved["notebook_url"],
        "notebook_id": resolved.get("notebook_id"),
        "profile": sanitize_profile_name(args.profile),
        **({"attempts": ask_result["attempts"]} if ask_result.get("attempts") else {}),
        **({"artifacts": ask_result["artifacts"]} if ask_result.get("artifacts") else {}),
        **({"previous_errors": ask_result["previous_errors"]} if ask_result.get("previous_errors") else {}),
    }


def _run_batch_mode(args, library: Dict, questions: List[str]) -> Dict:
    resolved = _resolve_notebook(args, library)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    results: List[Dict] = []
    for question in questions:
        ask_result = _ask_with_retries(
            args,
            notebook_url=resolved["notebook_url"],
            question=question,
            mode="batch",
        )
        if ask_result.get("error"):
            item = {
                "question": question,
                "error": ask_result["error"],
                "timestamp_utc": now_iso(),
            }
            if ask_result.get("artifacts"):
                item["artifacts"] = ask_result["artifacts"]
            results.append(item)
            if args.fail_fast:
                break
            continue

        if resolved.get("notebook_id"):
            record_notebook_use(library, resolved["notebook_id"])

        item = {
            "question": question,
            "answer": ask_result["answer"],
            "citations": ask_result.get("citations", []),
            "timestamp_utc": ask_result.get("timestamp_utc", now_iso()),
        }
        if ask_result.get("attempts"):
            item["attempts"] = ask_result["attempts"]
        if ask_result.get("previous_errors"):
            item["previous_errors"] = ask_result["previous_errors"]
        if ask_result.get("artifacts"):
            item["artifacts"] = ask_result["artifacts"]
        results.append(item)

    success_count = len([item for item in results if not item.get("error")])
    error_count = len(results) - success_count

    return {
        "status": "success" if error_count == 0 else "partial_success",
        "mode": "batch",
        "notebook_url": resolved["notebook_url"],
        "notebook_id": resolved.get("notebook_id"),
        "count": len(results),
        "success_count": success_count,
        "error_count": error_count,
        "results": results,
        "profile": sanitize_profile_name(args.profile),
    }


def _run_multi_mode(args, library: Dict, questions: List[str]) -> Dict:
    if len(questions) != 1:
        return {"error": "Multi-notebook mode supports exactly one question"}

    resolved = _resolve_compare_notebooks(args, library)
    if resolved.get("error"):
        return {"error": resolved["error"]}

    targets = resolved.get("targets", [])
    if not targets:
        return {
            "error": (
                "No comparison notebooks resolved. "
                "Use --compare-notebook-ids and/or --compare-notebook-urls"
            )
        }

    question = questions[0]
    responses: List[Dict] = []

    for target in targets:
        ask_result = _ask_with_retries(
            args,
            notebook_url=target["notebook_url"],
            question=question,
            mode="multi",
        )

        if ask_result.get("error"):
            item = {
                "notebook_url": target["notebook_url"],
                "notebook_id": target.get("notebook_id"),
                "error": ask_result["error"],
                "timestamp_utc": now_iso(),
            }
            if ask_result.get("artifacts"):
                item["artifacts"] = ask_result["artifacts"]
            responses.append(item)
            if args.fail_fast:
                break
            continue

        if target.get("notebook_id"):
            record_notebook_use(library, target["notebook_id"])

        item = {
            "notebook_url": target["notebook_url"],
            "notebook_id": target.get("notebook_id"),
            "answer": ask_result["answer"],
            "citations": ask_result.get("citations", []),
            "timestamp_utc": ask_result.get("timestamp_utc", now_iso()),
        }
        if ask_result.get("attempts"):
            item["attempts"] = ask_result["attempts"]
        if ask_result.get("previous_errors"):
            item["previous_errors"] = ask_result["previous_errors"]
        if ask_result.get("artifacts"):
            item["artifacts"] = ask_result["artifacts"]
        responses.append(item)

    success_count = len([item for item in responses if not item.get("error")])
    error_count = len(responses) - success_count

    return {
        "status": "success" if error_count == 0 else "partial_success",
        "mode": "multi",
        "question": question,
        "count": len(responses),
        "success_count": success_count,
        "error_count": error_count,
        "responses": responses,
        "profile": sanitize_profile_name(args.profile),
    }


def _run(args) -> Dict:
    library = load_library()
    questions, question_error = _extract_questions(args)
    if question_error:
        return {"error": question_error}

    compare_targets = _resolve_compare_notebooks(args, library)
    if compare_targets.get("error"):
        return {"error": compare_targets["error"]}

    multi_mode = len(compare_targets.get("targets", [])) > 0
    if multi_mode:
        result = _run_multi_mode(args, library, questions)
    elif len(questions) > 1:
        result = _run_batch_mode(args, library, questions)
    else:
        result = _run_single_mode(args, library, questions)

    if result.get("error"):
        return result

    mode = result.get("mode", "single")
    export_file = _write_export_if_requested(result, args, mode)
    if export_file:
        result["export_file"] = export_file
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Ask question(s) to NotebookLM")
    parser.add_argument("--question", help="Single question to ask")
    parser.add_argument(
        "--questions",
        help="Multiple questions (comma-separated or '||'-separated)",
    )
    parser.add_argument(
        "--questions-file",
        help="Path to file with one question per line",
    )

    parser.add_argument("--notebook-id", help="Notebook ID from local library")
    parser.add_argument("--notebook-url", help="NotebookLM URL")

    parser.add_argument(
        "--compare-notebook-ids",
        help="Comma-separated notebook IDs for multi-notebook comparison mode",
    )
    parser.add_argument(
        "--compare-notebook-urls",
        help="Comma-separated notebook URLs for multi-notebook comparison mode",
    )

    parser.add_argument("--show-browser", action="store_true", help="Show browser window while asking")
    parser.add_argument("--profile", default="default", help="Auth/browser profile name (default: default)")
    parser.add_argument("--timeout", type=int, default=120, help="Answer wait timeout in seconds (default: 120)")
    parser.add_argument(
        "--input-timeout",
        type=int,
        default=30,
        help="Timeout to wait for chat input visibility in seconds (default: 30)",
    )
    parser.add_argument("--retries", type=int, default=2, help="Retry attempts for transient browser failures")
    parser.add_argument(
        "--artifacts-dir",
        help="Directory for failure screenshots/HTML dumps (default: NOTEBOOKLM data dir artifacts)",
    )
    parser.add_argument("--fail-fast", action="store_true", help="Stop batch/multi mode on first error")

    parser.add_argument(
        "--export-format",
        default="json",
        help="Export format when saving results: json or markdown (default: json)",
    )
    parser.add_argument("--export-file", help="Write full result to this file path")
    parser.add_argument(
        "--save-notes",
        action="store_true",
        help="Save export under the skill notes directory when no --export-file is provided",
    )

    args = parser.parse_args()

    try:
        result = _run(args)
    except Exception as exc:  # noqa: BLE001
        result = {"error": str(exc)}

    print(json.dumps(result, indent=2))
    if isinstance(result, dict) and result.get("error"):
        sys.exit(1)


if __name__ == "__main__":
    main()
