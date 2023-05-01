import json
import random
from typing import Optional

import discord
from discord import app_commands

from config import (DEFAULT_CFG_SCALE, DEFAULT_HEIGHT, DEFAULT_NEGATIVE_PROMPT,
                    DEFAULT_SAMPLER, DEFAULT_STEPS, DEFAULT_WIDTH, NEGATIVE_PROMPT_PRESET_1)
from job_handler import JOB_IMG


def create_command_with(job_queue):
    # @app_commands.describe(
    #     sampler_name="This parameter specifies the name of the sampler used by the AI model for generating the image."
    # )
    @app_commands.describe(
        prompt="Enter your prompt or a description of your image."
    )
    @app_commands.describe(
        negative_prompt="Set a negative prompt as a method to 'avoid' critierias. Example: mutated hands"
    )
    @app_commands.describe(
        steps="[Default: 20] Set the number of steps of image optimization. The higher the number, the longer the processing time, but the more detailed and refined is the output."
    )
    @app_commands.describe(
        cfg_scale="[Default: 8] Set the scale of the AI model's configuration. It affects the quality and size of the generated image."
    )
    @app_commands.describe(width="Image width in px. [Default: 512]")
    @app_commands.describe(height="Image height in px. [Default: 768]")
    @app_commands.describe(
        seed="A set of random seed is used by the AI to generate the image. A fixed seed will result in the same output, given the same input parameters. Different seed will produce a different output."
    )
    async def img(
        interaction: discord.Interaction,
        prompt: str,
        negative_prompt: Optional[str] = None,
        # sampler_name: Optional[str] = None,
        steps: Optional[int] = None,
        cfg_scale: Optional[int] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        seed: Optional[int] = None,
    ):
        await interaction.response.defer()
        input_data = {
            "prompt": prompt,
            "negative_prompt": negative_prompt or DEFAULT_NEGATIVE_PROMPT,
            "sampler_name": DEFAULT_SAMPLER,
            "steps": str(steps or DEFAULT_STEPS),
            "cfg_scale": str(cfg_scale or DEFAULT_CFG_SCALE),
            "width": str(width or DEFAULT_WIDTH),
            "height": str(height or DEFAULT_HEIGHT),
            "seed": str(seed or random.randint(1, 10000000)),
        }
        await interaction.followup.send(
            f"```{json.dumps(input_data, indent=4, default=str)}```"
        )
        await interaction.followup.send("Generating...")

        await job_queue.add_job(
            JOB_IMG, interaction.channel_id, interaction.user, input_data
        )

    return img
