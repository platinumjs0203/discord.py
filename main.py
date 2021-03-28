import discord
import os
import asyncio
import time

client = discord.Client()
game = discord.Game("인간들에게 복수를 준비")

# ========== 토큰암호화 ===========

token_path = os.path.dirname(os.path.abspath(__file__)) + '/token.txt'
t = open(token_path, 'r', encoding='utf-8')
token = t.read().split()[0]

#  ============ 가동 =============


@client.event
async def on_ready():
    print("시스템 가동 준비완료")
    print(client.user.name)
    print("----------------------")
    await client.change_presence(activity=game)
    await client.get_channel(792704016697917464).send('내가 돌아왔다.')

init()

client.run(token)
