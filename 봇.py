import discord
import asyncio
import os
from discord.ext import commands
import urllib
from urllib.request import URLError
from urllib.request import HTTPError
from urllib.request import urlopen
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from urllib.parse import quote
import re # Regex for youtube link
import warnings
import requests
import time

token = 'ODAyOTExMjA3MjAzMDEyNjA4.YA2HVQ.4E-YQLGuAeeL0DqUxddWCIl727Q'

client = discord.Client() # Create Instance of Client. This Client is discord server's connection to Discord Room
def deleteTags(htmls):
    for a in range(len(htmls)):
        htmls[a] = re.sub('<.+?>','',str(htmls[a]),0).strip()
    return htmls

@client.event # Use these decorator to register an event.
async def on_ready(): # on_ready() event : when the bot has finised logging in and setting things up
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Type !help or !도움말 for help"))
    print("New log in as {0.user}".format(client))

@client.event
async def on_message(message): # on_message() event : when the bot has recieved a message
    #To user who sent message
    # await message.author.send(msg)
    print(message.content)
    if message.author == client.user:
        return
        
    if message.content.startswith('!메이플'):

        # Maplestroy base link
        mapleLink = "https://maplestory.nexon.com"
        # Maplestory character search base link
        mapleCharacterSearch = "https://maplestory.nexon.com/Ranking/World/Total?c="
        mapleUnionLevelSearch = "https://maplestory.nexon.com/Ranking/Union?c="


        playerNickname = ''.join((message.content).split(' ')[1:])
        html = urlopen(mapleCharacterSearch + quote(playerNickname))  # Use quote() to prevent ascii error
        bs = BeautifulSoup(html, 'html.parser')

        html2 = urlopen(mapleUnionLevelSearch + quote(playerNickname))
        bs2 = BeautifulSoup(html2,'html.parser')

        if len(message.content.split(" ")) == 1:
            embed = discord.Embed(title="닉네임이 입력되지 않았잉...", description="", color=0x5CD1E5)
            embed.add_field(name="Player nickname not entered",
                            value="To use command !메이플 : !메이플 (Nickname)", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Incorrect command usage ", embed=embed)

        elif bs.find('tr', {'class': 'search_com_chk'}) == None:
            embed = discord.Embed(title="Nickname not exist", description="", color=0x5CD1E5)
            embed.add_field(name="해당 닉네임의 유저가 존재하지 않는다잉...", value="유저의 이름을 확인해줘라잉...", inline=False)
            embed.set_footer(text='Service provided by Hoplin.',
                             icon_url='https://avatars2.githubusercontent.com/u/45956041?s=460&u=1caf3b112111cbd9849a2b95a88c3a8f3a15ecfa&v=4')
            await message.channel.send("Error : Non existing Summoner ", embed=embed)

        else:
            # Get to the character info page
            characterRankingLink = bs.find('tr', {'class': 'search_com_chk'}).find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*')})['href']
            #Parse Union Level
            characterUnionRanking = bs2.find('tr', {'class': 'search_com_chk'})
            if characterUnionRanking == None:
                pass
            else:
                characterUnionRanking = characterUnionRanking.findAll('td')[2].text
            html = urlopen(mapleLink + characterRankingLink)
            bs = BeautifulSoup(html, 'html.parser')

            # Find Ranking page and parse page
            personalRankingPageURL = bs.find('a', {'href': re.compile('\/Common\/Character\/Detail\/[A-Za-z0-9%?=]*\/Ranking\?p\=[A-Za-z0-9%?=]*')})['href']
            html = urlopen(mapleLink + personalRankingPageURL)
            bs = BeautifulSoup(html, 'html.parser')
            #Popularity

            popularityInfo = bs.find('span',{'class' : 'pop_data'}).text.strip()
            ''' Can't Embed Character's image. Gonna fix it after patch note
            #Character image
            getCharacterImage = bs.find('img',{'src': re.compile('https\:\/\/avatar\.maplestory\.nexon\.com\/Character\/[A-Za-z0-9%?=/]*')})['src']
            '''
            infoList = []
            # All Ranking information embeded in <dd> elements
            RankingInformation = bs.findAll('dd')  # [level,job,servericon,servername,'-',comprehensiveRanking,'-',WorldRanking,'-',JobRanking,'-',Popularity Ranking,'-',Maple Union Ranking,'-',Achivement Ranking]
            for inf in RankingInformation:
                infoList.append(inf.text)
            embed = discord.Embed(title="유저: " + playerNickname + " 의 정보다잉...", description=infoList[0] + " | " +infoList[1] + " | " + "서버 : " + infoList[2], color=0x5CD1E5)
            embed.add_field(name="전체 순위",value=infoList[4], inline=True)
            embed.add_field(name="월드 순위", value=infoList[6], inline=True)
            embed.add_field(name="직업 순위", value=infoList[8], inline=True)
            embed.add_field(name="인기도 순위", value=infoList[10] + "( " +popularityInfo + " )", inline=True)
            if characterUnionRanking == None:
                embed.add_field(name="유니온 순위", value=infoList[12],inline=True)
            else:
                embed.add_field(name="유니온", value=infoList[12] + "( 레벨:" + characterUnionRanking + " )", inline=True)
            embed.add_field(name="업적 순위", value=infoList[14], inline=True)
            await message.channel.send("유저: " + playerNickname +" 의 정보다잉...", embed=embed)
client.run('ODAyOTExMjA3MjAzMDEyNjA4.YA2HVQ.4E-YQLGuAeeL0DqUxddWCIl727Q')