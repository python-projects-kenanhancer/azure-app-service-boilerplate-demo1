from abc import ABC, abstractmethod


class ConfigProvider(ABC):
    @abstractmethod
    def get_config(self) -> str | None:
        pass
