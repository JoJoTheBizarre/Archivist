import uvicorn

# import all modules that register tools, resources, and routes onto `mcp`.
# order matters: server must be imported first.
from archivist.server import mcp  # noqa: F401
import archivist.tools.rag  # noqa: F401
import archivist.resources.collections  # noqa: F401
import archivist.routes.health  # noqa: F401
import archivist.routes.collections  # noqa: F401
import archivist.routes.documents  # noqa: F401

from archivist.config import settings


def main() -> None:
    """start the archivist server with uvicorn."""
    uvicorn.run(
        "archivist.main:mcp",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
