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
        self, job_type: str, channel_id: int, user_name: str, input: dict[str, str]
    ) -> None:
        logging.info("Adding a job to the queue")
        self.jobs.put((job_type, input, channel_id, user_name))

    async def run_jobs(self, client: discord.Client, job_function) -> None:
        while True:
            try:
                job_type, input, channel, user_id = self.jobs.get(block=False)
                logging.info(
                    f"Job [{job_type}] found, executing..."
                )  # Add this line to see if a job is being executed
            except queue.Empty:
                await asyncio.sleep(1)
                continue

            try:
                job_result = await job_selector(
                    job_type, client, input, channel, user_id
                )
            except Exception as e:
                logging.error(e)

            self.jobs.task_done()


async def job_selector(job_type, client, input, channel_id, user_name):
    job_type_map = {
        JOB_IMG: job_img,
        JOB_TXT: job_txt,
    }
    logging.info(
        "Executing job selector..."
    )  # Add this line to see if the function is being executed
    await job_type_map[job_type](client, input, channel_id, user_name)
    logging.info(f"done executing job")


# TODO: find a model that can handle text
async def job_txt(client, input, channel_id, user_name):
    logging.info(
        "Executing txt job function..."
    )  # Add this line to see if the function is being executed
    url = "http://192.168.1.123:5001/predictions"
    headers = {"Content-Type": "application/json"}
    data = {"input": input}
    result = "lol text model is down right now."

    # async with aiohttp.ClientSession() as session:
    #     async with session.post(
    #         url, headers=headers, data=json.dumps(data)
    #     ) as response:
    #         if response.status == 200:
    #             result = await response.json()
    #             print(result)
    #         else:
    #             logging.error(f"Request failed with status code {response.status}")

    coro = client.get_channel(channel_id).send(f"@{user_name}: {result}")
    future = asyncio.run_coroutine_threadsafe(coro, client.loop)
    future.result()
    logging.info(f"sending response to @{user_name}")


async def job_img(client, input, channel_id, user_name):
    logging.info(
        "Executing img job function..."
    )  # Add this line to see if the function is being executed
    url = "http://192.168.1.123:5000/predictions"
    headers = {"Content-Type": "application/json"}
    data = {"input": input}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            url, headers=headers, data=json.dumps(data)
        ) as response:
            if response.status == 200:
                response_data = await response.json()
                png_data = base64.b64decode(response_data["output"].split(",")[1])
                with open("output.png", "wb") as f:
                    f.write(png_data)
            else:
                logging.error(f"Request failed with status code {response.status}")
                logging.error(response.text)

    coro = client.get_channel(channel_id).send(
        f"@{user_name} Here's your image!", file=discord.File("output.png")
    )
    future = asyncio.run_coroutine_threadsafe(coro, client.loop)
    future.result()
    logging.info(f"sending response to @{user_name}")
