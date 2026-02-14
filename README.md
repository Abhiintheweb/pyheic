# pyheic

Python package to convert `.heic` / `.heif` images into `.jpg`.

## Install

```bash
pip install pyheic
```

For local development:

```bash
pip install -e .
```

## CLI usage

```bash
heic2jpeg input.heic
heic2jpeg input.heic --output output.jpg --quality 90
```

## Python usage

```python
from pyheic import convert_heic_to_jpeg

output = convert_heic_to_jpeg("input.heic", quality=90)
print(output)
```
