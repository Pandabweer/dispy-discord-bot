from disnake import Member, Guild

async def member_get_or_fetch(guild: Guild, member_id: int) -> Member:
    return guild.get_member(member_id) or await guild.fetch_member(member_id)
