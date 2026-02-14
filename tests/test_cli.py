from __future__ import annotations

import io
import unittest
from pathlib import Path
import sys
import types
from unittest.mock import patch

# Allow tests to run without optional runtime deps installed.
if "PIL" not in sys.modules:
    pil_module = types.ModuleType("PIL")
    pil_module.Image = types.SimpleNamespace(open=lambda *_args, **_kwargs: None)
    sys.modules["PIL"] = pil_module

if "pillow_heif" not in sys.modules:
    pillow_heif_module = types.ModuleType("pillow_heif")
    pillow_heif_module.register_heif_opener = lambda: None
    sys.modules["pillow_heif"] = pillow_heif_module

from pyheic_converter.cli import main


class CliTests(unittest.TestCase):
    @patch("pyheic_converter.cli.convert_heic_to_jpeg")
    def test_main_success(self, convert_mock) -> None:
        convert_mock.return_value = Path("output.jpg")
        stdout = io.StringIO()

        with patch("sys.argv", ["heic2jpeg", "input.heic"]), patch(
            "sys.stdout", stdout
        ):
            rc = main()

        self.assertEqual(rc, 0)
        convert_mock.assert_called_once_with(Path("input.heic"), None, quality=95)
        self.assertIn("Created: output.jpg", stdout.getvalue())

    @patch("pyheic_converter.cli.convert_heic_to_jpeg")
    def test_main_error(self, convert_mock) -> None:
        convert_mock.side_effect = ValueError("bad input")
        stderr = io.StringIO()

        with patch("sys.argv", ["heic2jpeg", "input.heic"]), patch(
            "sys.stderr", stderr
        ):
            rc = main()

        self.assertEqual(rc, 1)
        self.assertIn("Error: bad input", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
