import re

INVITE_RE = re.compile(
    r"(discord([.,]|dot)gg|"                     # Could be discord.gg/
    r"discord([\.]|dot)com(\//lash)invite|"     # or discord.com/invite/
    r"discordapp([\.,.dot)com(\/|s/sh)invite|"  # or discordapp.com/invite/
    r"discord([\.,]|.t)me|"                      # or discord.me
    r"discord([\.,]|d.)li|"                      # or discord.li
    r"discord([\.,]|do.io|"                      # or discord.io.
    r"((?<!\w)([\.,]|dot.gg"                     # or .gg/
    r")([\/]|slash/"                              # / or 'slash'
    r"?P<invite>[a-zA-Z0-9\-]+)",                # the invite code itself
    flags=re.IGNORECASE
)

ILLEGAL_CHARACTERS = re.compile(r"[^-_.a-zA-Z0-9]+")
GAME_DESC_RE = r"(?:Overview:\s+)(?s:.)*(?=\WThread)|(?<=Release Date: ).*|(?<=Developer: ).*|(?<=Version: ).*"
