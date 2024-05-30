import asyncio
from datetime import date, datetime
from prisma import Prisma
from prisma.models import Canteen
from requests import request
from api_response import DayMenu
from typing import List
import re
import json
from base_data import additives, types, counters, run_all


async def get_day_by_date(prisma: Prisma, date: date):
    day = await prisma.day.find_unique(
        where={"date": datetime.combine(date, datetime.min.time())}
    )

    return day


async def create_day(prisma: Prisma, date: date):
    day = await prisma.day.create(
        data={"date": datetime.combine(date, datetime.min.time())}
    )

    return day


async def get_menu_item_by_title_date_canteen(
    prisma: Prisma, title: str, dayId: int, canteen: Canteen
):
    menu_item = await prisma.menuitem.find_first(
        where={
            "title": {
                "is": {
                    "de": title,
                }
            },
            "day": {"is": {"id": dayId}},
            "canteen": {"is": {"remoteId": canteen.remoteId}},
        }
    )

    return menu_item


async def get_title(prsima: Prisma, titleDe: str):
    title = await prsima.title.find_unique(where={"de": titleDe})
    return title


def filter_additives(_additives: List[str]) -> List[str]:
    valid_codes = {type_item["code"]: type_item for type_item in additives}

    return [code for code in _additives if code in valid_codes]


def filter_types(_types: List[str]) -> List[str]:
    valid_codes = {type_item["code"]: type_item for type_item in types}

    return [code for code in _types if code in valid_codes]


def filter_counter(_counter: str) -> str | None:
    valid_codes = {type_item["name"]: type_item for type_item in counters}

    return _counter if _counter in valid_codes else None


async def fetch_data():
    # Set the database connection
    prisma = Prisma()
    await prisma.connect()

    # Get all canteens
    canteens = await prisma.canteen.find_many()

    for canteen in canteens:
        menu_data = await fetch_menu(canteen)

        if menu_data is None:
            continue

        for day in menu_data:
            # Check if the day is in the current calender week and skip saturday and sunday
            if (
                day.date.isocalendar()[1] != datetime.now().isocalendar()[1]
                or day.date.weekday() > 4
            ):
                continue

            # Check if the day exists already
            db_day = await get_day_by_date(prisma, day.date)

            if db_day is None:
                db_day = await create_day(prisma, day.date)

            for item in day.meals:
                # Check if the menu item for this day exists already
                db_menu_item = await get_menu_item_by_title_date_canteen(
                    prisma, item["title"]["de"], db_day.id, canteen
                )

                # Skip if its in the database already
                if db_menu_item is not None:
                    continue

                # Check if the title exists already
                db_title = await get_title(prisma, item["title"]["de"])

                new_menu_item_data = {
                    "title": (
                        {
                            "create": {
                                "de": item["title"]["de"],
                                "en": item["title"]["en"],
                                "parsedDe": parse_menu_item_name(item["title"]["de"]),
                                "parsedEn": parse_menu_item_name(item["title"]["en"]),
                            }
                        }
                        if not db_title
                        else {"connect": {"id": db_title.id}}
                    ),
                    "type": {
                        "connect": [{"code": t} for t in filter_types(item["type"])]
                    },
                    "additives": {
                        "connect": [
                            {"code": a} for a in filter_additives(item["additives"])
                        ]
                    },
                    "category": item["category"],
                    "price": {
                        "create": {
                            "student": convert_price_to_cents(item["price"]["student"]),
                            "staff": convert_price_to_cents(item["price"]["staff"]),
                            "guest": convert_price_to_cents(item["price"]["guest"]),
                        }
                    },
                    "dispoId": item["dispoId"],
                    "position": item["position"],
                    "day": {"connect": {"id": db_day.id}},
                    "canteen": {"connect": {"remoteId": canteen.remoteId}},
                }

                if "counter" in item:
                    new_menu_item_data["counter"] = {
                        "connect": {"name": filter_counter(item["counter"])}
                    }

                new_menu_item = await prisma.menuitem.create(data=new_menu_item_data)


def parse_menu_item_name(name: str) -> str:
    # Remove content within parentheses and trailing |
    parsed_name = re.sub(r"\([^)]*\)", "", name).strip().rstrip("|")
    return parsed_name


def convert_price_to_cents(price: str) -> int:
    # Remove all non-numeric characters
    return int(re.sub(r"\D", "", price))


async def fetch_menu(canteen: Canteen) -> List[DayMenu] | None:
    fetch_url = f"https://mobil.itmc.tu-dortmund.de/canteen-menu/v3/canteens/{canteen.remoteId}/?expand=true"

    response = request("get", fetch_url)

    if not response.ok and response.status_code != 200:
        return None

    j = json.loads(response.text)

    # Preprocess the JSON response
    day_menus = []
    for date, menu in j.items():
        day_menus.append(
            DayMenu(date=datetime.strptime(date, "%Y-%m-%d").date(), meals=menu)
        )

    return day_menus


# schedule.every().day.at("07:00").do(fetch_data)


async def main():
    # Run this function once a day
    # while True:
    #     schedule.run_pending()
    await run_all()
    await fetch_data()


if __name__ == "__main__":
    asyncio.run(main())
