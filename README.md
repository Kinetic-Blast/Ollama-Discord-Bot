# Discord Bot with Ollama API Integration (v2)

This project is a Discord bot that integrates with the Ollama API to generate conversational responses. The bot listens for messages in a specific channel and maintains a short-term memory of the last five user messages and bot responses to provide context-aware replies.

## Features

- **Memory Management**: Keeps track of the last 5 user messages and bot responses for a richer conversational context.
- **Channel-Specific Interaction**: Only listens to a specified source channel for user messages.
- **Custom Commands**: Includes a `!clear` command to reset both user and bot memories with a fun acknowledgment message.
- **Chunked Responses**: Splits responses into manageable chunks to avoid exceeding Discord's message length limit.
- **Simulated Typing**: Simulates typing to enhance the user experience.

## Updates in v2

- **Memory Integration**: Added short-term memory storage using `deque` to maintain context.
- **Customizable Placeholders**: Removed hardcoded sensitive data like bot token, channel ID, and API URL. These are now placeholders (`<bot_token>`, `<source_channel_id>`, `<ollama_api_url>`).
- **Improved Clear Command**: Clearing memory now sends a humorous acknowledgment message.
- **Typing Indicator**: Shows the bot is typing while processing user input.

## Requirements

- Python 3.7 or higher
- A Discord bot token (can be obtained from the [Discord Developer Portal](https://discord.com/developers/applications)).
- The Ollama API running locally or accessible via a specified URL.

## Usage

- **Conversation**: Post a message in the specified source channel. The bot will process the message and respond based on context.
- **Clear Memory**: Use the `!clear` command in any channel to reset the bot's memory.

## Notes

- Ensure the Ollama API is running and accessible from the bot.
- Replace the placeholders with actual values before deploying the bot.

---
# Discord Bot with Ollama API Integration V1

This project is a simple Discord bot that integrates with the Ollama API to generate responses based on user questions. When a user sends a message starting with !bot, the bot will forward the question to the Ollama API and return the response in chunks, ensuring the message length does not exceed Discord's limits.

## Features

- Responds to messages that start with !bot and returns the generated response.
- Splits responses into manageable chunks to avoid exceeding Discord's message length limit.
- Simulates typing to provide a better user experience.

## Requirements

- Python 3.7 or higher
- A Discord bot token (you can get one by creating a bot on the [Discord Developer Portal](https://discord.com/developers/applications))
- The Ollama API running locally or accessible from the specified URL
