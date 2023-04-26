import json
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from config import *
from job_handler import JOB_TXT, JobQueue


def create_command_with(job_queue):
    @app_commands.describe(
        prompt="This is the input prompt provided to the AI model to guide the text generation process. The prompt is a text description that the AI will respond to."
    )
    async def txt(
        interaction: discord.Interaction,
        prompt: str,
        # sampler_name: Optional[str] = None,
    ):
        await interaction.response.defer()
        await interaction.followup.send("parameters for your request: ")
        input_data = {
            "prompt": prompt,
            "top_p": str(1),
            "temperature": str(0.75),
            "max_new_tokens": str(499),
            "repetition_penalty": str(1.2)
        }
        await interaction.followup.send(f"```{json.dumps(input_data, indent=4, default=str)}```")
        await interaction.followup.send("please wait while we process your request")

        await job_queue.add_job(JOB_TXT, interaction.channel_id, interaction.user.name, input_data)

    return txt

