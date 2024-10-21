import discord
import requests
import json  # Import the json module from the standard library
import asyncio  # Import asyncio to use sleep for typing simulation

# Ollama API URL
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
MAX_RESPONSE_LENGTH = 1999  # Set the maximum response length

# Create a Discord client with the default intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}!')  # Log when the bot is ready

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages sent by the bot itself

    if message.content.startswith('!bot'):  # Check if the message starts with "!bot"
        question = message.content[5:].strip()  # Extract the question after "!bot"
        
        if question:  # Ensure there's a question provided
            # Simulate typing for 1 second (you can adjust the duration)
            async with message.channel.typing():
                await asyncio.sleep(1)  # Optional delay to simulate typing
                
                response = send_message_to_ollama(question)
                
                # Send the Ollama API response in chunks with a delay between each chunk
                for chunk in response:
                    if len(chunk) > MAX_RESPONSE_LENGTH:
                        # If a single response chunk exceeds the limit, split it
                        for i in range(0, len(chunk), MAX_RESPONSE_LENGTH):
                            await message.channel.send(chunk[i:i + MAX_RESPONSE_LENGTH])
                            await asyncio.sleep(2)  # Delay between each chunk
                    else:
                        await message.channel.send(chunk)  # Send the chunk
                        await asyncio.sleep(2)  # Delay between each chunk
        else:
            await message.channel.send("Please provide a question after `!bot`.")

def send_message_to_ollama(prompt):
    try:
        # Sending a POST request to the Ollama API with streaming enabled
        response = requests.post(OLLAMA_API_URL, json={
            'model': 'llama3.2',  # Specify the model name here
            'prompt': prompt
        }, stream=True)

        # Check if the request was successful
        if response.status_code == 200:
            # To store the accumulated response
            accumulated_response = ""
            responses = []  # List to hold the final responses

            # Process each line in the streamed response
            for line in response.iter_lines():
                if line:
                    try:
                        # Decode the line from bytes to string and parse it as JSON
                        line_data = line.decode('utf-8')
                        json_data = json.loads(line_data)

                        # Extract the 'response' field
                        new_response = json_data.get('response', '')

                        # Check if adding new response would exceed the max length
                        if len(accumulated_response) + len(new_response) > MAX_RESPONSE_LENGTH:
                            # Add the current accumulated response to the list
                            responses.append(accumulated_response)
                            # Reset accumulated_response and add the new response
                            accumulated_response = new_response
                            
                            # If accumulated_response still exceeds limit, slice it
                            while len(accumulated_response) > MAX_RESPONSE_LENGTH:
                                responses.append(accumulated_response[:MAX_RESPONSE_LENGTH])
                                accumulated_response = accumulated_response[MAX_RESPONSE_LENGTH:]

                        else:
                            accumulated_response += new_response
                    except ValueError:
                        # If parsing fails, skip the line
                        continue

            # Append any remaining accumulated response to the list
            if accumulated_response:
                responses.append(accumulated_response)

            return responses  # Return the list of responses

        else:
            return [f'Error: {response.status_code} - {response.text}']

    except requests.RequestException as e:
        return [f'Failed to connect to Ollama API: {str(e)}']

# Run the bot with your token
client.run('<your bot token>')
