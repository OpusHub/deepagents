"""Output types for Copy Creator agent."""

from typing import Optional, Literal
from typing_extensions import TypedDict


class CopyMetadata(TypedDict):
    """Metadata for copy generation."""
    client_name: str
    region: str
    service: str
    total_copies: int
    requested_copies: int


class CopyObject(TypedDict):
    """Individual copy object."""
    id: str
    content: str
    score: Optional[float]


class CopyOutput(TypedDict):
    """Structured output from Copy Creator agent."""
    message: str
    type: Literal["copies", "validation_error", "message"]
    copies: Optional[list[CopyObject]]
    metadata: Optional[CopyMetadata]
