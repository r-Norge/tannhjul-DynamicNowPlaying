import os
import discord
from discord.ext import commands
import operator
import asyncio
from .utils.dataIO import fileIO
from .utils import checks

default_settings = {"MsgID": None, "ChannelID": None}
freq = 90


class YeetPlays:
    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/YeetPlays/data.json", "load")
        self.yeet = False

    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_channels=True)
    async def yeetstart(self, ctx):
        """Starts YeetGames"""
        await self.bot.say("The Yeet Machine has started yeeting")
        if self.yeet is False:
            self.yeet = True
            await self.run()


    @commands.command(pass_context=True, no_pm=True)
    @checks.mod_or_permissions(manage_channels=True)
    async def yeetgames(self, ctx):
        """Shows the currently most played games"""
        user = ctx.message.author
        message = ctx.message
        msg = "Generating First Message \n this can take {} seconds.".format(freq)
        first_em = discord.Embed(description=msg, colour=user.colour)
        first_msg = await self.bot.say(embed=first_em)

        if message.id not in self.settings:
            self.settings[first_msg.id] = default_settings
            self.settings[first_msg.id]["MsgID"] = first_msg.id
            self.settings[first_msg.id]["ChannelID"] = first_msg.channel.id
            fileIO("data/YeetPlays/data.json", "save", self.settings)
        if self.yeet is False:
            self.yeet = True
            await self.run()


    async def gamelist(self,message):
        server = message.server
        members = server.members
        color = message.author.color
        freq_list = {}
        for member in members:
            if not member:
                continue
            if not member.game or not member.game.name:
                continue
            if member.bot:
                continue
            if member.game.name not in freq_list:
                freq_list[member.game.name] = 0
            freq_list[member.game.name] += 1

        sorted_list = sorted(freq_list.items(),
                             key=operator.itemgetter(1),
                             reverse=True)

        if not freq_list:
            em = discord.Embed(description="Surprisingly, no one is playing anything.", colour=color)
            em.set_author(name="These are the server's most played games at the moment:")
            return em

        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += "▸ {}: __{}__\n".format(game, freq_list[game])
                #print(game)

            em = discord.Embed(description=msg, colour=color)
            em.set_author(name="These are the server's most played games at the moment:")
            return em

    async def run(self):
        while self.yeet is True:
            f = fileIO("data/YeetPlays/data.json", "load")
            for msg_id in f:
                id = self.settings[msg_id]["MsgID"]
                chan = self.settings[msg_id]["ChannelID"]

                channel = self.bot.get_channel(chan)
                message = await self.bot.get_message(channel, str(id))

                output = await self.gamelist(message)
                await self.bot.edit_message(message=message, embed=output)
            await asyncio.sleep(freq)


def check_folders():
    if not os.path.exists("data/YeetPlays"):
        print("Creating data/YeetPlays folder...")
        os.makedirs("data/YeetPlays")


def check_files():
    f = "data/YeetPlays/data.json"
    if not fileIO(f, "check"):
        print("Creating YeetPlays data.json...")
        fileIO(f, "save", {})
    else: #consistency check
        current = fileIO(f, "load")
        for k,v in current.items():
            if v.keys() != default_settings.keys():
                for key in default_settings.keys():
                    if key not in v.keys():
                        current[k][key] = default_settings[key]
                        print("Adding " + str(key) + " field to YeetPlays data.json")
        fileIO(f, "save", current)



def setup(bot):
    check_folders()
    check_files()
    n = YeetPlays(bot)
    bot.add_cog(n)