from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import date


@dataclass
class Title:
    de: str
    en: str


@dataclass
class Price:
    student: str
    staff: str
    guest: str


@dataclass
class Meal:
    title: Title
    type: List[str]
    additives: List[str]
    category: str
    price: Price
    dispoId: str
    counter: str
    position: int


@dataclass
class DayMenu:
    date: date
    meals: List[Meal]


@dataclass
class ScheduleResponse:
    id: int
    morningStartTime: str
    morningEndTime: str
    afternoonStartTime: Optional[str]
    afternoonEndTime: Optional[str]
    days: int
