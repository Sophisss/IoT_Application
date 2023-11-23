from typing import Optional
from pydantic import Field, BaseModel

class BuildingDevice(BaseModel):
    building_id: str = Field(min_length=2, max_length=256)
    device_id: str = Field(min_length=2, max_length=256)
