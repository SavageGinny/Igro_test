import asyncio
from psycopg_pool import AsyncConnectionPool
from psycopg.errors import OperationalError
from database.config import settings
from logs.logs_config import logger


class Database:
    def __init__(self):
        self.pool: AsyncConnectionPool | None = None

    async def connect(self) -> None:
        try:
            self.pool = AsyncConnectionPool(
                conninfo=settings.dsn,
                min_size=settings.db_min_pool,
                max_size=settings.db_max_pool,
                timeout=10
            )
            logger.info("Database pool created successfully")

        except OperationalError as e:
            logger.error(f"Database connection failed: {e}")
            raise

        except Exception as e:
            logger.exception(f"Unexpected error during DB connect: {e}")
            raise

    async def disconnect(self) -> None:
        if self.pool:
            await self.pool.close()
            logger.info("Database pool closed")

    async def fetch(self, query: str):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    logger.info(f"Database fetch\n{query}")
                    return await cur.fetchall()

        except asyncio.TimeoutError:
            logger.error("Database query timeout")
            raise

        except Exception as e:
            logger.exception(f"Database fetch error: {e}")
            raise

    async def fetch_one(self, query: str):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    logger.info(f"Database fetch one\n{query}")
                    return await cur.fetchone()

        except asyncio.TimeoutError:
            logger.error("Database query timeout")
            raise

        except Exception as e:
            logger.exception(f"Database fetch one error: {e}")
            raise

    async def execute(self, query: str):
        try:
            async with self.pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(query)
                    await conn.commit()
                    logger.info(f"Database execute\n{query}")

        except asyncio.TimeoutError:
            logger.error("Database execute timeout")
            raise

        except Exception as e:
            logger.exception(f"Database execute error: {e}")
            raise
