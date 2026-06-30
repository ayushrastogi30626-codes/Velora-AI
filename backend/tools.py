def pdf_search_tool(vector_store, query):
    return vector_store.search(query)