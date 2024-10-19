import discord
import requests
import json
import asyncio

# Configuration
OLLAMA_API_URL = 'http://localhost:11434/api/generate'  # URL of the Ollama API
MAX_RESPONSE_LENGTH = 1999  # Maximum length for Discord messages
MODEL_NAME = 'llama3.2'  # Specify the model name to be used
DISCORD_BOT_TOKEN = 'your_bot_token_here'  # Replace with your Discord bot token

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Logs a message when the bot is ready."""
    print(f'Logged in as {client.user}!')

@client.event
async def on_message(message):
    """Handles incoming messages."""
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    if message.content.startswith('!bot'):
        question = message.content[5:].strip()  # Extract the question after "!bot"

        if question:
            async with message.channel.typing():  # Simulate typing
                await asyncio.sleep(1)

                # Fetch response from the Ollama API
                response_chunks = get_response_from_ollama(question)

                # Send the response in chunks to avoid exceeding message length limits
                for chunk in response_chunks:
                    await message.channel.send(chunk[:MAX_RESPONSE_LENGTH])
                    await asyncio.sleep(2)  # Optional delay to avoid rate limits
        else:
            await message.channel.send("Please provide a question after `!bot`.")

def get_response_from_ollama(prompt):
    """
    Sends a prompt to the Ollama API and returns the response as a list of message chunks.
    """
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={'model': MODEL_NAME, 'prompt': prompt},
            stream=True
        )

        if response.status_code != 200:
            return [f'Error: {response.status_code} - {response.text}']

        accumulated_response = ""
        responses = []

        # Stream the response from the API
        for line in response.iter_lines():
            if line:
                try:
                    line_data = line.decode('utf-8')
                    json_data = json.loads(line_data)
                    new_response = json_data.get('response', '')

                    if len(accumulated_response) + len(new_response) > MAX_RESPONSE_LENGTH:
                        responses.append(accumulated_response)
                        accumulated_response = new_response
                        
                        while len(accumulated_response) > MAX_RESPONSE_LENGTH:
                            responses.append(accumulated_response[:MAX_RESPONSE_LENGTH])
                            accumulated_response = accumulated_response[MAX_RESPONSE_LENGTH:]
                    else:
                        accumulated_response += new_response
                except ValueError:
                    continue  # Skip any lines that can't be parsed as JSON

        if accumulated_response:
            responses.append(accumulated_response)

        return responses

    except requests.RequestException as e:
        return [f'Failed to connect to Ollama API: {str(e)}']

# Run the bot
if __name__ == "__main__":
    if DISCORD_BOT_TOKEN == 'your_bot_token_here':
        print("Error: Please set your Discord bot token in the DISCORD_BOT_TOKEN variable.")
    else:
        client.run(DISCORD_BOT_TOKEN)
