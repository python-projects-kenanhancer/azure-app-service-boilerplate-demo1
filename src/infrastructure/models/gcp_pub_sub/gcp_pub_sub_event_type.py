from enum import Enum


class GcpPubSubEventType(str, Enum):
    # Topic events
    MESSAGE_PUBLISHED = "google.cloud.pubsub.topic.v1.messagePublished"

    # Subscription events
    MESSAGE_ACKNOWLEDGED = "google.cloud.pubsub.subscription.v1.acknowledged"
    DEAD_LETTER = "google.cloud.pubsub.subscription.v1.deadLettered"
    MESSAGE_DELIVERED = "google.cloud.pubsub.subscription.v1.delivered"

    # Schema events
    SCHEMA_CREATED = "google.cloud.pubsub.schema.v1.created"
    SCHEMA_UPDATED = "google.cloud.pubsub.schema.v1.updated"
    SCHEMA_DELETED = "google.cloud.pubsub.schema.v1.deleted"
