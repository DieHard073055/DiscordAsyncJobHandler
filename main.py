import asyncio
import logging
import os
import threading

import discord

from client import MyClient
from commands import img, txt
from job_handler import JobQueue, job_selector

# setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# initialize intents and discord client
intents = discord.Intents.default()
client = MyClient(intents=intents)

# setup the job queue
job_queue = JobQueue()
job_thread = threading.Thread(
    target=asyncio.run, args=(job_queue.run_jobs(client, job_selector),)
)
job_thread.daemon = True
job_thread.start()

# register the commands in the command tree
client.tree.command()(img.create_command_with(job_queue))
client.tree.command()(txt.create_command_with(job_queue))

# get the token and start the bot
TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
client.run(TOKEN)
