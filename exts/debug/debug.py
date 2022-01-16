from disnake import (
    Embed,
    ButtonStyle,
    MessageInteraction,
    Message
)
from disnake.ui import (
    View,
    Button,
    button
)
from disnake.ext.commands import (
    Cog, 
    Context,
    command
)
from core import Dispy

class EmbedFactory:
    """Embed factory"""

    @staticmethod
    def normal_embed(ctx, title: str):
        return Embed(
            title=title,
            colour=0xb82785,
            timestamp=ctx.message.created_at
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url
        )




class ChangeView(View):
    def __init__(self, ctx: Context, bot_message: Message):
        super().__init__()

        self.ctx = ctx
        self.bot_message = bot_message

    @button(label="Name", style=ButtonStyle.green)
    async def name_button(
        self, button: Button, interaction: MessageInteraction
    ): 
        ...

    @button(label="Avatar", style=ButtonStyle.green)
    async def avatar_button(
        self, button: Button, interaction: MessageInteraction
    ):  
        ...

class DebugView(View):
    def __init__(self, ctx: Context):
        super().__init__()

        self.ctx = ctx

    @button(label="Echo", style=ButtonStyle.green)
    async def echo_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        args:
            -> user/channel
            -> message
        """

    @button(label="Blacklist", style=ButtonStyle.green)
    async def blacklist_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        args:
            -> user/guild/channel
            -> duration
        """
        ...

        #TODO: append to db

    @button(label="Leave guild", style=ButtonStyle.green)
    async def leave_guild_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        args:
            -> guild (fuzzy)"""

    @button(label="Change", style=ButtonStyle.green)
    async def change_button(
        self, button: Button, interaction: MessageInteraction
    ):  
        embed = EmbedFactory.normal_embed(self.ctx, "What would you like to change?")

        await self.bot_message.edit(embed=embed, view=ChangeView(self.ctx, self.bot_message))
   
class Debug(Cog, name='debug'):
    def __init__(self, bot: Dispy) -> None:
        self.bot = bot

    async def cog_check(self, ctx: Context) -> bool:
        return await self.bot.is_owner(ctx.author)

    @command(hidden=True)
    async def debug(self, ctx):
        """
        echo:
            -> user
            -> channel
                => send message

        blacklist:
            -> user
            -> guild
                => blacklist 

        leave_guild:
            -> guild
                => leave guild
        """

        embed = EmbedFactory.normal_embed(ctx, "Debug Controls")
        view = DebugView(ctx)

        view.bot_message = await ctx.send(embed=embed, view=view)


def setup(bot: Dispy) -> None:
    """ Load the Debug extension """

    bot.add_cog(Debug(bot))