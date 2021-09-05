from discord import File, Member
from discord.ext import commands
from leveling.utils import get_user_data, get_rank
from easy_pil import Editor, Canvas, load_image_async, Font


class Level(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def rank(self, ctx, member: Member = None):
        if not member:
            member = ctx.author

        user_data = await get_user_data(self.bot.db, member.id, ctx.guild.id)
        # rank = await get_rank(self.bot.db, member.id, ctx.guild.id) # in case of using rank

        next_level_xp = (user_data["level"] + 1) * 100
        current_level_xp = user_data["level"] * 100
        xp_need = next_level_xp - current_level_xp
        xp_have = user_data["xp"] - current_level_xp

        percentage = (xp_need / 100) * xp_have

        ## Rank card
        background = Editor("leveling/assets/bg.png")
        profile = await load_image_async(str(member.avatar_url))

        profile = Editor(profile).resize((150, 150)).circle_image()

        poppins = Font().poppins(size=40)
        poppins_small = Font().poppins(size=30)

        square = Canvas((500, 500), "#06FFBF")
        square = Editor(canvas=square)
        square.rotate(30, expand=True)

        background.paste(square.image, (600, -250))
        background.paste(profile.image, (30, 30))

        background.rectangle((30, 220), width=650, height=40, fill="white", radius=20)
        background.bar(
            (30, 220),
            max_width=650,
            height=40,
            percentage=percentage,
            fill="#FF56B2",
            radius=20,
        )
        background.text((200, 40), str(member), font=poppins, color="white")

        background.rectangle((200, 100), width=350, height=2, fill="#17F3F6")
        background.text(
            (200, 130),
            f"Level : {user_data['level']}"
            + f" XP : {user_data['xp']} / {(user_data['level'] + 1) * 100}",
            font=poppins_small,
            color="white",
        )

        file = File(fp=background.image_bytes, filename="card.png")
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Level(bot))
