"""
Loads raw documents from data folder
"""

from pathlib import Path
from typing import List, Tuple
from config import DATA_DIR



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
