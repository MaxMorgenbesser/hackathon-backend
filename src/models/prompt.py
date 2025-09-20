from pydantic import BaseModel


class Prompt(BaseModel):
    id: int
    coupons: bool
    Feedback: bool
    Newsletters: bool
    exclusions: str