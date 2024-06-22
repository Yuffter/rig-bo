import discord
import os
from dotenv import load_dotenv
from server import server_thread
from discord import app_commands

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    await tree.sync()#スラッシュコマンドを同期

@client.event
async def on_message(message):
    print(f'送信: {message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.content == '$Hello':
        await message.channel.send('Hello!')

# メッセージがピン留めされたときのイベントハンドラ
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    # ピン留めされたメッセージを取得
    pins = await channel.pins()
    # 最新のピン留めされたメッセージを取得
    latest_pin = pins[0]
    # メッセージを転送
    guild = channel.guild
    for chn in guild.channels:
        if chn.name == "ピン留め一覧":
            await chn.send(
                f'#{channel.name} において、メッセージがピン止めされました\n{latest_pin.jump_url}\n{latest_pin.content}'
            )
            break
    """destination_channel = client.get_channel(1250813996995575868)
    await destination_channel.send(
        f'#{channel.name} において、メッセージがピン止めされました\n{latest_pin.jump_url}\n{latest_pin.content}')"""
    
@tree.command(name="test",description="テストコマンドです。")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("てすと！",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」
    
server_thread()
client.run(TOKEN)
