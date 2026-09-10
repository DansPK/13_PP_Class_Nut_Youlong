"""
Stage 1 of the pipeline: turn raw files in data/ into searchable vectors.

Flow: load files
"""

from pathlib import Path
from typing import List, Tuple

# __file__ is the path to *this* Python file.
# .resolve() parent goes up one directory (app/ -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"



def load_documents(data_dir: str = DATA_DIR) -> List[Tuple[str, str]]:
    """
     Load documents from data directory.

     Returns a list of (filename, full_text) for every .txt file in data_dir.
    """
    documents = []

    for file_path in Path(data_dir).glob("*.txt"):
        # read the text
        text = file_path.read_text(encoding="utf-8")

        # add file_path meta and text together for citation later
        documents.append((file_path.name, text))

    return documents
