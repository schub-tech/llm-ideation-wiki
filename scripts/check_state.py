#!/usr/bin/env python3
"""Check that local agent state files stay small and readable by a cold reader.

Fails when hot.md exceeds its size or line caps, or when hot.md, wiki/index.md,
or the recent tail of wiki/log.md contain glued, space-stripped tokens such as
"Active1191;nooutreach", "total18/150", or "nooutreach". Wrap a real identifier
that trips the check (a product name like `Office365`) in backticks.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

HOT_MAX_BYTES = 5 * 1024
HOT_MAX_LINE_CHARS = 300
LOG_TAIL_LINES = 30

# Prose known to be written with normal spacing; its words are never flagged.
REFERENCE_PROSE = ["AGENTS.md", "README.md", "docs/**/*.md", "templates/*.md", ".agents/skills/*/SKILL.md"]

# Tokens that legitimately mix letters, digits, or punctuation.
ALLOWED_TOKENS = {"sha256", "base64", "utf16", "utf32", "tl;dr"}

# A number followed by a unit is a measurement, not glue ("100ms", "2rem").
UNIT = re.compile(r"\d+(?:\.\d+)?(?:ms|kb|mb|gb|tb|rem|deg|dvh|svh|lvh|fps|kwh)", re.IGNORECASE)

# Closed compounds whose spaced form is also normal English ("every one", "break down").
CLOSED_COMPOUNDS = {
    "afterwards", "anything", "anywhere", "breakdown", "breakeven", "breakthrough", "businessplan",
    "changelog", "checklist", "checkout", "cybersecurity", "datapoint", "entrypoint", "everybody", "everyday",
    "everyone", "everything", "everywhere", "followup", "giveaway", "handover", "headcount",
    "however", "indirect", "infrastructure", "meanwhile", "nevertheless", "nonetheless",
    "notebook", "onboarding", "otherwise", "outbound", "overview", "pushback", "readback", "realtime",
    "screenshot", "somebody", "someone", "something", "sometimes", "somewhere", "standalone",
    "takeaway", "therefore", "together", "turnover", "walkthrough", "whatever", "whenever",
    "wherever", "wikilink", "workaround", "workflow", "workshop", "worldwide", "yourself",
    "themselves", "ourselves",
}

# Product and person names in PascalCase ("FastTrack", "DeepSearch") keep their spelling.
PASCAL_CASE = re.compile(r"[A-Z][a-z]+(?:[A-Z][a-z]+)+")

# Two-letter words allowed as pieces of a glued token ("no" in "nooutreach").
SHORT_WORDS = {"ai", "an", "as", "at", "by", "in", "is", "it", "no", "of", "on", "or", "to", "up", "vs"}

GLUE_PATTERNS = [
    # Letters, digits, letters: "archive572preserved", "Chrome100%visual".
    re.compile(r"[A-Za-z]{2,}\d+%?[A-Za-z]{2,}"),
    # Word fused to a count: "total18", "Contacts1189".
    re.compile(r"[a-z]{3,}\d{2,}"),
    # Count fused to a word: "61fresh", "4Contact".
    re.compile(r"\d+[A-Za-z]{3,}"),
]

# Comma or semicolon with no space after a word: "Active1191;nooutreach".
PUNCTUATION_GLUE = re.compile(r"[A-Za-z)][;,][\w(]|\d[;,][A-Za-z(]")

CODE_SPAN = re.compile(r"`[^`]*`")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
BARE_URL = re.compile(r"https?://\S+")
HEX_ID = re.compile(r"[0-9a-f]{16,}")
EDGE_PUNCTUATION = "*_()[]{}\"'.,;:!?"
MIN_GLUED_WORD = 8


def clean(line: str) -> str:
    return BARE_URL.sub(" ", LINK_TARGET.sub("]", CODE_SPAN.sub(" ", line)))


class Corpus:
    """Spaced words and word pairs: evidence that a glued token was once two words."""

    def __init__(self, texts: list[str], reference: list[str]) -> None:
        self.words: set[str] = set()
        self.pairs: set[tuple[str, str]] = set()
        self.reference: set[str] = set()
        for text in texts + reference:
            for line in text.splitlines():
                self._add_line(line)
        for text in reference:
            self.reference.update(word.lower() for word in re.findall(r"[^\W\d_]+", text))

    def _add_line(self, line: str) -> None:
        previous = None
        for raw in clean(line).split():
            word = raw.strip(EDGE_PUNCTUATION).lower()
            if not word.isalpha():
                previous = None
                continue
            self.words.add(word)
            if previous:
                self.pairs.add((previous, word))
            previous = None if raw.rstrip("*_)]\"'")[-1:] in ".;:!?" else word

    def _piece(self, piece: str) -> bool:
        return piece in SHORT_WORDS if len(piece) < 3 else piece in self.words

    def glued(self, token: str) -> bool:
        """True when the token splits fully into known words, every adjacent pair seen spaced elsewhere."""
        word = token.lower()
        if len(word) < MIN_GLUED_WORD or PASCAL_CASE.fullmatch(token) or word in self.reference:
            return False
        if word in CLOSED_COMPOUNDS or word.removesuffix("s") in CLOSED_COMPOUNDS:
            return False
        # reach[i] holds the last words of valid splits of word[:i].
        reach: list[set[str]] = [set() for _ in range(len(word) + 1)]
        for end in range(2, len(word)):
            if self._piece(word[:end]):
                reach[end].add(word[:end])
        for start in range(2, len(word)):
            for last in reach[start]:
                for end in range(start + 2, len(word) + 1):
                    piece = word[start:end]
                    if self._piece(piece) and (last, piece) in self.pairs:
                        if end == len(word):
                            return True
                        reach[end].add(piece)
        return False


def glued_tokens(line: str, corpus: Corpus | None = None) -> list[str]:
    found = []
    for raw in clean(line).split():
        token = raw.strip(EDGE_PUNCTUATION)
        if not token or token.startswith("#") or any(char in token for char in "=<>") or token.lower() in ALLOWED_TOKENS:
            continue
        if PUNCTUATION_GLUE.search(token):
            found.append(token)
            continue
        # Slugs, filenames, versions, and IDs keep their own spelling.
        if re.search(r"\w[-_.]\w", token) or HEX_ID.fullmatch(token):
            continue
        # Check each side of a slash: "review27/import", "61fresh/63reconsidered".
        for part in (part.strip(EDGE_PUNCTUATION) for part in token.split("/")):
            if not part or part.lower() in ALLOWED_TOKENS or HEX_ID.fullmatch(part) or UNIT.fullmatch(part):
                continue
            if any(pattern.search(part) for pattern in GLUE_PATTERNS) or (
                corpus and part.isalpha() and corpus.glued(part)
            ):
                found.append(token)
                break
    return found


def check_file(label: str, lines: list[tuple[int, str]], corpus: Corpus, failures: list[str]) -> None:
    for number, line in lines:
        tokens = glued_tokens(line, corpus)
        if tokens:
            shown = ", ".join(tokens[:5])
            failures.append(f"{label}:{number}: glued words ({shown}); write full words with normal spacing")


def numbered(path: Path) -> list[tuple[int, str]]:
    return list(enumerate(path.read_text(encoding="utf-8").splitlines(), start=1))


def reference_prose(root: Path) -> list[str]:
    paths = {path for pattern in REFERENCE_PROSE for path in root.glob(pattern) if path.is_file()}
    return [path.read_text(encoding="utf-8") for path in sorted(paths)]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Repo root to check (default: this repo).")
    args = parser.parse_args()

    root = args.root.resolve()
    hot = root / "hot.md"
    log = root / "wiki" / "log.md"
    index = root / "wiki" / "index.md"
    failures: list[str] = []

    state = [path.read_text(encoding="utf-8") for path in (hot, log, index) if path.exists()]
    corpus = Corpus(state, reference_prose(root))

    if hot.exists():
        size = hot.stat().st_size
        if size > HOT_MAX_BYTES:
            failures.append(
                f"hot.md is {size} bytes (cap {HOT_MAX_BYTES}); rewrite it as current state and move history to wiki/log.md"
            )
        hot_lines = numbered(hot)
        for number, line in hot_lines:
            if len(line) > HOT_MAX_LINE_CHARS:
                failures.append(f"hot.md:{number}: line is {len(line)} chars (cap {HOT_MAX_LINE_CHARS}); split it or link the detail")
        check_file("hot.md", hot_lines, corpus, failures)

    if index.exists():
        check_file("wiki/index.md", numbered(index), corpus, failures)

    if log.exists():
        check_file("wiki/log.md", numbered(log)[-LOG_TAIL_LINES:], corpus, failures)

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("state files are within caps and readable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
