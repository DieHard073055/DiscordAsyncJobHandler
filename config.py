import os

import discord

DEFAULT_NEGATIVE_PROMPT = "(ugly:1.331), (worst quality:2), (low quality:2), (normal quality:2), lowres, normal quality, ((monochrome)), ((grayscale)), jpeg artifacts, cropped, blurry"
DEFAULT_SAMPLER = "DPM++ SDE Karras"
DEFAULT_STEPS = 20
DEFAULT_CFG_SCALE = 8
DEFAULT_WIDTH = 512
DEFAULT_HEIGHT = 512

NEGATIVE_PROMPT_PRESET_1 = DEFAULT_NEGATIVE_PROMPT + \
    "paintings, sketches, skin spots, acnes, skin blemishes, age spot, glans, , (duplicate:1.331), (morbid:1.21), (mutilated:1.21), (tranny:1.331), mutated hands, (poorly drawn hands:1.331), 3hands, 4fingers, 3arms, bad anatomy, missing fingers, extra digit, fewer digits ,poorly drawn face ,mutation, deformed"

# TODO: Get this dynamically depending on who subscribe to the bot.
# replace with your guild id
GUILD = discord.Object(id=os.environ.get("DISCORD_GUILD_ID"))
