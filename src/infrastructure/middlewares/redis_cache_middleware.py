"""Redis Cache Middleware for managing user and org context in Redis cache."""

import json
from typing import Any, Dict, Optional

from ..decorators.pipeline_decorator import Context, Next
from ..logger.logger_strategies.logger_strategy import LoggerStrategy

# Try to import redis, but handle gracefully if not available
try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

    # Create a dummy class for type checking when redis is not available
    class DummyRedis:
        pass

    redis = DummyRedis


def redis_cache_middleware(context: Context, next: Next, logger: LoggerStrategy):
    """Middleware to handle Redis cache operations for user and org context."""

    if not REDIS_AVAILABLE:
        logger.error("[REDIS_CACHE] Redis package not available")
        return {"error": "Redis service not available", "status": 503}

    logger.info(f"[REDIS_CACHE] Processing {context.func.__name__}")

    # Get session ID from JWT authentication middleware
    session_id = context.kwargs.get("session_id")
    if not session_id:
        logger.warning("[REDIS_CACHE] No session ID found in context")
        return {"error": "Session not authenticated", "status": 401}

    try:
        # Get Redis connection from context or create new one
        redis_client = _get_redis_client(context, logger)
        if not redis_client:
            return {"error": "Redis connection failed", "status": 500}

        # Fetch user and org context from Redis
        user_context = _get_user_context(redis_client, session_id, logger)
        org_context = _get_org_context(redis_client, session_id, logger)

        if not user_context or not org_context:
            logger.warning(f"[REDIS_CACHE] Context not found in Redis for session: {session_id}")
            return {"error": "Session expired or invalid", "status": 401}

        # Add context information to kwargs for downstream middleware
        context.kwargs["redis_client"] = redis_client
        context.kwargs["user_context"] = user_context
        context.kwargs["org_context"] = org_context

        logger.info(f"[REDIS_CACHE] Successfully retrieved context for session: {session_id}")
        logger.info(f"[REDIS_CACHE] User: {user_context.get('username', 'unknown')}")
        logger.info(f"[REDIS_CACHE] Organization: {org_context.get('org_name', 'unknown')}")

        # Continue with the request
        result = next()
        return result

    except Exception as e:
        if REDIS_AVAILABLE and hasattr(e, "__class__") and "Redis" in e.__class__.__name__:
            logger.error(f"[REDIS_CACHE] Redis error: {str(e)}")
            return {"error": "Cache service unavailable", "status": 503}
        else:
            logger.error(f"[REDIS_CACHE] Cache middleware error: {str(e)}")
            return {"error": "Internal server error", "status": 500}


def _get_redis_client(context: Context, logger: LoggerStrategy) -> Optional[Any]:
    """Get Redis client from context or create new one."""
    if not REDIS_AVAILABLE:
        return None

    # Try to get Redis client from context first
    redis_client = context.kwargs.get("redis_client")

    if redis_client and hasattr(redis_client, "ping"):
        try:
            redis_client.ping()
            return redis_client
        except Exception:
            logger.warning("[REDIS_CACHE] Existing Redis client connection failed")

    # Create new Redis client
    try:
        # In production, get these from environment variables or configuration
        if not REDIS_AVAILABLE:
            return None

        redis_client = redis.Redis(  # type: ignore[attr-defined]
            host="localhost",  # Replace with your Redis host
            port=6379,  # Replace with your Redis port
            db=0,  # Replace with your Redis database
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )

        # Test connection
        redis_client.ping()
        logger.info("[REDIS_CACHE] Created new Redis client connection")
        return redis_client

    except Exception as e:
        logger.error(f"[REDIS_CACHE] Failed to create Redis client: {str(e)}")
        return None


def _get_user_context(redis_client: Any, session_id: str, logger: LoggerStrategy) -> Optional[Dict[str, Any]]:
    """Get user context from Redis cache."""
    try:
        user_key = f"user_context:{session_id}"
        user_data = redis_client.get(user_key)

        if not user_data:
            logger.warning(f"[REDIS_CACHE] User context not found for key: {user_key}")
            return None

        user_context = json.loads(user_data)
        logger.debug(f"[REDIS_CACHE] Retrieved user context: {user_context}")
        return user_context

    except json.JSONDecodeError as e:
        logger.error(f"[REDIS_CACHE] Failed to decode user context JSON: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"[REDIS_CACHE] Error retrieving user context: {str(e)}")
        return None


def _get_org_context(redis_client: Any, session_id: str, logger: LoggerStrategy) -> Optional[Dict[str, Any]]:
    """Get organization context from Redis cache."""
    try:
        org_key = f"org_context:{session_id}"
        org_data = redis_client.get(org_key)

        if not org_data:
            logger.warning(f"[REDIS_CACHE] Organization context not found for key: {org_key}")
            return None

        org_context = json.loads(org_data)
        logger.debug(f"[REDIS_CACHE] Retrieved organization context: {org_context}")
        return org_context

    except json.JSONDecodeError as e:
        logger.error(f"[REDIS_CACHE] Failed to decode organization context JSON: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"[REDIS_CACHE] Error retrieving organization context: {str(e)}")
        return None


def create_user_context(
    redis_client: Any, session_id: str, user_data: Dict[str, Any], ttl: int = 3600, logger: Optional[LoggerStrategy] = None
) -> bool:
    """Create user context in Redis cache (utility function for login)."""
    if not REDIS_AVAILABLE or not redis_client:
        return False

    try:
        user_key = f"user_context:{session_id}"
        redis_client.setex(user_key, ttl, json.dumps(user_data))

        if logger:
            logger.info(f"[REDIS_CACHE] Created user context for session: {session_id}")
        return True

    except Exception as e:
        if logger:
            logger.error(f"[REDIS_CACHE] Failed to create user context: {str(e)}")
        return False


def create_org_context(
    redis_client: Any, session_id: str, org_data: Dict[str, Any], ttl: int = 3600, logger: Optional[LoggerStrategy] = None
) -> bool:
    """Create organization context in Redis cache (utility function for login)."""
    if not REDIS_AVAILABLE or not redis_client:
        return False

    try:
        org_key = f"org_context:{session_id}"
        redis_client.setex(org_key, ttl, json.dumps(org_data))

        if logger:
            logger.info(f"[REDIS_CACHE] Created organization context for session: {session_id}")
        return True

    except Exception as e:
        if logger:
            logger.error(f"[REDIS_CACHE] Failed to create organization context: {str(e)}")
        return False


def invalidate_session(redis_client: Any, session_id: str, logger: Optional[LoggerStrategy] = None) -> bool:
    """Invalidate session by removing context from Redis (utility function for logout)."""
    if not REDIS_AVAILABLE or not redis_client:
        return False

    try:
        user_key = f"user_context:{session_id}"
        org_key = f"org_context:{session_id}"

        redis_client.delete(user_key, org_key)

        if logger:
            logger.info(f"[REDIS_CACHE] Invalidated session: {session_id}")
        return True

    except Exception as e:
        if logger:
            logger.error(f"[REDIS_CACHE] Failed to invalidate session: {str(e)}")
        return False
