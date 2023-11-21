from typing import Optional
from pydantic import Field, BaseModel


class Device(BaseModel):
    device_id: str = Field(min_length=2, max_length=256)
    thingName: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, min_length=2, max_length=256)
    deviceType: str = Field(min_length=2, max_length=100)
    status: str
