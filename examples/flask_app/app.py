from flask import Flask, Response

from tex2image.client import TexRenderingClient


app = Flask(__name__)


@app.route("/")
def hello():
    return "This is an example webpage.\n<img src='/latex_image.png'>"


@app.route("/latex_image.png")
def latex_image():
    client = TexRenderingClient()
    return Response(
        client.request_latex_to_png("Pythagorean Theorem: $a^2 + b^2 = c^2$."),
        mimetype="image/png",
    )
