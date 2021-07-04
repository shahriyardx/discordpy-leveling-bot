from discord.ext import commands
from leveling.utils import get_user_data, get_rank
from disrank.generator import Generator
import functools
import asyncio
import discord

class Level(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def get_card(self, args):
        image = Generator().generate_profile(**args)
        return image
    
    @commands.command()
    async def rank(self, ctx):
        user_data = await get_user_data(self.bot.db, ctx.message)
        rank = await get_rank(self.bot.db, ctx.message)

        args = {
			'bg_image' : 'https://mcdn.wallpapersafari.com/medium/74/90/fsUChQ.jpg', # Background image link (Optional)
			'profile_image' : str(ctx.author.avatar_url_as(format='png')), # User profile picture link
			'level' : user_data['level'], # User current level 
			'current_xp' : user_data['level'] * 100, # Current level minimum xp
			'user_xp' : user_data['xp'], # User current xp
			'next_xp' : (user_data['level'] + 1) * 100, # xp required for next level
			'user_position' : rank, # User position in leaderboard
			'user_name' : str(ctx.author), # user name with descriminator 
			'user_status' : ctx.author.status.name, # User status eg. online, offline, idle, streaming, dnd
		}

        func = functools.partial(self.get_card, args)
        image = await asyncio.get_event_loop().run_in_executor(None, func)

        file = discord.File(fp=image, filename='image.png')
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Level(bot))