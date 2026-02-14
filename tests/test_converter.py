from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys
import types
from unittest.mock import MagicMock, patch

# Allow tests to run without optional runtime deps installed.
if "PIL" not in sys.modules:
    pil_module = types.ModuleType("PIL")
    pil_module.Image = types.SimpleNamespace(open=lambda *_args, **_kwargs: None)
    sys.modules["PIL"] = pil_module

if "pillow_heif" not in sys.modules:
    pillow_heif_module = types.ModuleType("pillow_heif")
    pillow_heif_module.register_heif_opener = lambda: None
    sys.modules["pillow_heif"] = pillow_heif_module

from pyheic_converter.converter import convert_heic_to_jpeg


class ConvertHeicToJpegTests(unittest.TestCase):
    def test_raises_when_input_missing(self) -> None:
        with self.assertRaises(FileNotFoundError):
            convert_heic_to_jpeg("does-not-exist.heic")

    def test_raises_for_non_heic_suffix(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "image.png"
            path.touch()

            with self.assertRaises(ValueError):
                convert_heic_to_jpeg(path)

    def test_raises_for_invalid_quality(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "image.heic"
            path.touch()

            with self.assertRaises(ValueError):
                convert_heic_to_jpeg(path, quality=0)

            with self.assertRaises(ValueError):
                convert_heic_to_jpeg(path, quality=100)

    @patch("pyheic_converter.converter.Image.open")
    def test_converts_with_default_output_path(self, open_mock: MagicMock) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "image.heic"
            src.touch()

            image_mock = MagicMock()
            image_mock.mode = "RGB"
            open_mock.return_value.__enter__.return_value = image_mock

            out = convert_heic_to_jpeg(src, quality=90)

            self.assertEqual(out, src.with_suffix(".jpg"))
            image_mock.save.assert_called_once_with(
                src.with_suffix(".jpg"), format="JPEG", quality=90, optimize=True
            )

    @patch("pyheic_converter.converter.Image.open")
    def test_converts_alpha_mode_to_rgb(self, open_mock: MagicMock) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            src = Path(tmpdir) / "image.heif"
            dst = Path(tmpdir) / "out" / "image.jpg"
            src.touch()

            image_mock = MagicMock()
            image_mock.mode = "RGBA"
            converted_mock = MagicMock()
            image_mock.convert.return_value = converted_mock
            open_mock.return_value.__enter__.return_value = image_mock

            out = convert_heic_to_jpeg(src, dst)

            self.assertEqual(out, dst)
            image_mock.convert.assert_called_once_with("RGB")
            converted_mock.save.assert_called_once_with(
                dst, format="JPEG", quality=95, optimize=True
            )


if __name__ == "__main__":
    unittest.main()
