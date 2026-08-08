from core.logging import get_logger
from database.providers import Provider

log = get_logger()


class ProviderRegistry:
    """Allows attribute-style access to providers by name."""

    def __init__(self, providers: list[Provider]):
        self._providers: dict[str, Provider] = {
            p.name: p for p in providers
        }


    def __getattr__(self, name: str) -> Provider:
        try:
            return self._providers[name]
        except KeyError:
            raise AttributeError(f"No provider names '{name}'...")


    def __getitem__(self, name: str) -> Provider:
        return self._providers[name]


    def __contains__(self, name) -> bool:
        return name in self._providers


    def __iter__(self):
        return iter(self._providers.values())


    @property
    def names(self) -> list[str]:
        """Returns a list of all Provider names."""
        return list(self._providers.keys())


    def __repr__(self):
        return f"ProviderRegistry({list(self._providers.keys())})"