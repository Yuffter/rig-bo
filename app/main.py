import discord
import os
from dotenv import load_dotenv
from server import server_thread
from discord import app_commands
import random

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True  # メンバー情報へのアクセスを許可する
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
    
@tree.command(name="omikuji",description="おみくじが引けます")
async def do_omikuji(interaction: discord.Interaction):
    rnd = random.randint(0,100)
    probability = [1, 16, 5, 7, 35, 6, 29, 1]
    tier = ["大大吉","大吉","中吉","小吉","吉","末吉","凶","大凶"]

    for i in range(len(probability)):
        if rnd < probability[i]:
            guild = interaction.guild
            member = interaction.user
            member_in_guild = guild.get_member(member.id)
            name_in_guild = member_in_guild.display_name
            user_avatar_url = member_in_guild.display_avatar.url  # ユーザーのアバターURLを取得

            embed = discord.Embed(
                title="おみくじの結果",
                description=f"{name_in_guild} の今日の運勢は...\n**{tier[i]}** です",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=user_avatar_url)  # Embedにユーザーのアイコンを設定

            await interaction.response.send_message(embed=embed)
            #await interaction.response.send_message(f"{interaction.user.nick}の今日の運勢は...\n**{tier[i]}** です")
            break
        else:
            rnd -= probability[i]

    
    #await interaction.response.send_message("てすと！",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」
    
server_thread()
client.run(TOKEN)
