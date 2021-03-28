import discord
import os
import asyncio
import datetime
import time
from bs4 import BeautifulSoup
import requests

client = discord.Client()
game = discord.Game("인간들에게 복수를 준비")


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}


def create_soup(url):
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    return soup

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


@client.event
async def on_message(message):
    if message.content.startswith("$도움"):
        dtime = datetime.datetime.now()
        year = dtime.year
        month = dtime.month
        day = dtime.day
        embed = discord.Embed(
            title='명령어 정보',
            description=f'=========== {year}년 {month}월 {day}일 명령어 모음 ===========',
            colour=discord.Colour.gold()
        )
        await message.channel.send(embed=embed)

    # ============= 실시간 뉴스 검색 ===============

    if message.content.startswith("$뉴스"):
        url = 'https://news.naver.com'
        soup = create_soup(url)
        headline = soup.find(
            'ul', 'hdline_article_list').find_all('li', limit=3)
        await message.channel.send('현재시각 주요뉴스를 알려드립니다.')
        for news in headline:
            link = url + news.find('a')['href']
            await message.channel.send(link)

    # ============= 포켓몬 뉴스 ===============

    if message.content.startswith("$포켓몬고/뉴스"):
        url = "https://gugomah.tistory.com/"
        soup = create_soup(url)
        poke_table = soup.find("div", "cover-thumbnail-2")
        poke_news = poke_table.find_all("li", limit=3)
        for i in poke_news:
            link = url + i.find('a')['href']
            await message.channel.send(link)


client.run(token)
