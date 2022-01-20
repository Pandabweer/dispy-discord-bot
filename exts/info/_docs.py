import disnake
import io
import os
import re
import zlib

from typing import List

from disnake import ApplicationCommandInteraction, Message, Embed
from disnake.ext.commands import Cog, slash_command, Param

from core import Dispy, logger

CACHE_NAMES = []
PAGE_TYPES = {
    "python": "https://docs.python.org/3",
    "discord.py": "https://discordpy.readthedocs.io/en/master",
    "disnake": "https://docs.disnake.dev/en/latest"
}


# noinspection PyUnusedLocal
async def autocomplete_docs(inter: ApplicationCommandInteraction, string: str) -> List[str]:
    return sorted([lang for lang in CACHE_NAMES if string.lower() in lang.lower()][:25])


def parse_object_inv(stream, url):
    # key: URL
    # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
    result = {}

    # first line is version info
    inv_version = stream.readline().rstrip()

    if inv_version != '# Sphinx inventory version 2':
        raise RuntimeError('Invalid objects.inv file version.')

    # next line is "# Project: <name>"
    # then after that is "# Version: <version>"
    projname = stream.readline().rstrip()[11:]
    version = stream.readline().rstrip()[11:]

    # next line says if it's a zlib header
    line = stream.readline()
    if 'zlib' not in line:
        raise RuntimeError('Invalid objects.inv file, not z-lib compatible.')

    # This code mostly comes from the Sphinx repository.
    entry_regex = re.compile(r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
    for line in stream.read_compressed_lines():
        match = entry_regex.match(line.rstrip())
        if not match:
            continue

        name, directive, prio, location, dispname = match.groups()
        domain, _, subdirective = directive.partition(':')
        if directive == 'py:module' and name in result:
            # From the Sphinx Repository:
            # due to a bug in 1.1 and below,
            # two inventory entries are created
            # for Python modules, and the first
            # one is correct
            continue

        # Most documentation pages have a label
        if directive == 'std:doc':
            subdirective = 'label'

        if location.endswith('$'):
            location = location[:-1] + name

        key = name if dispname == '-' else dispname
        prefix = f'{subdirective}:' if domain == 'std' else ''

        if projname in ['discord.py', 'nextcord', 'disnake']:
            key = key.replace('discord.ext.commands.', '').replace('discord.', '')

        result[f'{prefix}{key}'] = os.path.join(url, location)

    return result


class SphinxObjectFileReader:
    # Inspired by Sphinx's InventoryFileReader
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')


class Docs(Cog, name="documents"):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot
        self.cache = {}
        self.cache_name = []

    async def cog_load(self):
        await self.cache_docs()

    async def cache_docs(self):
        global CACHE_NAMES
        cache = {}

        for key, page in PAGE_TYPES.items():
            cache[key] = {}

            async with self.bot.http_session.get(page + '/objects.inv') as resp:
                if resp.status != 200:
                    logger.warn("Cannot fetch discord inventory right now")

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = parse_object_inv(stream, page)

        self.cache = {key: value for d in cache.keys() for key, value in cache[d].items()}
        CACHE_NAMES = [key for d in cache.keys() for key, value in cache[d].items()]

    @slash_command(name="docs")
    async def documentation(
        self, inter: ApplicationCommandInteraction,
        item: str = Param(autocomplete=autocomplete_docs)
        ) -> Message:
        """ Get the document for the provided item """

        if item not in self.cache:
            return await inter.send("I have no documentation for this.", ephemeral=True)

        await inter.send(self.cache[item], ephemeral=True)


def setup(bot: Dispy) -> None:
    """ Load the Docs cog """
    bot.add_cog(Docs(bot))
