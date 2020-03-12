import discord
from spider import Spider


class Bot:
    def __init__(self, url):
        self.url = url
        self.last_message = None
        self.news_links = {}

    @staticmethod
    def get_help():
        embed = discord.Embed(title='KarotBot Manual', description='List of commands')
        embed.add_field(name='!help', value="Show the list of command", inline=False)
        embed.add_field(name='!news', value="Display Apex's latest news (in developement)", inline=False)
        embed.add_field(name='!latest_news', value="Post Apex's latest news in the news-apex channel", inline=False)
        embed.add_field(name='!quit', value="Cancel the current command", inline=False)

        return embed

    def get_news(self):
        spider = Spider(self.url)

        to_send = discord.Embed(title="Select a news to display")
        for index, news in enumerate(spider.short_news):
            readable_index = index + 1
            to_send.add_field(
                name='{0}'.format(readable_index),
                value="{0}\n".format(news.a['title']),
                inline=False
            )
            self.news_links[readable_index] = {"article": news, "published": False}

        return to_send

    async def handle_last_message(self, message):
        if not message.content.isdigit():
            await message.delete(delay=2)
            await self.delete_user_and_bot_last_msg(message)
        elif int(message.content) not in list(self.get_news_keys()):
            await message.channel.send('You did not select a valid article to publish.')
        elif message.content == '!quit':
            await self.delete_user_and_bot_last_msg(message)
            await message.channel.send('No article published.')
        else:
            await self.delete_user_and_bot_last_msg(message)
            await message.channel.send('item {0} selected'.format(message.content))

        self.reset_last_message()

    async def delete_user_and_bot_last_msg(self, message):
        await message.delete(delay=2)
        await self.last_message.delete(delay=2)

    def get_news_keys(self):
        return self.news_links.keys()

    def reset_last_message(self):
        self.last_message = None

    def can_handle_last_message(self):
        return self.last_message is not None

    async def check_publication(self, channel):
        messages = await channel.history(limit=50).flatten()
        if not self.news_links:
            self.get_news()
        for message in messages:
            for news in self.news_links:
                links = self.news_links[news]['article'].find_all('a', limit=1)
                for a in links:
                    self.news_links[news]['link'] = self.url[:-14] + a['href']
                    if self.url[:-14] + a['href'] in message.content:
                        self.news_links[news]['published'] = True

    async def check_latest_news(self, channel):
        await self.check_publication(channel)
        for news in self.news_links:
            if not self.news_links[news]['published']:
                await channel.send(self.news_links[news]['link'])
