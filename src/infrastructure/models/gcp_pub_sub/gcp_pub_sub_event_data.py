from typing import Generic

from pydantic import BaseModel

from .gcp_pub_sub_message import GcpPubSubMessage, TGcpPubSubMessageData


class GcpPubSubEventData(BaseModel, Generic[TGcpPubSubMessageData]):
    message: GcpPubSubMessage[TGcpPubSubMessageData]
    subscription: str
