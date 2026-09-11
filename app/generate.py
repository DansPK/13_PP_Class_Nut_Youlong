from openai import OpenAI
from retrieval import search_chroma
from config import TOP_K, TEMPERATURE, SIMILARITY_THRESHOLD, SYSTEM_PROMPT, GEN_MODEL, OPENAI_BASE_URL, OPENAI_COMPATIBLE_API_KEY

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_COMPATIBLE_API_KEY,
)


def build_prompt(question: str, chunks: list[dict]) -> str:

    context = "\n\n".join(
        f"[{int(chunk['source'].split('_')[0]):02d}] {chunk['source']}\n{chunk['text']}"
        for chunk in chunks
    )

    return f"""Context:
{context}

Question: {question}
Answer:"""


def generate_answer(question: str, history: list[dict] = None, top_k: int = TOP_K, temperature: float = TEMPERATURE, similarity_threshold: float = SIMILARITY_THRESHOLD, stream: bool = False, chunks: list[dict] = None) -> tuple[str, list[dict], list[dict]]:

    if history is None:
        history = []

    # 1. Retrieve: find chunks related to the question 
    if chunks is None:
        chunks = search_chroma(question, top_k=top_k, similarity_threshold=similarity_threshold)

    # stuff chunks into the prompt as context
    prompt = build_prompt(question, chunks)

    #the LLM to answer, using the system prompt + prior turns + this question
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": prompt}]

    if stream:
        response = client.chat.completions.create(
            model=GEN_MODEL,
            messages=messages,
            temperature=temperature,
            stream=True,
        )
        pieces = []
        for event in response:
            delta = event.choices[0].delta.content
            if delta:
                pieces.append(delta)
                print(delta, end="", flush=True)
        print()
        answer = "".join(pieces)
    else:
        response = client.chat.completions.create(
            model=GEN_MODEL,
            messages=messages,
            temperature=temperature,
        )
        answer = response.choices[0].message.content

    # remember for next time
    history = history + [
        {"role": "user", "content": question},
        {"role": "assistant", "content": answer},
    ]

    return answer, history, chunks
