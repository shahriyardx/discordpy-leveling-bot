from asyncpg import Pool


async def create_tables(pool: Pool):
    async with pool.acquire() as connection:
        # await connection.execute("DROP TABLE IF EXISTS users") # Uncomment this line if you have the database already created and have old data

        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users(
                id BIGSERIAL PRIMARY KEY NOT NULL,
                user_id BIGINT NOT NULL,
                guild_id BIGINT NOT NULL,
                xp BIGINT NOT NULL DEFAULT 5,
                level BIGINT NOT NULL DEFAULT 0
            )
        """
        )


async def create_user(pool: Pool, user_id, guild_id):
    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM users WHERE user_id=$1 AND guild_id=$2", user_id, guild_id
        )
        if record:
            return

        await connection.execute(
            "INSERT INTO users(user_id, guild_id) VALUES($1, $2)", user_id, guild_id
        )


async def increase_xp(pool: Pool, message, rate=5):
    await create_user(pool, message.author.id, message.guild.id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM users WHERE user_id=$1 AND guild_id=$2", message.author.id, message.guild.id
        )
        xp = record["xp"]
        level = record["level"]
        new_level = int((xp + rate) / 100)

        if new_level > level:
            new_level = new_level
        else:
            new_level = level

        await connection.execute(
            "UPDATE users SET xp = $1, level = $2 WHERE user_id = $3 AND guild_id=$4",
            xp + rate,
            new_level,
            message.author.id,
            message.guild.id,
        )


async def get_user_data(pool: Pool, user_id, guild_id):
    await create_user(pool, user_id, guild_id)

    async with pool.acquire() as connection:
        record = await connection.fetchrow(
            "SELECT * FROM users WHERE user_id=$1 AND guild_id=$2", user_id, guild_id
        )
        return dict(record)


async def get_rank(pool: Pool, user_id, guild_id):
    await create_user(pool, user_id, guild_id)

    async with pool.acquire() as connection:
        records = await connection.fetch(
            "SELECT * FROM users WHERE guild_id=$1 ORDER BY xp DESC", guild_id
        )
        rank = 0
        for record in records:
            rank += 1
            if record["user_id"] == user_id:
                break

        return rank
