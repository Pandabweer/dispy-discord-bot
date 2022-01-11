import random

from disnake import ApplicationCommandInteraction, Message, Member
from disnake.ext.commands import AutoShardedBot, Cog, slash_command

from core import Dispy


class Fun(Cog, name='fun'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

        self.attack_random = [
            "Heavy blow! You struck <enemy_user> and he fatally bleeds to death.",
            "Whilst walking towards <enemy_user> you tripped and fell into a ravine.",
            "You slipped and died."
            ]

    def random_attack(self, member: Member) -> str:
        return random.choice(self.attack_random).replace('<enemy_user>', member.mention)

    @slash_command(name="kill")
    async def kill_user(self, inter: ApplicationCommandInteraction, member: Member) -> Message:
        if inter.author.id == member.id:
            # Suicide
            return await inter.response.send_message('Ow awwie why would i hurt myself..?', ephemeral=True)

        if member.bot:
            # Death guaranteed
            return await inter.response.send_message(f'I am made of steel {inter.author.mention}!', ephemeral=True)

        return await inter.response.send_message(self.random_attack(member))


def setup(bot: Dispy) -> None:
    """ Load the fun cog """
    bot.add_cog(Fun(bot))
