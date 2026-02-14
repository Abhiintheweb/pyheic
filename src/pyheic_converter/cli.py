"""CLI for converting HEIC images to JPEG."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .converter import convert_heic_to_jpeg


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heic2jpeg",
        description="Convert HEIC/HEIF images to JPEG.",
    )
    parser.add_argument("input", type=Path, help="Path to input .heic/.heif file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Path to output .jpg file (default: same name as input).",
    )
    parser.add_argument(
        "-q",
        "--quality",
        type=int,
        default=95,
        help="JPEG quality 1-95 (default: 95)",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        out = convert_heic_to_jpeg(args.input, args.output, quality=args.quality)
    except Exception as exc:  # pragma: no cover - CLI error surface
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Created: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

