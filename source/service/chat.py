from util.retriever import Retriever
from util.llm_client import ask_llm
from prompt.prompt import SYSTEM_PROMPT, HUMAN_PROMPT

async def chat(query: str, collection: str = "default", persist_dir: str = "index_data"):
    retriever = Retriever(collection_name=collection, persist_dir=persist_dir)

    hits = await retriever.search(query, top_k=3)
    context = "\n\n---\n\n".join([h["text"] for h in hits])

    system_prompt = SYSTEM_PROMPT.format(context=context)
    human_prompt = HUMAN_PROMPT.format(question=query)

    print(f"SYSTEM PROMPT\n")
    print(system_prompt)
    print(f"USER PROMPT\n")
    print(human_prompt)

    answer = ask_llm(system_prompt=system_prompt, user_prompt=human_prompt, model="gpt-oss-20b")
    return {"query": query, "response": answer, "sources": hits}