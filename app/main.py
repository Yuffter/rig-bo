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
    imageUrl = ["https://pbs.twimg.com/media/FlRp3-2aMAAJjQ8.jpg",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimpKtspceL47HWV8CIjCG83OLzaXss2VrjPQt65pfItad0LzQVB13lABAZ8zvViixYeemTkX9O3F2W9vfmDrv2u00nRzGmVD4OIj81oM6zOk84edl8Loj2BvpLIkT4TgWCiPJr4YMSzQZE/s400/omikuji_daikichi.png",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjDPy0X_GAJUV8pauG2Pwpn1dC5O7FfDAJdfDQNxcDB2JpPK85arrtw_qaLKdlvD1YQ9KqkHVrWe_Yfo1hJbYOQNwp8Zb-IZmaISp7_jFDX9pwXINlc7aJtIrlwEAMk6lCkQbweriNT9Lvx/s400/omikuji_chuukichi.png",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhhjqxIjcS2_4hGG8FLlhHSDe1pnMU-XeAXEGWUy10y8Nj-Ohhuchx2ZqxYmPcW2FexxQAdbPyVbJvyCqnAbJ9_DGY7nN3WK0-P0Rz8UlfeouDwdfqgjlx0cBtwXWrTLe7zY8JUGciZcia8/s400/omikuji_syoukichi.png",
                "https://1geki.jp/pachinko/p_hibkoiemakimb/26/",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEglx-IJtiH6CUGvdXF6GAfm_Sh8mbWExuxTjGKhWZbbVk8oiJNWfkXNqSg8v8rreg7cdRN5v8RyMpVPPl_y4GAlCDx0YHia7rtMs5QfOE7qiX8_pdi3xv-9mYanwTjNBOg2WFrEgiIo8RcI/s400/omikuji_suekichi.png",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjYwJAbs5msucqL3TQJEYwCuR7ehewBO-F9HuYH_ERwC9wgzSCHUG3EEUvwF9A281BjEG02Lp8tDY4bKdoTDvr1j-QA78qQXN-DKolTIfj97z2zvFDWC3gJBOHfrdW3hgrXPsMS5yli-Sqo/s400/omikuji_kyou.png",
                "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiM7jD5fZAfHSZ6vk0KH99puqk6oQNcwCgmImN28pHYZey7VxVDIlSnF5ZKxrBx0GVVCyIJXlSRR46S3U3_xMex4LIVAHB_kYJHpJ3RVxjEQLZUEUl6R0B3QidHyZazb-rhwzJxRzI_d6xe/s400/omikuji_daikyou.png"
                ]

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
            embed.set_image(url=imageUrl[i])
            embed.set_thumbnail(url=user_avatar_url)  # Embedにユーザーのアイコンを設定

            await interaction.response.send_message(embed=embed)
            #await interaction.response.send_message(f"{interaction.user.nick}の今日の運勢は...\n**{tier[i]}** です")
            break
        else:
            rnd -= probability[i]

    
    #await interaction.response.send_message("てすと！",ephemeral=True)#ephemeral=True→「これらはあなただけに表示されています」
    
server_thread()
client.run(TOKEN)
