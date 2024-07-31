
def generate_prompt(query: str, query_res: list)->str:
    prompt = '''
        You are a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
        Use only the facts from the CONTEXT when answering the QUESTION.

        QUESTION: {question}

        CONTEXT: {context}
        '''.strip()
    
    context = ""

    for doc in query_res:
        context = context + f"section:{doc['section']}\nquestion:f{doc['question']}\nanswer:f{doc['text']}\n\n"
        
    return prompt.format(question=query, context=context)
