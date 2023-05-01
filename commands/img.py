import json
import random
from typing import Optional

import discord
from discord import app_commands

from config import (DEFAULT_CFG_SCALE, DEFAULT_HEIGHT, DEFAULT_NEGATIVE_PROMPT,
                    DEFAULT_SAMPLER, DEFAULT_STEPS, DEFAULT_WIDTH)
from job_handler import JOB_IMG


def create_command_with(job_queue):
    @app_commands.describe(
        prompt="This is the input prompt provided to the AI model to guide the image generation process. The prompt is a text description that the AI will use to create the image."
    )
    @app_commands.describe(
        negative_prompt="This parameter is used to provide a prompt that the AI model should avoid generating. It can be helpful for refining the output or ensuring that the generated image does not contain certain elements."
    )
    # @app_commands.describe(
    #     sampler_name="This parameter specifies the name of the sampler used by the AI model for generating the image."
    # )
    @app_commands.describe(
        steps="This parameter controls the number of optimization steps the AI model should take to generate the image. A higher number of steps might result in more detailed and refined output, but it may also take longer to generate"
    )
    @app_commands.describe(
        cfg_scale="This parameter controls the scale of the AI model's configuration. It can affect the quality and size of the generated image."
    )
    @app_commands.describe(width="Width of the generated image")
    @app_commands.describe(height="Height of the generated image")
    @app_commands.describe(
        seed="This parameter sets the random seed used by the AI model for generating the image. A fixed seed will result in the same output every time the program is run with the same input parameters, while a different seed will produce a different output."
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
        await interaction.followup.send("parameters for your request: ")
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
        await interaction.followup.send("please wait while we process your request")

        await job_queue.add_job(
            JOB_IMG, interaction.channel_id, interaction.user, input_data
        )

    return img
