from prisma import Prisma

additives = [
    {"code": "1", "description": "mit Antioxidationsmittel"},
    {"code": "2", "description": "mit Konservierungsstoffen"},
    {"code": "3", "description": "geschwefelt"},
    {"code": "4", "description": "mit Farbstoff"},
    {"code": "5", "description": "gewachst"},
    {"code": "6", "description": "mit Geschmacksverstärker"},
    {"code": "7", "description": "mit Süßungsmitteln"},
    {"code": "8", "description": "enth. eine Phenylalaninquelle"},
    {"code": "9", "description": "mit Phosphat"},
    {"code": "10", "description": "geschwärzt"},
    {"code": "11", "description": "mit Alkohol"},
    {"code": "20a", "description": "Gluten aus Weizen & Erzeugnisse"},
    {"code": "20b", "description": "Gluten aus Roggen & Erzeugnisse"},
    {"code": "20c", "description": "Gluten aus Gerste & Erzeugnisse"},
    {"code": "20d", "description": "Gluten aus Hafer & Erzeugnisse"},
    {"code": "20e", "description": "Gluten aus Dinkel & Erzeugnisse"},
    {"code": "20f", "description": "Gluten aus Kamut & Erzeugnisse"},
    {"code": "21", "description": "Krebstiere & Erzeugnisse"},
    {"code": "22", "description": "Eier & Erzeugnisse"},
    {"code": "23", "description": "Fisch & Erzeugnisse"},
    {"code": "24", "description": "Erdnüsse & Erzeugnisse"},
    {"code": "25", "description": "Soja & Erzeugnisse"},
    {"code": "26", "description": "Milch & Erzeugnisse"},
    {"code": "27a", "description": "Mandeln & Erzeugnisse"},
    {"code": "27b", "description": "Haselnüsse & Erzeugnisse"},
    {"code": "27c", "description": "Walnüsse & Erzeugnisse"},
    {"code": "27d", "description": "Kaschunüsse & Erzeugnisse"},
    {"code": "27e", "description": "Pekannüsse & Erzeugnisse"},
    {"code": "27f", "description": "Paranüsse & Erzeugnisse"},
    {"code": "27g", "description": "Pistazien & Erzeugnisse"},
    {"code": "28", "description": "Sellerie & Erzeugnisse"},
    {"code": "29", "description": "Senf & Erzeugnisse"},
    {"code": "30", "description": "Sesamsamen & Erzeugnisse"},
    {"code": "31", "description": "Schwefeldioxid/Sulfite > 10mg/kg"},
    {"code": "32", "description": "Lupine & Erzeugnisse"},
    {"code": "33", "description": "Weichtiere & Erzeugnisse"},
]

types = [
    {
        "code": "V",
        "description": "Ohne Fleisch",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-vegetarisch.png",
    },
    {
        "code": "G",
        "description": "Mit Geflügel",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-gefluegel.png",
    },
    {
        "code": "N",
        "description": "Vegane Speisen",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-vegan.png",
    },
    {
        "code": "F",
        "description": "Mit Fisch bzw. Meeresfrüchten",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-fisch.png",
    },
    {
        "code": "S",
        "description": "Mit Schweinefleisch",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-schwein.png",
    },
    {
        "code": "R",
        "description": "Mit Rindfleisch",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-rind.png",
    },
    {
        "code": "A",
        "description": "Fleisch aus artgerechter Haltung",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-artgerechte-haltung.png",
    },
    {
        "code": "B",
        "description": "Bio",
        "icon": "https://www.stwdo.de/typo3conf/ext/pa_mensa/Resources/Public/Images/Supplies/icon-bio.png",
    },
]

canteens = [
    {"name": "Hauptmensa", "remoteId": "341"},
    {"name": "Mensa Süd", "remoteId": "342"},
    {"name": "Archeteria", "remoteId": "452"},
    {"name": "Mensa Max Ophuels Platz", "remoteId": "453"},
    {"name": "Mensa Sonnenstraße", "remoteId": "455"},
    {"name": "kostBar", "remoteId": "456"},
    {"name": "food fakultät", "remoteId": "474"},
    {"name": "Galerie", "remoteId": "451"},
]

counters = [
    {
        "name": "Menü 1",
    },
    {
        "name": "Aktionsteller",
    },
    {
        "name": "Menü 2",
    },
    {
        "name": "Tagesgericht",
    },
    {
        "name": "Vegetarisches Menü",
    },
    {
        "name": "Beilagen",
    },
]


async def set_canteens():
    prisma = Prisma()
    await prisma.connect()

    for canteen in canteens:
        try:
            await prisma.canteen.create(data=canteen)
        except Exception as e:
            continue

    await prisma.disconnect()


async def set_additives():
    prisma = Prisma()
    await prisma.connect()

    try:
        for additive in additives:
            await prisma.additive.create(data=additive)
    except Exception as e:
        pass

    await prisma.disconnect()


async def set_types():
    prisma = Prisma()
    await prisma.connect()

    for type_entry in types:
        try:
            await prisma.type.create(data=type_entry)
        except Exception as e:
            continue

    await prisma.disconnect()


async def set_counters():
    prisma = Prisma()
    await prisma.connect()

    for counter in counters:
        try:
            await prisma.counter.create(data=counter)
        except Exception as e:
            continue

    await prisma.disconnect()


async def run_all():
    await set_canteens()
    await set_additives()
    await set_types()
    await set_counters()


if __name__ == "__main__":
    import asyncio

    asyncio.run(run_all())
