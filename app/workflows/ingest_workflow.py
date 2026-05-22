import datetime
import inngest

from app.core.inngest_client import inngest_client
from app.models.custom_types import (
    RAGChunkAndSrc,
    RAGUpsertResult
)
from app.services.ingestion_service import (
    load_pdf_chunks,
    upsert_chunks
)

@inngest_client.create_function(
    fn_id="RAG: Ingest PDF",
    trigger=inngest.TriggerEvent(
        event="rag/ingest_pdf"
    ),
    throttle=inngest.Throttle(
        limit=2,
        period=datetime.timedelta(minutes=1)
    ),
    rate_limit=inngest.RateLimit(
        limit=1,
        period=datetime.timedelta(hours=4),
        key="event.data.source_id",
    ),
)
async def rag_ingest_pdf(
    ctx: inngest.Context
):

    pdf_path = ctx.event.data["pdf_path"]

    source_id = ctx.event.data.get(
        "source_id",
        pdf_path
    )

    chunks_and_src = await ctx.step.run(
        "load-and-chunk",
        lambda: load_pdf_chunks(
            pdf_path,
            source_id
        ),
        output_type=RAGChunkAndSrc
    )

    ingested = await ctx.step.run(
        "embed-and-upsert",
        lambda: upsert_chunks(
            chunks_and_src
        ),
        output_type=RAGUpsertResult
    )

    return ingested.model_dump()