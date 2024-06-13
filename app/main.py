import discord
import os
from dotenv import load_dotenv
from server import server_thread

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
client = discord.Client(intents=intents)

@client.event
async def on_ready(self):
    print(f'ログインしました: {self.user}')

@client.event
async def on_message(self, message):
    print(f'送信: {message.author}: {message.content}')
    if message.author == self.user:
        return

    if message.content == '$Hello':
        await message.channel.send('Hello!')

server_thread()
client.run(TOKEN)
