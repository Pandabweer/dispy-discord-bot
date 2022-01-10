import re

from typing import List

from disnake import ApplicationCommandInteraction, Message, Embed
from disnake.utils import escape_markdown
from disnake.ext import commands
from disnake.ext.commands import AutoShardedBot, Cog, slash_command

from core import logger

URL = 'https://pypi.org/pypi/{package}/json'
PYPI_ICON = 'https://cdn.discordapp.com/emojis/766274397257334814.png'

ILLEGAL_CHARACTERS = re.compile(r"[^-_.a-zA-Z0-9]+")
PACKAGES = [
    'Disnake', 'Aiohttp', 'Requests', 'Python-dotenv', 'PyYAML', 'Beautiful Soup', 'Importlib', 'Asyncpg',
    'Coloredlogs', 'Setuptools'
    ]


async def autocomplete_pypi(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    return [lang for lang in PACKAGES if string.lower() in lang.lower()]


class PyPi(Cog, name="pypi"):
    def __init__(self, bot: AutoShardedBot) -> None:
        self.bot = bot

    @slash_command(name="pypi", guild_ids=[561662622827806721, 926115595307614249])
    async def get_package_info(
            self,
            inter: ApplicationCommandInteraction,
            package: str = commands.Param(autocomplete=autocomplete_pypi)
        ) -> Message:
        """ Provide information about a specific package from PyPI """
        embed = Embed(title="Nuh-uh.", colour=0xF47174)  # Soft red
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
                    embed.colour = 0xACD1AF  # Soft green

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
            await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            return await inter.response.send_message(embed=embed)


def setup(bot: AutoShardedBot) -> None:
    """ Load the PyPi cog """
    bot.add_cog(PyPi(bot))
