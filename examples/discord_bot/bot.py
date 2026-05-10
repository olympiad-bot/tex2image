import os
from io import BytesIO

import certifi

os.environ["SSL_CERT_FILE"] = certifi.where()

import discord
from discord import app_commands

from tex2image.client import TexRenderingClient


MY_TEST_GUILD = discord.Object(id=input("Enter TEST_GUILD_ID: "))


class LatexBotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_TEST_GUILD)
        await self.tree.sync(guild=MY_TEST_GUILD)
        await self.tree.sync()


intents = discord.Intents.default()
client = LatexBotClient(intents=intents)


@client.tree.command()
@app_commands.user_install()
@app_commands.describe(latex_snippet="Latex snippet to render.")
async def latex(interaction: discord.Interaction, latex_snippet: str) -> None:
    """Render `latex_snippet` to an image."""
    tex2image_client = TexRenderingClient()
    await interaction.response.send_message(
        file=discord.File(
            BytesIO(tex2image_client.request_latex_to_png(latex_snippet)),
            filename="latex.png",
        )
    )


client.run(input("Enter token: "))
