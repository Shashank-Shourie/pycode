from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Tool:
    """Metadata and implementation for an agent tool."""

    name: str
    function: Callable[..., Any]
    definition: dict

    requires_permission: bool = False
    supports_streaming: bool = False