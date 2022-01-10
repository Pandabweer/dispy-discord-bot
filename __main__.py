from socket import gethostname, gethostbyname
from os import system

from core import Dispy, config, logger

if __name__ == '__main__':
    system('cls')
    logger.info(f"Starting bot for {gethostname()} at {gethostbyname(gethostname())}")
    bot = Dispy.create()
    bot.load_extensions()

    logger.info(f"Attempting to connect to Discord..")
    bot.run(config.bot.token, reconnect=True)
