import functools
import inspect
from typing import Any, Callable, ParamSpec, Protocol, TypeVar, get_type_hints


class BaseSettings(Protocol):
    pass


# TypeVar for settings classes that implement BaseSettings
TSettings = TypeVar("TSettings", bound=BaseSettings)

# ParamSpec for the decorated function’s signature
P = ParamSpec("P")
# TypeVar for the decorated function’s return
R = TypeVar("R")


def inject_settings(
    loader_func: Callable[..., TSettings],
    param_name: str = "settings",
    **loader_args: Any,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    # ) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    A decorator that:
      - Finds a parameter named `param_name` in the wrapped function's signature,
      - Discovers its annotation to determine the settings type (TSettings),
      - Loads the settings object once (via `loader_func(SettingsClass=..., **loader_args)`),
      - Injects it into `kwargs[param_name]` if not already present.

    Usage:
        @inject_settings(loader_func=my_loader, param_name="my_settings", bucket="...", blob="...")
        def my_func(req, my_settings: MySettings):
            # First call loads MySettings once; subsequent calls reuse it
            ...
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        # 1) Inspect the function signature & type hints
        sig = inspect.signature(func)
        hints = get_type_hints(func, include_extras=True)

        # 2) Find which parameter is named 'settings' (or whichever logic you prefer)
        settings_param = sig.parameters.get(param_name, None)
        if settings_param is None:
            raise TypeError(f"inject_settings could not find a parameter named 'settings' in the function {func.__name__}.")

        # 3) Resolve the annotation for 'settings'
        annotated_type = hints.get(param_name, settings_param.annotation)
        if annotated_type is inspect._empty:
            raise TypeError(f"The 'settings' parameter in {func.__name__} is not annotated with a type.")

        # 4) We'll call loader_func(SettingsClass=<the annotated_type>, **loader_args)
        #    on the first call, then cache the result.
        loaded_settings: TSettings | None = None

        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            nonlocal loaded_settings

            # If 'settings' not in kwargs, inject our loaded one.
            if param_name not in kwargs:
                if loaded_settings is None:
                    # Load once
                    # 5) The loader_func must accept `SettingsClass=<...>` or similar
                    #    Adjust if your loader_func expects a different signature
                    loaded_settings = loader_func(SettingsClass=annotated_type, **loader_args)

                kwargs[param_name] = loaded_settings

            return func(*args, **kwargs)

        return wrapper

    return decorator


__all__ = ["BaseSettings", "TSettings", "inject_settings"]
