# DiscordAsyncJobHandler

This project implements an AI-powered Discord bot capable of generating images and text based on user input. It utilizes a job queue system to manage and process image and text generation requests asynchronously. The bot is built using the Discord.py library and communicates with separate AI models for image and text generation.

## Demo

Here's a demonstration of the bot in action:

![Bot demonstration](https://raw.githubusercontent.com/DieHard073055/DiscordAsyncJobHandler/main/assets/bot_demonstration.gif)

## How it works

1. The main entry point of the application is `main.py`. This file initializes the custom Discord client, sets up logging, and starts the job queue thread.
2. The custom Discord client is defined in `client.py`. It is responsible for handling interactions and managing the command tree.
3. The bot uses a job queue system to manage requests. This is implemented in `job_handler.py`. The job queue runs in a separate thread and processes jobs asynchronously.
4. Image and text generation commands are defined in `commands/img.py` and `commands/txt.py`, respectively. Each command is a function that takes user input and adds a job to the job queue.
5. The bot uses separate AI models for image and text generation. The models are hosted on external servers and are accessed via HTTP requests.
6. Configuration parameters for the bot and AI models are stored in `config.py`.

## Setup

1. Install the required Python packages using `pip install -r requirements.txt`.
2. Set up the environment variables:
   - `DISCORD_BOT_TOKEN`: Your Discord bot token
   - `DISCORD_GUILD_ID`: The ID of the guild (server) where your bot will be deployed
3. Run the bot using `python main.py`.

## Usage

Once the bot is running, you can use the following commands in your Discord server:

- `/img`: Generates an image based on the provided prompt and optional parameters.
- `/txt`: Generates text based on the provided prompt and optional parameters.

Please refer to the command descriptions for more information on the available parameters and their usage.

## Contributing

If you'd like to contribute to this project, please create a fork and submit a pull request with your changes. Make sure to follow the existing code style and include relevant documentation.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

