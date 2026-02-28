from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Chunk:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)


class IngestionStrategy(ABC):
    @abstractmethod
    async def process_file(
        self, filename: str, content: bytes, metadata: dict[str, Any]
    ) -> list[Chunk]: ...

    @abstractmethod
    async def process_text(
        self, text: str, metadata: dict[str, Any]
    ) -> list[Chunk]: ...
