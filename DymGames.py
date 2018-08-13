import discord
from discord.ext import commands
import operator
import asyncio


class WhoPlaysDyn:
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True, no_pm=True)
    async def dyngames(self, ctx):
        """Shows the currently most played games"""
        user = ctx.message.author
        server = ctx.message.server
        members = server.members
        first_em = discord.Embed(description="Generating First Message", colour=user.colour)
        first_msg = await self.bot.say(embed=first_em)
        msg_id = first_msg.id
        msg_chan = first_msg.channel.id
        msg_serv = first_msg.server.id
        msg_str = "{}.{}".format(msg_chan, msg_id)
        #print(msg_str)


        while True:
            output = await self.gamelist(ctx)
            await self.bot.edit_message(message=first_msg, embed=output)
            #print("Hei")
            await asyncio.sleep(30)

    async def gamelist(self, ctx):
        user = ctx.message.author
        server = ctx.message.server
        members = server.members
        #print("Yall gay")
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
            em = discord.Embed(description="Surprisingly, no one is playing anything.", colour=user.colour)
            em.set_author(name="These are the server's most played games at the moment:")
            #print("yote")


            return em
        else:
            # create display
            msg = ""
            max_games = min(len(sorted_list), 10)
            for i in range(max_games):
                game, freq = sorted_list[i]
                msg += "▸ {}: __{}__\n".format(game, freq_list[game])
                #print(game)

            em = discord.Embed(description=msg, colour=user.colour)
            em.set_author(name="These are the server's most played games at the moment:")
            return em

def setup(bot):
    n = WhoPlaysDyn(bot)
    bot.add_cog(n)