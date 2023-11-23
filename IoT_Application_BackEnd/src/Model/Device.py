from typing import Optional
from pydantic import Field, BaseModel


class Device(BaseModel):
    device_id: str = Field(min_length=2, max_length=256)
    thingName: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(default=None)
    deviceType: str = Field(min_length=2, max_length=256)
    status: str = Field()
