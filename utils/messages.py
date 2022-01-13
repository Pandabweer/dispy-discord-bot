from datetime import datetime

def time_discord_format(custom: datetime = None) -> str:
    if custom:
        return f"<t:{round(custom.timestamp())}:R>"
    return f"<t:{round(datetime.now().timestamp())}:R>"
