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

@client.event
async def on_message_edit(before, after):
    pin_log_channel_id = 1250813996995575868  # ピン留めされたメッセージを送信するチャンネルのIDを指定
    pin_log_channel = client.get_channel(pin_log_channel_id)
    
    if pin_log_channel is None:
        print("Pin log channel not found")
        return
    
    # ピン留めがされたときだけ感知する
    if not before.pinned and after.pinned:
        embed = discord.Embed(
            title="📌 Pinned Message",
            description=after.content,
            color=discord.Color.blue()
        )
        embed.add_field(name="Author", value=after.author.mention)
        embed.add_field(name="Channel", value=after.channel.mention)
        embed.add_field(name="Link", value=f"[Jump to message]({after.jump_url})")
        embed.set_footer(text=f"Message ID: {after.id}")

        await pin_log_channel.send(embed=embed)

server_thread()
client.run(TOKEN)