import random
import re
import json

from typing import List

from disnake import ApplicationCommandInteraction, Message, Embed
from disnake.utils import escape_markdown
from disnake.ext import commands
from disnake.ext.commands import Cog, slash_command

from core import Dispy, logger, NEGATIVE_REPLIES, ERROR_COLOR, SUCCESS_COLOR
from utils import ILLEGAL_CHARACTERS, update_json

URL = 'https://pypi.org/pypi/{package}/json'
PYPI_ICON = 'https://cdn.discordapp.com/emojis/766274397257334814.png'

with open("./resources/package_names.json", mode="r+") as package_names:
    PACKAGES = json.load(package_names)


# noinspection PyUnusedLocal
async def autocomplete_pypi(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    return sorted([lang for lang in PACKAGES if string.lower() in lang.lower()][:25])


class PyPi(Cog, name="pypi"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    @slash_command(name="pypi")
    async def get_package_info(
        self, inter: ApplicationCommandInteraction,
        package: str = commands.Param( autocomplete=autocomplete_pypi)
    ) -> Message:
        """ Provide information about a specific package from PyPI """

        embed = Embed(title=random.choice(NEGATIVE_REPLIES), colour=ERROR_COLOR)
        embed.set_thumbnail(url=PYPI_ICON)

        error = True

        if characters := re.search(ILLEGAL_CHARACTERS, package):
            embed.description = f"Illegal character(s) passed into command: '{escape_markdown(characters.group(0))}'"

        else:
            async with self.bot.http_session.get(URL.format(package=package)) as response:
                if response.status == 404:
                    embed.description = "Package could not be found."

                elif response.status == 200 and response.content_type == "application/json":
                    response_json = await response.json()
                    info = response_json["info"]

                    embed.title = f"{info['name']} v{info['version']}"

                    embed.url = info["package_url"]
                    embed.colour = SUCCESS_COLOR

                    if not package.lower() in [p.lower() for p in PACKAGES]:
                        PACKAGES.append(info['name'])
                        await update_json("./resources/package_names.json", PACKAGES)

                        embed.set_footer(
                            text="I have added this PyPi to my database",
                            icon_url="https://emoji.gg/assets/emoji/6308_PandaLove.png"
                            )

                    summary = escape_markdown(info["summary"])

                    # Summary could be completely empty, or just whitespace.
                    if summary and not summary.isspace():
                        embed.description = summary
                    else:
                        embed.description = "No summary provided."

                    error = False

                else:
                    embed.description = "There was an error when fetching your PyPi package."
                    logger.warn(f"Error when fetching PyPi package: {response.status}.")
        if error:
            return await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            return await inter.response.send_message(embed=embed)


def setup(bot: Dispy) -> None:
    """ Load the PyPi cog """
    bot.add_cog(PyPi(bot))
