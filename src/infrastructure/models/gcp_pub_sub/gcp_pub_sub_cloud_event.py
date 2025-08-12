from datetime import datetime
from typing import Generic

from cloudevents.http import CloudEvent
from pydantic import BaseModel

from .gcp_pub_sub_event_data import GcpPubSubEventData
from .gcp_pub_sub_event_type import GcpPubSubEventType
from .gcp_pub_sub_message import GcpPubSubMessage, TGcpPubSubMessageData


class GcpPubSubCloudEvent(BaseModel, Generic[TGcpPubSubMessageData]):
    specversion: str | None = None
    id: str
    source: str
    type: GcpPubSubEventType
    data: GcpPubSubEventData[TGcpPubSubMessageData]
    time: datetime | None = None
    datacontenttype: str | None = None
    subject: str | None = None

    @classmethod
    def from_cloud_event(cls, cloud_event: CloudEvent):
        message_data = cloud_event.data.get("message", {})

        message = GcpPubSubMessage.model_validate(message_data)

        # Create structured data
        event_data = GcpPubSubEventData(
            message=message,
            subscription=cloud_event.data.get("subscription", ""),
        )

        return cls(
            specversion=cloud_event.get("specversion"),
            id=cloud_event["id"],
            source=cloud_event["source"],
            type=cloud_event["type"],
            time=cloud_event.get("time"),
            datacontenttype=cloud_event.get("datacontenttype"),
            subject=cloud_event.get("subject"),
            data=event_data,
        )
