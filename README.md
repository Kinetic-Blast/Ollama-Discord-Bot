# Discord Bot with Ollama API Integration

This project is a simple Discord bot that integrates with the Ollama API to generate responses based on user questions. When a user sends a message starting with `!bot`, the bot will forward the question to the Ollama API and return the response in chunks, ensuring the message length does not exceed Discord's limits.

## Features

- Responds to messages that start with `!bot` and returns the generated response.
- Splits responses into manageable chunks to avoid exceeding Discord's message length limit.
- Simulates typing to provide a better user experience.

## Requirements

- Python 3.7 or higher
- A Discord bot token (you can get one by creating a bot on the [Discord Developer Portal](https://discord.com/developers/applications))
- The Ollama API running locally or accessible from the specified URL
