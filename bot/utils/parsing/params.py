from typing import NamedTuple, Optional


class Params(NamedTuple):
    """Named tuple to store URL params that necessary for searching."""

    category: str
    exp: str
    city: Optional[str] = None
    remote: Optional[bool] = False
    relocate: Optional[bool] = False
    search: Optional[str] = None
    descr: Optional[bool] = False  # search in jobs descriptions

    def __str__(self) -> str:
        """Returns string representation: URL params."""
        if self.remote:
            prefix = "?remote&"
        elif self.relocate:
            prefix = "?relocate&"
        else:
            prefix = "?"
        return prefix + "&".join(
            f"{key}={value}"
            for key, value in self._asdict().items()
            if value and key not in ("remote", "relocate")
        )
