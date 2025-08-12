"""Repositories module for dependency injection."""

from injector import Module, singleton

from ..repositories import AuthRepository, OrganizationRepository, UserRepository


class RepositoriesModule(Module):
    """Module for repositories dependency injection."""

    def configure(self, binder):
        """Configure repository bindings."""
        binder.bind(AuthRepository, to=AuthRepository, scope=singleton)
        binder.bind(UserRepository, to=UserRepository, scope=singleton)
        binder.bind(OrganizationRepository, to=OrganizationRepository, scope=singleton)
