from openai import OpenAI

client = OpenAI()

def generate_answer(
    question: str,
    contexts: list[str]
) -> str:

    context_block = "\n\n".join(
        f"- {c}"
        for c in contexts
    )

    user_content = (
        "Use the following context "
        "to answer the question.\n\n"
        f"Context:\n{context_block}\n\n"
        f"Question: {question}\n"
        "Answer concisely using the context above."
    )

    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        max_tokens=1024,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": (
                    "You answer questions "
                    "using only the provided context."
                )
            },
            {
                "role": "user",
                "content": user_content
            }
        ]
    )

    return response.choices[0].message.content