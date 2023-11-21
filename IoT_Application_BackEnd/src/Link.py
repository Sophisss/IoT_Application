from pydantic import BaseModel


class BuildingDevice(BaseModel):
    building_id: str
    device_id: str
