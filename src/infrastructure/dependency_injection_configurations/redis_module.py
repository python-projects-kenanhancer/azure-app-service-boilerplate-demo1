"""Redis module for dependency injection."""

import redis
from injector import Module, provider, singleton

from ..logger import LoggerStrategy
from ..models.settings import Settings


class RedisModule(Module):
    """Module for Redis client dependency injection."""

    def configure(self, binder):
        """Configure Redis client binding."""
        binder.bind(redis.Redis, to=self.provide_redis_client, scope=singleton)

    @singleton
    @provider
    def provide_redis_client(self, settings: Settings, logger: LoggerStrategy) -> redis.Redis:
        """Provide Redis client instance."""
        try:
            # In a real application, these would come from settings
            redis_host = settings.redis_host
            redis_port = settings.redis_port
            redis_password = settings.redis_password
            redis_db = settings.redis_db

            logger.info(f"Redis client connecting to {redis_host}:{redis_port}")

            # Create Redis client
            redis_client = redis.Redis(
                host=redis_host,
                port=redis_port,
                password=redis_password,
                db=redis_db,
                decode_responses=True,  # Return strings instead of bytes
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
            )

            # Test connection
            redis_client.ping()
            logger.info(f"Redis client connected to {redis_host}:{redis_port}")

            return redis_client

        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            raise Exception(f"Redis connection failed: {str(e)}")
