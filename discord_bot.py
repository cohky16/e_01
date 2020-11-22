import discord
from dotenv import load_dotenv
import os
import requests
import datetime

# 環境変数取得
load_dotenv()
token = os.environ['DISCORD_TOKEN']

class MyClient(discord.Client):
    async def on_ready(self):
        # 起動確認
        print('Logged on as', self.user)

    async def on_message(self, message):
        # 送信者確認
        if message.author == self.user:
            return

        if message.content.startswith('/covid'):
            # URLからjson取得
            country = message.content.split()[1]
            url = 'https://covidapi.info/api/v1/country/' + country + '/latest'
            json = requests.get(url).json()

            # jsonを加工
            try:
                yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
                d_yesterday = yesterday.strftime('%Y-%m-%d')
                needJson = json['result'][d_yesterday]
                confirmed = str(needJson['confirmed'])
                deaths = str(needJson['deaths'])
                recovered = str(needJson['recovered'])
                await message.channel.send('[' + d_yesterday + '] ' + 'confirmed: ' + confirmed + ' | ' + 'deaths: ' + deaths + ' | ' + 'recovered: ' + recovered)
            except KeyError:
                await message.channel.send('[' + d_yesterday + '] ' +'未取得')

client = MyClient()
client.run(token)