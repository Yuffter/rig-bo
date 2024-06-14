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
async def on_ready():
    print(f'ログインしました: {client.user}')

@client.event
async def on_message(message):
    print(f'送信: {message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.content == '$Hello':
        await message.channel.send('Hello!')

# メッセージがピン留めされたときのイベントハンドラ
@client.event
async def on_message_pins_update(channel, last_pin):
    # ピン留めされたメッセージを取得
    pins = await channel.pins()
    # 最新のピン留めされたメッセージを取得
    latest_pin = pins[0]
    # メッセージを転送
    destination_channel = client.get_channel(1250813996995575868)
    await destination_channel.send(f'New pinned message: {latest_pin.content}')
    
server_thread()
client.run(TOKEN)
