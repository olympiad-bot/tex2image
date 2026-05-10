from dataclasses import dataclass


try:
    import requests
except ImportError as e:
    raise RuntimeError(
        "To use the client, please install with:\n\n"
        "        pip install tex2image[client]"
    ) from e


@dataclass(frozen=True)
class TexRenderingClient:
    host: str = "localhost"
    port: int = 8000

    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

    def request_latex_to_png(
        self,
        latex_snippet: str,
        template: str | None = None,
    ) -> bytes:
        """Convert a LaTeX snippet to a PNG image, returning the image bytes.

        See
        [the documentation for `render_latex_snippet`](https://tex2image.readthedocs.io/en/latest/renderer#tex2image.rendering.render_latex_to_png)
        for more information on the parameters.
        """
        response = requests.get(
            f"{self.base_url}/render_latex_snippet",
            params={"latex_snippet": latex_snippet, "template": template},
        )
        response.raise_for_status()
        return response.content
