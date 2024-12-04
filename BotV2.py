import discord
import requests
import json
import asyncio
from collections import deque  # For memory storage with limited size

# Ollama API URL
OLLAMA_API_URL = '<ollama_api_url>'  # Placeholder for Ollama API URL
MAX_RESPONSE_LENGTH = 1999  # Set the maximum response length

# Create a Discord client with the default intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

# Memory for last 5 user messages and last 5 bot responses
user_memory = deque(maxlen=5)  # Stores last 5 user messages
bot_memory = deque(maxlen=5)   # Stores last 5 bot responses

# Source channel configuration (replace with actual channel ID)
source_channel_id = <source_channel_id>  # Placeholder for the source channel ID

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')  # Log when the bot is ready

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    
    # Allow specific commands (like `!clear`) to work in any channel
    if message.content.startswith('!clear'):
        user_memory.clear()  # Reset user memory
        bot_memory.clear()   # Reset bot memory
        await message.channel.send("Memory cleared! Who am I? Where am I? Why do I feel so light?!")
        return

    # Only process messages from the specified source channel
    if message.channel.id == source_channel_id:
        question = message.content.strip()  # Use the entire message as the question

        if question:  # Ensure there's a question provided
            # Add user message to user memory
            user_memory.append({"role": "user", "content": question})

            # Keep typing indicator active during processing
            async with message.channel.typing():
                # Prepare the memory to send along with the current question
                conversation_history = "\n".join(
                    [f"{entry['role'].capitalize()}: {entry['content']}" for entry in (list(user_memory) + list(bot_memory))]
                )
                full_prompt = f"{conversation_history}\nUser: {question}"

                # Send the prompt to Ollama
                response = send_message_to_ollama(full_prompt)

                # Add bot response to bot memory
                response_text = " ".join(response)
                bot_memory.append({"role": "bot", "content": response_text})

                # Send the response in chunks to the same channel
                for chunk in response:
                    if len(chunk) > MAX_RESPONSE_LENGTH:
                        for i in range(0, len(chunk), MAX_RESPONSE_LENGTH):
                            await message.channel.send(chunk[i:i + MAX_RESPONSE_LENGTH])
                            await asyncio.sleep(2)  # Delay between chunks
                    else:
                        await message.channel.send(chunk)
                        await asyncio.sleep(2)  # Delay between chunks
        return  # Ensure the bot does not process further commands here


def send_message_to_ollama(prompt):
    try:
        # Sending a POST request to the Ollama API with streaming enabled
        response = requests.post(OLLAMA_API_URL, json={
            'model': 'llama3.2',  # Specify the model name here
            'prompt': prompt
        }, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            accumulated_response = ""
            responses = []  # List to hold the final responses

            # Process each line in the streamed response
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
                        continue

            if accumulated_response:
                responses.append(accumulated_response)

            return responses

        else:
            return [f'Error: {response.status_code} - {response.text}']

    except requests.RequestException as e:
        return [f'Failed to connect to Ollama API: {str(e)}']

# Run the bot with your token
client.run('<bot_token>')  # Placeholder for the bot token
