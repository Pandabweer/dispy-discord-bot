from datetime import datetime

def time_now_format() -> str:
    return f"<t:{round(datetime.now().timestamp())}:R>"