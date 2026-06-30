from backend.tools import pdf_search_tool

def run_agent(query, vector_store, llm_call):

    context_chunks = pdf_search_tool(vector_store, query)
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are a smart AI agent.

Use the context below to answer:

Context:
{context}

User Question:
{query}

If context is not enough, say you are not sure.
"""

    return llm_call(prompt)