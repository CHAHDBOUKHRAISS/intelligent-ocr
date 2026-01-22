"""Script to run the Streamlit web application."""

import subprocess
import sys
from pathlib import Path
import os

if __name__ == "__main__":
    
    app_path = Path(__file__).parent.parent / "src" / "intelligent_ocr" / "web" / "streamlit_app" / "main.py"
    
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    src_path = project_root / "src"
    os.environ["PYTHONPATH"] = str(src_path)
    
    subprocess.run([
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ])
