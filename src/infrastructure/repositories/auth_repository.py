"""Auth repository for authentication operations using Redis."""

import json
import time
import uuid
from typing import Any, Dict, Optional, Tuple

import jwt
import redis
from injector import inject, singleton

from ..logger import LoggerStrategy
from ..models.settings import Settings


@singleton
class AuthRepository:
    """Repository for authentication operations using Redis."""

    @inject
    def __init__(self, logger: LoggerStrategy, settings: Settings, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.logger = logger
        self.settings = settings
        self.jwt_secret = settings.jwt_secret
        self.jwt_algorithm = settings.jwt_algorithm
        self.session_ttl = settings.jwt_expiry_hours * 3600  # Convert hours to seconds

        # Debug logging
        if self.redis_client:
            self.logger.info("AuthRepository: Redis client is available")
            try:
                self.redis_client.ping()
                self.logger.info("AuthRepository: Redis connection test successful")
            except Exception as e:
                self.logger.error(f"AuthRepository: Redis connection test failed: {str(e)}")
        else:
            self.logger.error("AuthRepository: Redis client is None - this should not happen!")

    def create_session(self, user_data: Dict[str, Any], org_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create a new user session in Redis.

        Returns:
            Tuple[bool, Optional[str], Optional[str]]: (success, session_id, jwt_token)
        """
        try:
            if not self.redis_client:
                self.logger.error("Redis client not available for session creation")
                return False, None, None

            # Generate session ID
            session_id = str(uuid.uuid4())

            # Store user context
            user_context_created = self._store_user_context(session_id, user_data)
            if not user_context_created:
                self.logger.error("Failed to store user context in Redis")
                return False, None, None

            # Store organization context
            org_context_created = self._store_org_context(session_id, org_data)
            if not org_context_created:
                self.logger.error("Failed to store organization context in Redis")
                # Clean up user context
                self._remove_user_context(session_id)
                return False, None, None

            # Generate JWT token
            jwt_token = self.generate_jwt_token(session_id, user_data)

            self.logger.info(f"Session created successfully for user: {user_data.get('username', 'unknown')}")
            return True, session_id, jwt_token

        except Exception as e:
            self.logger.error(f"Failed to create session: {str(e)}")
            return False, None, None

    def validate_session(self, session_id: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[Dict[str, Any]]]:
        """
        Validate an existing session and return user/org context.

        Returns:
            Tuple[bool, Optional[Dict], Optional[Dict]]: (valid, user_context, org_context)
        """
        try:
            # Get user context
            user_context = self._get_user_context(session_id)
            if not user_context:
                self.logger.warning(f"No user context found for session: {session_id}")
                return False, None, None

            # Get organization context
            org_context = self._get_org_context(session_id)
            if not org_context:
                self.logger.warning(f"No organization context found for session: {session_id}")
                return False, None, None

            self.logger.info(f"Session validated successfully for user: {user_context.get('username', 'unknown')}")
            return True, user_context, org_context

        except Exception as e:
            self.logger.error(f"Failed to validate session: {str(e)}")
            return False, None, None

    def invalidate_session(self, session_id: str) -> bool:
        """
        Invalidate a session by removing it from Redis.

        Returns:
            bool: True if session was invalidated successfully
        """
        try:
            # Remove user context
            user_removed = self._remove_user_context(session_id)

            # Remove organization context
            org_removed = self._remove_org_context(session_id)

            if user_removed and org_removed:
                self.logger.info(f"Session invalidated successfully: {session_id}")
                return True
            else:
                self.logger.warning(f"Partial session invalidation for: {session_id}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to invalidate session: {str(e)}")
            return False

    def refresh_session(self, session_id: str) -> bool:
        """
        Refresh a session by extending its TTL.

        Returns:
            bool: True if session was refreshed successfully
        """
        try:
            # Check if session exists
            user_context = self._get_user_context(session_id)
            if not user_context:
                self.logger.warning(f"No session found to refresh: {session_id}")
                return False

            # Extend TTL for both user and org context
            user_extended = self._extend_user_context_ttl(session_id)
            org_extended = self._extend_org_context_ttl(session_id)

            if user_extended and org_extended:
                self.logger.info(f"Session refreshed successfully: {session_id}")
                return True
            else:
                self.logger.warning(f"Partial session refresh for: {session_id}")
                return False

        except Exception as e:
            self.logger.error(f"Failed to refresh session: {str(e)}")
            return False

    def _store_user_context(self, session_id: str, user_data: Dict[str, Any]) -> bool:
        """Store user context in Redis."""
        try:
            if not self.redis_client:
                return False
            key = f"user_context:{session_id}"
            self.redis_client.setex(key, self.session_ttl, json.dumps(user_data))
            return True
        except Exception as e:
            self.logger.error(f"Failed to store user context: {str(e)}")
            return False

    def _store_org_context(self, session_id: str, org_data: Dict[str, Any]) -> bool:
        """Store organization context in Redis."""
        try:
            if not self.redis_client:
                return False
            key = f"org_context:{session_id}"
            self.redis_client.setex(key, self.session_ttl, json.dumps(org_data))
            return True
        except Exception as e:
            self.logger.error(f"Failed to store organization context: {str(e)}")
            return False

    def _get_user_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get user context from Redis."""
        try:
            if not self.redis_client:
                return None
            key = f"user_context:{session_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(str(data))
            return None
        except Exception as e:
            self.logger.error(f"Failed to get user context: {str(e)}")
            return None

    def _get_org_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get organization context from Redis."""
        try:
            if not self.redis_client:
                return None
            key = f"org_context:{session_id}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(str(data))
            return None
        except Exception as e:
            self.logger.error(f"Failed to get organization context: {str(e)}")
            return None

    def _remove_user_context(self, session_id: str) -> bool:
        """Remove user context from Redis."""
        try:
            if not self.redis_client:
                return False
            key = f"user_context:{session_id}"
            return bool(self.redis_client.delete(key))
        except Exception as e:
            self.logger.error(f"Failed to remove user context: {str(e)}")
            return False

    def _remove_org_context(self, session_id: str) -> bool:
        """Remove organization context from Redis."""
        try:
            if not self.redis_client:
                return False
            key = f"org_context:{session_id}"
            return bool(self.redis_client.delete(key))
        except Exception as e:
            self.logger.error(f"Failed to remove organization context: {str(e)}")
            return False

    def _extend_user_context_ttl(self, session_id: str) -> bool:
        """Extend TTL for user context."""
        try:
            if not self.redis_client:
                return False
            key = f"user_context:{session_id}"
            return bool(self.redis_client.expire(key, self.session_ttl))
        except Exception as e:
            self.logger.error(f"Failed to extend user context TTL: {str(e)}")
            return False

    def _extend_org_context_ttl(self, session_id: str) -> bool:
        """Extend TTL for organization context."""
        try:
            if not self.redis_client:
                return False
            key = f"org_context:{session_id}"
            return bool(self.redis_client.expire(key, self.session_ttl))
        except Exception as e:
            self.logger.error(f"Failed to extend organization context TTL: {str(e)}")
            return False

    def generate_jwt_token(self, session_id: str, user_data: Dict[str, Any]) -> str:
        """Generate JWT token for the session."""
        try:
            payload = {
                "session_id": session_id,
                "user_id": user_data.get("id"),
                "username": user_data.get("username"),
                "exp": int(time.time()) + self.session_ttl,
                "iat": int(time.time()),
            }
            return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
        except Exception as e:
            self.logger.error(f"Failed to generate JWT token: {str(e)}")
            raise

    def decode_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate JWT token."""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("JWT token has expired")
            return None
        except jwt.InvalidTokenError as e:
            self.logger.warning(f"Invalid JWT token: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to decode JWT token: {str(e)}")
            return None
