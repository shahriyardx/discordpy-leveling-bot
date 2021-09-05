import asyncpg
from discord.ext import commands
from leveling.config import db_config
from leveling.utils import create_tables, increase_xp


class Leveling(commands.Bot):
    def __init__(self, **options):
        super().__init__(**options)

    async def on_ready(self):
        await self.connect_db()
        await self.load_cogs()

        print("Bot is ready")

    async def load_cogs(self):
        self.load_extension("leveling.cogs.leveling")

    async def connect_db(self):
        self.db = await asyncpg.create_pool(**db_config)
        await create_tables(self.db)

    async def on_message(self, message):
        await self.process_commands(message)

        if message.author.bot:
            return

        await increase_xp(self.db, message)


bot = Leveling(command_prefix="?")
