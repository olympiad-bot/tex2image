A simple Discord bot that provides a command `/latex` that renders a
latex snippet as a PNG and sends to the chat.

You will need to start a `tex2image` server (running on `localhost:8000`) before
running this example.
The easiest way to do this (assuming you have Docker installed) is to run

```bash
docker run --rm -p 8000:8000 -it ghcr.io/olympiad-bot/tex2image
```

You can then run the example (in a separate terminal) using

```bash
uv run --extra examples python bot.py
```

Note that the `--extra examples` flag in this command is to ensure that the
necessary the `discord` library is installed into the virtual environment before
running the example.
