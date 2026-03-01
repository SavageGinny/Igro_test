import aiohttp
import aiofiles
import asyncio
import time
import os
import json
from database.db import Database
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

"""
При запуске с сервером установленном на win - убрать комментарий,
так как на винде позволяется только один пул. Не знаю точно - в
PostgreSQL проблема, или в psycopg
"""
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

SQL_INSERT_FILE: str = os.path.join(
    Path(__file__).resolve().parent,
    "sql_scripts",
    "exchange_insert.sql"
)

db: Database = Database()


async def fetch_exchange_rates() -> None:
    """Получение курсов валют"""

    try:
        async with aiohttp.ClientSession() as session:
            url: str = "https://api.currencylayer.com/live"
            params: dict[str, str] = {
                "currencies": "RUB,EUR,CNY,GBP,JPY",
                "access_key": os.getenv('API_TOKEN'),
            }

            async with session.get(url, params=params) as response:
                data: dict = await response.json()

        conditions: dict[str, float] = {
            "USD": round(float(data['quotes']['USDRUB']), 2),
            "EUR": round(1 / float(data['quotes']['USDEUR']) * data['quotes']['USDRUB'], 2),
            "CNY": round(1 / float(data['quotes']['USDCNY']) * data['quotes']['USDRUB'], 2),
            "GBP": round(1 / float(data['quotes']['USDGBP']) * data['quotes']['USDRUB'], 2),
            "JPY": round(1 / float(data['quotes']['USDJPY']) * data['quotes']['USDRUB'], 2),
        }

        print(f"Курсы валют: {conditions}")

        async with aiofiles.open(SQL_INSERT_FILE, "r", encoding="utf-8") as conf_file:
            sql_template: str = await conf_file.read()

        sql_query: str = sql_template.format(**conditions)

        await db.execute(sql_query)
        print("Данные успешно сохранены в БД")

    except aiohttp.ClientError as e:
        print(f"Ошибка HTTP запроса: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        raise


async def main() -> None:
    """Главная функция с циклом"""
    timer: int = int(input("Введите временной промежуток паузы в минутах: "))
    print(f"Запуск с интервалом {timer} минут")

    await db.connect()

    try:
        while True:
            print(f"\n{'=' * 50}")
            print(f"Запуск задачи в {time.strftime('%H:%M:%S')}")
            await fetch_exchange_rates()
            print(f"Следующий запуск через {timer} минут")
            await asyncio.sleep(60 * timer)
    except KeyboardInterrupt:
        print("\nОстановка по запросу пользователя")
    finally:
        await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
