import inngest

from app.core.inngest_client import inngest_client
from app.services.retrieval_service import (
    retrieve_contexts
)
from app.services.llm_service import (
    generate_answer
)
from app.models.custom_types import (
    RAGSearchResult
)

@inngest_client.create_function(
    fn_id="RAG: Query PDF",
    trigger=inngest.TriggerEvent(
        event="rag/query_pdf_ai"
    )
)
async def rag_query_pdf_ai(
    ctx: inngest.Context
):

    question = ctx.event.data["question"]

    top_k = int(
        ctx.event.data.get(
            "top_k",
            5
        )
    )

    found = await ctx.step.run(
        "embed-and-search",
        lambda: retrieve_contexts(
            question,
            top_k
        ),
        output_type=RAGSearchResult
    )

    answer_text = await ctx.step.run(
        "llm-answer",
        lambda: generate_answer(
            question,
            found.contexts
        )
    )

    return {
        "answer": answer_text,
        "sources": found.sources,
        "num_contexts": len(found.contexts)
    }