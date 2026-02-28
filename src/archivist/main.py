import uvicorn

from archivist.server import mcp
import archivist.tools.rag  # noqa: F401
import archivist.tools.memory  # noqa: F401
import archivist.resources.memory  # noqa: F401
import archivist.resources.search  # noqa: F401
import archivist.resources.server  # noqa: F401
import archivist.routes.health  # noqa: F401
import archivist.routes.collections  # noqa: F401
import archivist.routes.documents  # noqa: F401

from archivist.config import settings

app = mcp.http_app()


def main() -> None:
    uvicorn.run(
        "archivist.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
