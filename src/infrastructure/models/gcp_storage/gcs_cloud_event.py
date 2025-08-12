from cloudevents.http import CloudEvent
from pydantic import BaseModel

from .gcs_event_data import GCSEventData
from .gcs_event_type import GCSEventType


class GCSCloudEvent(BaseModel):
    id: str
    type: GCSEventType  # Using enum instead of Literal
    data: GCSEventData

    @classmethod
    def from_cloud_event(cls, cloud_event: CloudEvent):
        return cls(id=cloud_event["id"], type=cloud_event["type"], data=GCSEventData.model_validate(cloud_event.data))
