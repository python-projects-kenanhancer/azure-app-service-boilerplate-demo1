import base64
import json
from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel, field_validator

TGcpPubSubMessageData = TypeVar("TGcpPubSubMessageData")


class GcpPubSubMessage(BaseModel, Generic[TGcpPubSubMessageData]):
    data: TGcpPubSubMessageData
    messageId: str | None = None
    publishTime: datetime | None = None
    attributes: dict | None = None
    ordering_key: str | None = None

    @field_validator("data", mode="before")
    @classmethod
    def from_base64(cls, base64_data: str, **kwargs):
        """Create from base64 encoded data"""
        # If input is not a string, return as-is
        if not isinstance(base64_data, str):
            return base64_data

        # If data is empty, return empty string
        if not base64_data:
            return ""

        try:
            # Attempt to decode base64
            decoded: str = base64.b64decode(base64_data).decode("utf-8")

            # Try to parse as JSON
            try:
                return json.loads(decoded)
            except json.JSONDecodeError:
                # If not JSON, return decoded string
                return decoded
        except Exception:
            # If decoding fails, return original value
            return base64_data


__all__ = ["GcpPubSubMessage", "TGcpPubSubMessageData"]
