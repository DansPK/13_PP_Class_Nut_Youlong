"""
Stage 3 of the pipeline: turn (question + retrieved chunks) into a grounded answer.

Sends question and context to the LLM and returns the answer.
"""
from typing import List


def build_prompt(query: str, chunks: List[dict]) -> str:
    """
    Build the augmented prompt with context and question.

    Args:
        query: The user's question
        chunks: List of retrieved context chunks

    Returns:
        The formatted prompt to send to the LLM
    """
    pass


def generate_answer(query: str, chunks: List[dict]) -> str:
    """
    Generate a grounded answer using the LLM.

    Args:
        query: The user's question
        chunks: List of retrieved context chunks

    Returns:
        The generated answer
    """
    pass
