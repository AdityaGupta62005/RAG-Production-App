from fastapi import FastAPI
import inngest.fast_api

from app.core.inngest_client import (
    inngest_client
)

from app.workflows.ingest_workflow import (
    rag_ingest_pdf
)

from app.workflows.query_workflow import (
    rag_query_pdf_ai
)

app = FastAPI()

inngest.fast_api.serve(
    app,
    inngest_client,
    [
        rag_ingest_pdf,
        rag_query_pdf_ai
    ]
)