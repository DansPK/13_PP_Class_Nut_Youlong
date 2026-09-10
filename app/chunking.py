"""
Text chunking strategies for splitting documents into manageable pieces.
"""

# paragraph breaks, line breaks, sentence endings, words,
# then finally individual characters if nothing else made a piece small enough
SEPARATORS = ["\n\n", "\n", ". ", " ", ""]


def merge_pieces(pieces: list[str], chunk_size: int, separator: str) -> list[str]:
    """
    put small pieces back together into one chunk, up to chunk_size.
    """
    chunks = []
    current = ""

    for piece in pieces:
        candidate = current + separator + piece if current else piece

        if len(candidate) <= chunk_size:
            current = candidate
        else:
            if current:
                chunks.append(current)
            current = piece
    if current:
        chunks.append(current)

    return chunks


def recursive_split(text: str, chunk_size: int, separators: list[str]) -> list[str]:
    """
    Split text using a priority list of separators
    """
    # fits already, or nothing left to split on -- stop recursing
    if len(text) <= chunk_size or not separators:
        return [text]

    separator, remaining_separators = separators[0], separators[1:]
    pieces = text.split(separator)

    chunks = []
    for piece in pieces:
        if len(piece) <= chunk_size:
            chunks.append(piece)
        else:
            # recurse one level more granular (e.g. paragraph -> sentence)
            chunks.extend(recursive_split(piece, chunk_size, remaining_separators))

    # splitting often leaves pieces far smaller than chunk_size (a lone
    # header, a short line) -- merge them
    # chunk on one short piece
    return merge_pieces(chunks, chunk_size, separator)


def add_overlap(chunks: list[str], overlap_chars: int) -> list[str]:
    """
    Repeat the tail end of each chunk at the start of the next one, so an
    idea that sits right on a chunk boundary doesn't lose its context.
    """
    if not chunks or overlap_chars <= 0:
        return chunks

    overlapped = [chunks[0]]
    for previous, current in zip(chunks, chunks[1:]):
        tail = previous[-overlap_chars:]
        overlapped.append(tail + " " + current)

    return overlapped


def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """
    The full chunking pipeline: split recursively, then add overlap.
    """
    chunks = recursive_split(text, chunk_size, SEPARATORS)
    return add_overlap(chunks, overlap)
