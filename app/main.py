import discord
import os
from dotenv import load_dotenv
from server import server_thread
from discord import app_commands
import random
from datetime import datetime, timedelta

load_dotenv()

TOKEN = os.getenv("TOKEN")
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
intents.guilds = True
intents.members = True  # メンバー情報へのアクセスを許可する
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# ユーザーの最終おみくじ引き日時を記録する辞書
user_omikuji_times = {}

@client.event
async def on_ready():
    print(f'ログインしました: {client.user}')
    await tree.sync()  # スラッシュコマンドを同期

@client.event
async def on_message(message):
    print(f'送信: {message.author}: {message.content}')
    if message.author == client.user:
        return

    if message.content == '$Hello':
        await message.channel.send('Hello!')
    if "社畜" in message.content:
        emoji = client.get_emoji(1258019788047908964)
        if emoji:
            await message.add_reaction(emoji)
        await message.channel.send(f"{message.author.display_name} は社畜です\nもっと頑張って社畜道を極めよう！")

# メッセージがピン留めされたときのイベントハンドラ
@client.event
async def on_guild_channel_pins_update(channel, last_pin):
    # ピン留めされたメッセージを取得
    pins = await channel.pins()
    # 最新のピン留めされたメッセージを取得
    if pins:
        latest_pin = pins[0]
        # メッセージを転送
        guild = channel.guild
        for chn in guild.channels:
            if chn.name == "ピン留め一覧":
                await chn.send(
                    f'@everyone \n<#{channel.id}> において、メッセージがピン止めされました\n{latest_pin.jump_url}\n{latest_pin.content}'
                )
                break

@tree.command(name="omikuji", description="おみくじが引けます")
async def do_omikuji(interaction: discord.Interaction):
    user_id = interaction.user.id
    current_time = datetime.now()

    # 最後におみくじを引いた時間を取得
    last_omikuji_time = user_omikuji_times.get(user_id)
    
    # 最後に引いたのが今日かどうかを確認
    if last_omikuji_time and last_omikuji_time.date() == current_time.date():
        await interaction.response.send_message("今日はもうおみくじを引いたよな？\nそんな甘い考えじゃ、社畜とは言えないな")
        return
    
    # おみくじを引いた時間を更新
    user_omikuji_times[user_id] = current_time
    
    rnd = random.randint(0, 1000)
    probability = [12, 160, 90, 120, 350, 120, 140, 13,5]
    #probability = [0,0,0,0,0,0,0,0,1000]
    tier = ["大大吉", "大吉", "中吉", "小吉", "吉", "末吉", "凶", "大凶","大大凶"]
    imageUrl = [
        "https://pbs.twimg.com/media/FlRp3-2aMAAJjQ8.jpg",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEimpKtspceL47HWV8CIjCG83OLzaXss2VrjPQt65pfItad0LzQVB13lABAZ8zvViixYeemTkX9O3F2W9vfmDrv2u00nRzGmVD4OIj81oM6zOk84edl8Loj2BvpLIkT4TgWCiPJr4YMSzQZE/s400/omikuji_daikichi.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjDPy0X_GAJUV8pauG2Pwpn1dC5O7FfDAJdfDQNxcDB2JpPK85arrtw_qaLKdlvD1YQ9KqkHVrWe_Yfo1hJbYOQNwp8Zb-IZmaISp7_jFDX9pwXINlc7aJtIrlwEAMk6lCkQbweriNT9Lvx/s400/omikuji_chuukichi.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhhjqxIjcS2_4hGG8FLlhHSDe1pnMU-XeAXEGWUy10y8Nj-Ohhuchx2ZqxYmPcW2FexxQAdbPyVbJvyCqnAbJ9_DGY7nN3WK0-P0Rz8UlfeouDwdfqgjlx0cBtwXWrTLe7zY8JUGciZcia8/s400/omikuji_syoukichi.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgablBON0p3T-N_SO2UoPe8MSmCLzGEUlntQIbe1CNzzzapUDo8bky9O4MQqvj_B0wygWh0mgFVlH6WTM-ovapykZUPabAHWT73KfAnViUAaUSBMdEveRAzJRVaAiMbA8ZxyoKCujlj9iqx/s400/omikuji_kichi.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEglx-IJtiH6CUGvdXF6GAfm_Sh8mbWExuxTjGKhWZbbVk8oiJNWfkXNqSg8v8rreg7cdRN5v8RyMpVPPl_y4GAlCDx0YHia7rtMs5QfOE7qiX8_pdi3xv-9mYanwTjNBOg2WFrEgiIo8RcI/s400/omikuji_suekichi.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjYwJAbs5msucqL3TQJEYwCuR7ehewBO-F9HuYH_ERwC9wgzSCHUG3EEUvwF9A281BjEG02Lp8tDY4bKdoTDvr1j-QA78qQXN-DKolTIfj97z2zvFDWC3gJBOHfrdW3hgrXPsMS5yli-Sqo/s400/omikuji_kyou.png",
        "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEiM7jD5fZAfHSZ6vk0KH99puqk6oQNcwCgmImN28pHYZey7VxVDIlSnF5ZKxrBx0GVVCyIJXlSRR46S3U3_xMex4LIVAHB_kYJHpJ3RVxjEQLZUEUl6R0B3QidHyZazb-rhwzJxRzI_d6xe/s400/omikuji_daikyou.png",
        "https://github.com/Yuffter/rig-bo/blob/main/img/%E5%A4%A7%E5%A4%A7%E5%87%B6.png?raw=true"
    ]
    tierText = [
        "君の努力は認められている。来世で。",
        "このまま突き進め。休む暇はない。」",
        "今の努力は実を結ぶ。ただし、ボーナスはカット。",
        "少しずつ進歩。睡眠時間は削れ。",
        "忍耐が鍵。休暇は夢のまた夢。",
        "辛抱強く。昇進はまだまだ先。",
        "困難は続く。社畜魂を忘れるな。",
        "試練の日々。残業代は期待するな。",
        "運命は過酷。働き続けるのみ。"
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
                description="",
                color=discord.Color.blue()
            )
            embed.add_field(name="名前",value=f"{name_in_guild}",inline=False)
            embed.add_field(name="運勢",value=f"{tier[i]}",inline=False)
            embed.add_field(name="一言",value=f"{tierText[i]}",inline=False)
            embed.set_image(url=imageUrl[i])
            embed.set_thumbnail(url=user_avatar_url)  # Embedにユーザーのアイコンを設定

            await interaction.response.send_message(embed=embed)
            break
        else:
            rnd -= probability[i]

server_thread()
client.run(TOKEN)
