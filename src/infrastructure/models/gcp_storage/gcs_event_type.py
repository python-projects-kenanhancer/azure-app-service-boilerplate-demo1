from enum import Enum


class GCSEventType(str, Enum):
    # Object events
    FINALIZED = "google.cloud.storage.object.v1.finalized"
    DELETED = "google.cloud.storage.object.v1.deleted"
    ARCHIVED = "google.cloud.storage.object.v1.archived"
    METADATA_UPDATED = "google.cloud.storage.object.v1.metadataUpdated"
    CREATED = "google.cloud.storage.object.v1.created"
    UPDATED = "google.cloud.storage.object.v1.updated"

    # Bucket events
    BUCKET_CREATED = "google.cloud.storage.bucket.v1.created"
    BUCKET_DELETED = "google.cloud.storage.bucket.v1.deleted"
    BUCKET_UPDATED = "google.cloud.storage.bucket.v1.updated"

    # IAM events
    IAM_PERMISSION_CREATED = "google.cloud.storage.bucket.v1.iam.permissionCreated"
    IAM_PERMISSION_DELETED = "google.cloud.storage.bucket.v1.iam.permissionDeleted"
    IAM_PERMISSION_UPDATED = "google.cloud.storage.bucket.v1.iam.permissionUpdated"
