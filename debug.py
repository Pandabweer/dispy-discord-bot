from disnake import (
    Embed,
    ButtonStyle,
    MessageInteraction,
    Message,
    SelectOption,
    Guild
)
from disnake.ui import (
    View,
    Button,
    Select,
    button
)
from disnake.ext.commands import (
    Cog,
    Context,
    command
)
from core import Dispy

def get_bot_message(ctx: Context):
    return ctx.bot.bot_messages[ctx.message.id]

class EmbedFactory:
    """Embed factory"""

    @staticmethod
    def static_embed(
        ctx: Context,
        title: str,
        *,
        path: str = None,
        description: str = None
    ):
        return Embed(
            title=title,
            colour=0xb82785,
            description=f"```yaml\nCurrent path: /{path or ''}```{'```' + description + '```' if description else ''}",
            timestamp=ctx.message.created_at
        ).set_author(
            name=ctx.author.name,
            icon_url=ctx.author.avatar.url
        )

class ConfirmLeave(View):
    def __init__(self, ctx: Context, guild: Guild) -> None:
        self.ctx = ctx
        self.guild = guild

    @button(label="Yes", style=ButtonStyle.green)
    async def confirm_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        leave guild
            -> return to leave_guild dialog
        """

        ...

    @button(label="No", style=ButtonStyle.danger)
    async def cancel_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        dont leave guild
            -> return to leave_guild dialog
        """
        ...

class Utilities:
    def __init__(self, ctx: Context) -> None:
        self.bot = ctx.bot
        self.ctx = ctx
        self.bot_message = get_bot_message(ctx)

    async def other_guilds(self, interaction: MessageInteraction, clicked: str) -> None:
        ...

    async def find_guilds(self, interaction: MessageInteraction, clicked: str) -> None:
        guilds = [k for k in self.bot.guilds if k.name.startswith(clicked)]
        if not guilds:
            return await interaction.response.send_message(f"I am in no guilds starting with {clicked}")
        if len(guilds) == 1:
            embed = EmbedFactory.static_embed(
                        self.ctx,
                        f"Would you like me to leave {guilds[0].name}?",
                        path="leave_guild/confim"
                    )
            return await self.bot_message.edit(embed, embed, view=ConfirmLeave(ctx, guilds[0])))

        embed = EmbedFactory.static_embed(self.ctx, f"Which guild?" )
        await self.bot_message.edit(embed=embed)

class SelectPZ(Select):
    def __init__(self, ctx: Context):
        super().__init__()

        self.bot = ctx.bot
        self.utils = Utilities(ctx)
        self.options = [
            SelectOption(label=str(k), value=str(k)) for k in [chr(a) for a in range(112, 123)]
        ]
        self.options.append(SelectOption(label="Other", value="other"))
        self.placeholder = "P-Z"

    async def callback(self, interaction: MessageInteraction) -> None:
        clicked = self.values[0]
        if clicked == "other":
            return await self.utils.find_other_guilds(interaction)
        await self.utils.find_guilds(interaction)

class SelectAO(Select):
    def __init__(self, ctx: Context):
        super().__init__()

        self.bot = ctx.bot
        self.utils = Utilities(ctx)
        self.options = [
            SelectOption(label=str(k), value=str(k)) for k in [chr(a) for a in range(97, 112)]
        ]
        self.options.append(SelectOption(label="Other", value="other"))
        self.placeholder = "A-O"

    async def callback(self, interaction: MessageInteraction) -> None:
        clicked = self.values[0]
        if clicked == "other":
            return await self.utils.find_other_guilds(interaction, clicked)
        await self.utils.find_guilds(interaction, clicked)

class SelectView(View):
    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

    def __init__(self, ctx: Context):
        super().__init__()

        self.ctx = ctx
        self.add_item(SelectAO(ctx))
        self.add_item(SelectPZ(ctx))

class ChangeView(View):
    def __init__(self, ctx: Context):
        super().__init__()

        self.ctx = ctx
        self.bot_message = get_bot_message(ctx)

    async def interaction_check(self, interaction: MessageInteraction) -> bool:
        return (
            interaction.author == self.ctx.author
            and interaction.channel == self.ctx.channel
        )

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
        self.bot_message = get_bot_message(ctx)

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

        embed = EmbedFactory.static_embed(self.ctx, "What guild would you like to edit?", "leave_guild")

        await interaction.response.defer()
        await self.bot_message.edit(embed=embed, view=SelectView(self.ctx))

    @button(label="Change", style=ButtonStyle.green)
    async def change_button(
        self, button: Button, interaction: MessageInteraction
    ):
        """
        args:
            -> name/avatar
        """

        embed = EmbedFactory.static_embed(self.ctx, "What would you like to change?", "change")

        await interaction.response.defer()
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

        embed = EmbedFactory.static_embed(ctx, "Debug Controls")
        self.bot.bot_messages[ctx.message.id] = await ctx.send(embed=embed, view=DebugView(ctx))


def setup(bot: Dispy) -> None:
    """ Load the Debug extension """

    bot.add_cog(Debug(bot))