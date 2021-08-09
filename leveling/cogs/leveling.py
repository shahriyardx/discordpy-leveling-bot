from discord import File
from discord.ext import commands
from leveling.utils import get_user_data, get_rank
from easy_pil import Editor, Canvas, load_image_async, Font

class Level(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def get_card(self, args):
        pass
    
    @commands.command()
    async def rank(self, ctx):
        user_data = await get_user_data(self.bot.db, ctx.message)
        rank = await get_rank(self.bot.db, ctx.message)

        background = Canvas((934, 282), "#23272a")
        profile = await load_image_async(str(ctx.author.avatar_url_as(format='png')))
        profile = Editor(profile).resize((190, 190)).circle_image()
        editor = Editor(background.image)
        font = Font().poppins(size=30)

        editor.rectangle((20, 20), 894, 242, "#2a2e35")
        editor.paste(profile.image, (50, 50))
        editor.ellipse((42, 42), width=206, height=206, outline="#43b581", stroke_width=10)
        editor.rectangle((260, 180), width=630, height=40, fill="#484b4e", radius=20)
        editor.bar((260, 180), max_width=630, height=40, percentage=30, fill="#00fa81", radius=20)
        editor.text((270, 120), str(ctx.author), font=font, color="#00fa81")
        editor.text((870, 125), f"{user_data['xp']} / {(user_data['level'] + 1) * 100}", font=font, color="#00fa81", anchor="rt")
        editor.text((870, 30), f"Rank {rank}    Level {user_data['level']}", font=font, color="#00fa81", anchor="rt")
        
        file = File(fp=editor.image_bytes, filename="card.png")
        
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Level(bot))