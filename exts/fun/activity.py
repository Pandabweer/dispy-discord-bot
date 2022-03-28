import json
import math
import random

from typing import Tuple

from disnake import ApplicationCommandInteraction, Message, Member, VoiceChannel
from disnake.ext import tasks
from disnake.ext.commands import Cog, slash_command, Param

from core import Dispy, logger
from core.constants import config

together_apps = {
    'youtube': '880218394199220334',
    'poker': '755827207812677713',
    'betrayal': '773336526917861400',
    'fishing': '814288819477020702',
    'chess': '832012774040141894',
    'letter-tile': '879863686565621790',
    'word-snack': '879863976006127627',
    'doodle-crew': '878067389634314250',
    'spellcast': '852509694341283871',
    'awkword': '879863881349087252',
    'checkers': '832013003968348200',
}


class Activity(Cog, name='discord-together'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot
        self.monkey.start()
        self.temp_solution = []

    def cog_unload(self):
        self.monkey.cancel()

    @tasks.loop(minutes=1.0, reconnect=True)
    async def monkey(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(957359105977229403)
        index = random.randint(0, 191)
        url = f"https://www.googleapis.com/customsearch/v1?key={config.google.API_KEY}&cx={config.google.SEARCH_ENGINE_ID}&q=monkey&searchType=image&start={index}"

        async with self.bot.http_session.get(url) as r:
            data = json.loads((await r.text()))

            links = [x["link"] for x in data['items'] if not x["link"] in self.temp_solution]
            rand_img = random.choice(links)

            self.temp_solution.append(rand_img)

        await channel.send(rand_img)

    async def create_together_url(self, voice_channel_id: int, option: str) -> Tuple[str, bool]:
        data = {
            'max_age': 0,
            'max_uses': 0,
            'target_application_id': together_apps[option],
            'target_type': 2,
            'temporary': False,
            'validate': None
        }

        async with self.bot.http_session.post(
                f"https://discord.com/api/v8/channels/{voice_channel_id}/invites", json=data,
                headers={'Authorization': f'Bot {config.bot.token}', 'Content-Type': 'application/json'}
        ) as resp:
            resp_code = resp.status
            result = await resp.json()

        if resp_code == 429:
            logger.warn("I'm getting rate limited smh")
            return "I could not create an activity right now, please try again later.", True
        elif resp_code == 401 or resp_code == 403:
            logger.warn("Authorization header is missing or invalid, check the token")
            return "I can't create an activity right now.", True

        elif result['code'] == 10003 or (result['code'] == 50035 and 'channel_id' in result['errors']):
            logger.debug("Someone passed an invalid voice channel id")
            return "Invalid channel id, did you pass a voice channel?", True
        elif result['code'] == 50013:
            logger.debug("Missing CREATE_INSTANT_INVITE permissions for that voice channel")
            return "I don't have permission to create and invite in that voice channel.", True
        elif result['code'] == 130000:
            logger.warn("API is overloaded")
            return "I could not create an activity right now, please try again later.", True

        return f"[Click me ONCE](https://discord.gg/{result['code']} 'Activity url')", False

    @slash_command(name="activity")
    async def together_activity(
        self, inter: ApplicationCommandInteraction,
        channel: VoiceChannel,
        activity: str = Param(choices=list(together_apps.keys()))
        ) -> Message:
        """ Start or join a voice channel activity """

        msg, hidden = await self.create_together_url(channel.id, activity)
        await inter.send(msg, ephemeral=hidden, delete_after=300)


def setup(bot: Dispy) -> None:
    """ Load the Activity cog """
    bot.add_cog(Activity(bot))
