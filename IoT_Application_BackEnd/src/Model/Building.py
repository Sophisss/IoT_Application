from typing import Optional
from pydantic import Field, BaseModel


class Building(BaseModel):
    building_id: str = Field(min_length=2, max_length=256)
    location: Optional[str] = Field(default=None)
    floors: int = Field(gt=1, lt=100)
