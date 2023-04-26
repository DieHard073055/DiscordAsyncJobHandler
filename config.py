import os

import discord

DEFAULT_NEGATIVE_PROMPT="paintings, sketches, (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), skin spots, acnes, skin blemishes, age spot, glans, (ugly:1.331), (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.331), blurry, 3hands,4fingers,3arms, bad anatomy, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts,poorly drawn face,mutation,deformed"
DEFAULT_SAMPLER="DPM++ SDE Karras"
DEFAULT_STEPS=20
DEFAULT_CFG_SCALE=8
DEFAULT_WIDTH=512
DEFAULT_HEIGHT=768

# TODO: Get this dynamically depending on who subscribe to the bot.
GUILD = discord.Object(id=os.environ.get("DISCORD_GUILD_ID"))  # replace with your guild id

