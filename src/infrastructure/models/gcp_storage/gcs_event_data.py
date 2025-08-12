from datetime import datetime

from pydantic import BaseModel


class GCSEventData(BaseModel):
    bucket: str
    name: str
    metageneration: str
    timeCreated: datetime
    updated: datetime
