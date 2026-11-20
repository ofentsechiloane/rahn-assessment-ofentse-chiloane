from typing import Literal

from pydantic import BaseModel


class Details(BaseModel):
    packages: list[Literal["single", "five", "twelve"]]
    asks_saturday: bool
    unknown_topics: list[str]


class Enquiry(BaseModel):
    intent: Literal["pricing", "availability", "pricing_and_availability", "other"]
    details: Details
    requires_human_approval: bool
