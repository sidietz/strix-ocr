#!/usr/bin/env python3
import ast
import json
import re
from pathlib import Path
from typing import Any, List, Optional


def natural_sort_key(path: Path) -> List[Any]:
    """
    Splits the filename into text and integer chunks so that numbers
    are sorted numerically instead of lexicographically.

    Example:
        'fixed_random_string_10.md' -> ['fixed_random_string_', 10, '.md']
        'fixed_random_string_2.md'  -> ['fixed_random_string_', 2, '.md']
    Because 2 < 10, '..._2.md' correctly comes before '..._10.md'.
    """
    return [
        int(chunk) if chunk.isdigit() else chunk.lower()
        for chunk in re.split(r"(\d+)", path.name)
    ]


def parse_array_content(raw_text: str) -> Optional[List[str]]:
    """Parse an array from raw text, handling JSON, Python literals, or malformed variants."""
    text = raw_text.strip()
    if not text:
        return None

    # 1. Try standard JSON parser
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return [str(item) for item in data]
    except Exception:
        pass

    # 2. Try ast.literal_eval (handles single quotes like ['test', 'string'])
    try:
        data = ast.literal_eval(text)
        if isinstance(data, (list, tuple)):
            return [str(item) for item in data]
    except Exception:
        pass

    # 3. Fallback: extract the bracketed portion if there's markdown/metadata around it
    bracket_match = re.search(r"\[(.*?)\]", text, re.DOTALL)
    if bracket_match:
        try:
            data = ast.literal_eval(bracket_match.group(0))
            if isinstance(data, (list, tuple)):
                return [str(item) for item in data]
        except Exception:
            pass

    return None


def join_tokens_readably(tokens: List[str]) -> str:
    """
    Join tokens into readable text, avoiding awkward spaces before common punctuation.
    """
    text = " ".join(tokens)
    # Remove space before common punctuation: "word , next" -> "word, next"
    text = re.sub(r"\s+([,.:;!?])", r"\1", text)
    return text.strip()


def combine_malformed_md_files(
    input_dir: str | Path,
    output_file: str | Path,
    include_headers: bool = False,
):
    """
    Combines all .md files from input_dir in numerical order into a single readable markdown file.

    :param input_dir: Directory containing the malformed .md files.
    :param output_file: Destination path for the merged .md file.
    :param include_headers: Whether to add a markdown heading for each source file.
    """
    input_path = Path(input_dir)
    output_path = Path(output_file)

    if not input_path.is_dir():
        raise ValueError(f"Input directory does not exist: {input_path}")

    # Exclude output file if it happens to be located in the same directory
    md_files = [f for f in input_path.glob("*.md") if f.resolve() != output_path.resolve()]

    if not md_files:
        print(f"No .md files found in {input_path}")
        return

    # Sort files numerically using the natural sort key
    md_files.sort(key=natural_sort_key)

    combined_sections = []

    for file_path in md_files:
        content = file_path.read_text(encoding="utf-8")
        tokens = parse_array_content(content)

        if tokens is not None:
            readable_text = join_tokens_readably(tokens)
        else:
            print(f"Warning: Could not parse array in {file_path.name}; keeping raw content.")
            readable_text = content.strip()

        if include_headers:
            section = f"## {file_path.stem}\n\n{readable_text}"
        else:
            section = readable_text

        combined_sections.append(section)

    # Ensure output parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Join sections with double newlines
    output_path.write_text("\n\n".join(combined_sections) + "\n", encoding="utf-8")
    print(f"Successfully processed {len(combined_sections)} files in numerical order.")
    print(f"Saved to: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Merge malformed .md files in numerical order into readable text."
    )
    parser.add_argument(
        "input_dir",
        help="Path to folder with malformed .md files",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="combined.md",
        help="Path to output .md file (default: combined.md)",
    )
    parser.add_argument(
        "--headers",
        action="store_true",
        help="Add a markdown header (## filename) before each file's content",
    )

    args = parser.parse_args()
    combine_malformed_md_files(
        input_dir=args.input_dir,
        output_file=args.output,
        include_headers=args.headers,
    )
