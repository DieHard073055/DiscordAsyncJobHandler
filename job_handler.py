import asyncio
import base64
import json
import logging
import queue

import aiohttp
import discord

JOB_IMG = "img"
JOB_TXT = "txt"


class JobQueue:
    def __init__(self):
        self.jobs = queue.Queue()

    async def add_job(
        self, job_type: str, channel_id: int, user: str, input: dict[str, str]
    ) -> None:
        logging.info("Added job to queue")
        self.jobs.put((job_type, channel_id, user, input))

    async def run_jobs(self, client: discord.Client, job_function) -> None:
        while True:
            try:
                job_type, channel_id, user, input = self.jobs.get(
                    block=False)
                # Add the following line to see if a job is being executed
                logging.info(f"Job [{job_type}] found, executing...")
            except queue.Empty:
                await asyncio.sleep(1)
                continue

            try:
                job_result = await job_selector(
                    job_type, client, input, channel_id, user
                )
            except Exception as e:
                logging.error(e)

            self.jobs.task_done()


async def job_selector(job_type, client, input, channel_id, user):
    job_type_map = {
        JOB_IMG: job_img,
        JOB_TXT: job_txt,
    }
    # Add the following line to see if the function is being executed
    logging.info("Executing job selector...")
    await job_type_map[job_type](client, input, channel_id, user)
    logging.info("Job execution - done!")


# TODO: find a model that can handle text
async def job_txt(client, input, channel_id, user):
    # Add the following line to see if the function is being executed
    logging.info("Executing /txt job function...")
    url = "http://192.168.1.123:5001/predictions"
    headers = {"Content-Type": "application/json"}
    data = {"input": input}
    result = "lol `/txt` model is down right now. :P"

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         url, headers=headers, data=json.dumps(data)
    #     ) as response:
    #         if response.status == 200:
    #             result = await response.json()
    #             print(result)
    #         else:
    #             logging.error(f"Request failed with status code {response.status}")

    coro = client.get_channel(channel_id).send(f"{user.mention} : {result}")
    future = asyncio.run_coroutine_threadsafe(coro, client.loop)
    future.result()
    logging.info(f"Sent response to {user}.")


async def job_img(client, input, channel_id, user):
    # Add the following line to see if the function is being executed
    logging.info("Executing /img job function...")

    url = "http://192.168.1.123:5000/predictions"
    headers = {"Content-Type": "application/json"}
    data = {"input": input}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers=headers, data=json.dumps(data)
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                png_data = base64.b64decode(
                    response_data["output"].split(",")[1])
                with open("output.png", "wb") as f:
                    f.write(png_data)
            else:
                logging.error(
                    f"Request failed. [Status code: {response.status}]")
                logging.error(response.text)

    data_embed = discord.Embed()
    data_embed.add_field(
        name='prompt', value=input["prompt"], inline=False)
    data_embed.add_field(
        name='width', value=input["width"], inline=True)
    data_embed.add_field(
        name='height', value=input["height"], inline=True)
    data_embed.add_field(
        name="cfg scale", value=input["cfg_scale"], inline=True)
    data_embed.add_field(
        name="steps", value=input["steps"], inline=True)
    data_embed.add_field(
        name="sampler", value=input["sampler_name"], inline=True)
    data_embed.add_field(
        name="seed", value=input["seed"], inline=True)
    data_embed.add_field(
        name="negatives", value=input["negative_prompt"], inline=False)

    coro_items = [
        bot_send_msg(channel_id, client),
        client.get_channel(channel_id).send(
            f"{user.mention}, here's your image:", file=discord.File("output.png"), embed=data_embed
        )
    ]
    for coro in coro_items:
        future = asyncio.run_coroutine_threadsafe(coro, client.loop)
        future.result()
    logging.info(f"Response sent to {user}")


async def bot_send_msg(channel_id: int, client: discord.Client):
    channel = client.get_channel(channel_id)
    await channel.send('✅ Done!')
