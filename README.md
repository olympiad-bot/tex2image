# tex2image
<!-- --8<-- [start:tex2image] -->

[![Documentation Status](https://readthedocs.org/projects/tex2image/badge/?version=latest)](https://tex2image.readthedocs.io/en/latest/?badge=latest)
[![PyPI Version](https://img.shields.io/pypi/v/tex2image.svg)](https://pypi.python.org/pypi/tex2image)

This is a simple library to generate images from tex snippets.

It uses the [standalone](https://ctan.org/pkg/standalone) latex package to
produce PDFs that are already set to an appropriate size, and then uses
[poppler](https://poppler.freedesktop.org/) to convert the PDF to an image.
You must make sure that `pdflatex` (available from TeX Live) and `pdftoppm`
(available in many package managers, and usually distributed as part of
poppler-utils) are available for python to execute.
<!-- --8<-- [end:tex2image] -->

## Quick start
<!-- --8<-- [start:quickstart] -->

### Direct usage

Once you have installed `pdflatex` and `pdftoppm`, you can use the library like
so:

```python
from pathlib import Path
from tempfile import TemporaryDirectory

from tex2image import latex_to_png

with TemporaryDirectory() as temp_dir:
    image_file_path = latex_to_png("Pythagorean Theorem: $a^2 + b^2 = c^2$.", Path(temp_dir))
    # Do something with the image here, before temp_dir gets deleted...
```

### Client / server method

If you would like to install the `pdflatex` and `pdftoppm` dependencies in a
container, then you may wish to use the simple FastAPI server included in this
library.
To launch the server, run

```bash
pip install tex2image[server]
tex2image-server
# Or run `tex2image-server --help` to see available options.
```

Alternatively, this library distributes an official Docker image:

```bash
docker run --rm -it ghcr.io/olympiad-bot/tex2image
```

Both methods will serve a FastAPI server: navigate to `[host]:[port]/docs`
(`localhost:8000/docs` by default) for OpenAPI documentation for the server.

The server can be easily interacted with from python by using the
`tex2image.client` module.
For example:

```python
from tex2image import TexRenderingClient

c = TexRenderingClient()
image_bytes = c.latex_to_png("Pythagorean Theorem: $a^2 + b^2 = c^2$.")
```

For some more useful examples, see the `examples` folder; in particular, for
examples of using the client, see the Discord bot example and the Flask app
example.

<!-- --8<-- [end:quickstart] -->
