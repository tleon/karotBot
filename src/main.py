#! python3
# todo : on selection publish article in news channel
# todo : parse all messages to see if news are missing and post missing ones

import discord
from bot import Bot

client = discord.Client()


def read_env():
    with open("src/.env", "r") as f:
        lines = f.readlines()
        return lines


@client.event
async def on_ready():
    print('Bot is logged in as {0.user}'.format(client))

    activity = discord.Game("Being programmed")
    await client.change_presence(status=discord.Status.online, activity=activity)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if bot.can_handle_last_message():
        await bot.handle_last_message(message)

    if message.content.startswith('!help'):
        await message.channel.send(content=None, embed=bot.get_help())

    if message.content.startswith('!news'):
        bot.last_message = await message.channel.send(content=None, embed=bot.get_news())

    if message.content.startswith('!latest_news'):
        # not working maybe it's the channel id.
        await bot.check_latest_news(client.get_channel(671722922422829096))


if __name__ == '__main__':
    env = read_env()
    token = env[0][6:]
    server_id = env[1][7:]

    bot = Bot('https://gamewave.fr/apex-legends/')

    client.run(token)
