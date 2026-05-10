import logging
from pathlib import Path
from subprocess import CalledProcessError
from tempfile import TemporaryDirectory
from typing import Literal

try:
    import click
    import uvicorn
    from fastapi import FastAPI
    from fastapi.responses import FileResponse, JSONResponse
    from pydantic import BaseModel
    from starlette.background import BackgroundTask
except ImportError as e:
    raise RuntimeError(
        "To use the server, please install with:\n\n"
        "        pip install tex2image[server]"
    ) from e
from tex2image.rendering import DEFAULT_TEMPLATE, render_latex_to_png

app = FastAPI()


class Message(BaseModel):
    message: str


@app.get(
    "/render_latex_snippet",
    response_model=None,
    responses={200: {"content": {"image/png": {}}}, 500: {"model": Message}},
)
async def render_latex_snippet(
    latex_snippet: str, template: str | None = DEFAULT_TEMPLATE
) -> FileResponse | JSONResponse:
    """Render `latex_snippet` to a png and return it.

    See
    [documentation for tex2image.latex_to_png](https://tex2image.readthedocs.io/en/latest/renderer#tex2image.rendering.render_latex_to_png)
    for more information on the `template` parameter.
    """
    temp_dir = TemporaryDirectory()
    temp_dir_name = Path(temp_dir.name)
    try:
        image_file = render_latex_to_png(latex_snippet, temp_dir_name, template)
    except CalledProcessError:
        return JSONResponse(
            status_code=500,
            content=Message(message="Exception while rendering.").model_dump(),
        )
    return FileResponse(
        image_file, media_type="image/png", background=BackgroundTask(temp_dir.cleanup)
    )


@app.get("/ping")
def ping() -> Literal["pong"]:
    return "pong"


class PingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /ping") == -1


@click.command(name="tex2image-server")
@click.option(
    "--host", default="127.0.0.1", help="Host to listen on.", show_default=True
)
@click.option("--port", default=8000, help="Port to listen on.", show_default=True)
def _tex2image_server(host: str, port: int) -> None:
    """Serve the tex2image server using uvicorn and FastAPI on `host`:`port`.

    Navigate to [host]:[port]/docs to view automatic interactive API documentation
    (provided by Swagger UI).
    """
    run_server(host, port)


def run_server(host: str, port: int) -> None:
    """Serve the tex2image server using uvicorn and FastAPI on `host`:`port`.

    Navigate to [host]:[port]/docs to view automatic interactive API documentation
    (provided by Swagger UI).

    Parameters:
        host: The host to listen on.

        port: The port to listen on.

    Example:

    ```bash
    run_server("127.0.0.1", 8000)
    ```
    """
    logging.getLogger("uvicorn.access").addFilter(PingFilter())
    uvicorn.run(app, host=host, port=port)
