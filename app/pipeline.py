"""
RAG Pipeline: Connects retriever and generator.

Takes a question, retrieves relevant chunks, and generates a grounded answer.
"""

from dotenv import load_dotenv
load_dotenv() 

from config import TOP_K, TEMPERATURE, SIMILARITY_THRESHOLD
from generate import generate_answer


def ask(question: str, history: list[dict] = None, top_k: int = TOP_K, 
        temperature: float = TEMPERATURE, 
        similarity_threshold: float = SIMILARITY_THRESHOLD, 
        stream: bool = False, chunks: list[dict] = None) -> tuple[str, list[dict], list[dict]]:

    return generate_answer(question,
                            history=history, 
                            top_k=top_k, 
                            temperature=temperature, 
                            similarity_threshold=similarity_threshold, 
                            stream=stream, chunks=chunks)


if __name__ == "__main__":
    question = "how do I reset a forgotten PIN?"
    answer, history, chunks = ask(question)
    print(f"Question: {question}")
    print(f"Answer: {answer}")
