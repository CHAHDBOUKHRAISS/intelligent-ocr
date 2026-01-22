"""Script to run the FastAPI server."""

import sys
from pathlib import Path
import uvicorn
from intelligent_ocr.config.settings import settings

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    src_path = project_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    uvicorn.run(
        "intelligent_ocr.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=False  
    )
