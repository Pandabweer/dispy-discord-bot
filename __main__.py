import logging

from bot import DCBot
from constants import config

bot = DCBot.create()
bot.load_extensions()
bot.run(config.bot.token)
