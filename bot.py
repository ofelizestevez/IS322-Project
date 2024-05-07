import os
import discord
import json
from dotenv import load_dotenv
from main import ChatProcessor
from messages_storage import MessageStorage

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
chat_processor = ChatProcessor()

messages_storage = MessageStorage("messages.json")
print(messages_storage.messages)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    global messages_storage
    
    if message.author == client.user:
        return

    author_id = str(message.author.id)
    # Add the new message to messages_storage
    messages_storage.add_message(author_id, message.content)

    # Process the chat history
    response = chat_processor.process_chat(messages_storage.messages[author_id])

    # Send response to the same channel
    try:
        if response["Chatter"]["response"]:
            await message.channel.send(response["Chatter"]["response"])
    except:
        print("No Chatter Response")

    try:
        if response["Games"]:
            message_to_send = "Here are some games you could like: \n"
            for game in response["Games"][:5]:
                message_to_send += game + "\n"

            if len(response["Searcher"]["genres"]) > 0 or len(response["Searcher"]["tags"]) > 0:
                message_to_send += "this is based on the following genres and tags: \n"

            if len(response["Searcher"]["genres"]) > 0:
                message_to_send += " ".join(response["Searcher"]["genres"]) + "\n"
            if len(response["Searcher"]["tags"]) > 0:
                message_to_send += " ".join(response["Searcher"]["tags"]) + "\n"

            await message.channel.send(message_to_send)
    except:
        print("No Games Response")

    print(response)

client.run(TOKEN)
