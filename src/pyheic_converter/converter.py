"""Core conversion logic for HEIC to JPEG."""

from __future__ import annotations

from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener


register_heif_opener()


def convert_heic_to_jpeg(
    input_path: str | Path,
    output_path: str | Path | None = None,
    *,
    quality: int = 95,
) -> Path:
    """
    Convert a HEIC file into a JPEG file.

    Parameters
    ----------
    input_path:
        Path to the input HEIC file.
    output_path:
        Optional output path. If omitted, uses input filename with `.jpg` suffix.
    quality:
        JPEG quality (1-95).
    """
    src = Path(input_path)
    if not src.exists():
        raise FileNotFoundError(f"Input file does not exist: {src}")
    if src.suffix.lower() not in {".heic", ".heif"}:
        raise ValueError(f"Expected a HEIC/HEIF file, got: {src.suffix}")
    if not (1 <= quality <= 95):
        raise ValueError("quality must be between 1 and 95")

    dst = Path(output_path) if output_path else src.with_suffix(".jpg")
    dst.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as image:
        # JPEG doesn't support alpha channel.
        if image.mode in ("RGBA", "LA", "P"):
            image = image.convert("RGB")
        image.save(dst, format="JPEG", quality=quality, optimize=True)

    return dst

