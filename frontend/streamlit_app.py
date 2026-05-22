import asyncio
import os
import time
from pathlib import Path

import inngest
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="RAG AI Assistant",
    page_icon="🤖",
    layout="wide"
)


if "messages" not in st.session_state:
    st.session_state.messages = []

@st.cache_resource
def get_inngest_client() -> inngest.Inngest:
    return inngest.Inngest(
        app_id="rag_app",
        is_production=False
    )

def save_uploaded_pdf(file) -> Path:
    uploads_dir = Path("uploads")
    uploads_dir.mkdir(parents=True, exist_ok=True)

    file_path = uploads_dir / file.name
    file_path.write_bytes(file.getbuffer())

    return file_path

async def send_rag_ingest_event(pdf_path: Path):
    client = get_inngest_client()

    await client.send(
        inngest.Event(
            name="rag/ingest_pdf",
            data={
                "pdf_path": str(pdf_path.resolve()),
                "source_id": pdf_path.name,
            },
        )
    )

async def send_rag_query_event(question: str, top_k: int):
    client = get_inngest_client()

    result = await client.send(
        inngest.Event(
            name="rag/query_pdf_ai",
            data={
                "question": question,
                "top_k": top_k,
            },
        )
    )

    return result[0]

def _inngest_api_base() -> str:
    return os.getenv(
        "INNGEST_API_BASE",
        "http://127.0.0.1:8288/v1"
    )

def fetch_runs(event_id: str) -> list[dict]:
    url = f"{_inngest_api_base()}/events/{event_id}/runs"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return data.get("data", [])

def wait_for_run_output(
    event_id: str,
    timeout_s: float = 120.0,
    poll_interval_s: float = 0.5
) -> dict:

    start = time.time()
    last_status = None

    while True:
        runs = fetch_runs(event_id)

        if runs:
            run = runs[0]

            status = run.get("status")
            last_status = status or last_status

            if status in (
                "Completed",
                "Succeeded",
                "Success",
                "Finished",
            ):
                return run.get("output") or {}

            if status in ("Failed", "Cancelled"):
                raise RuntimeError(f"Function run {status}")

        if time.time() - start > timeout_s:
            raise TimeoutError(
                f"Timed out waiting for run output "
                f"(last status: {last_status})"
            )

        time.sleep(poll_interval_s)

with st.sidebar:

    st.title(" RAG Control Panel")

    st.divider()

    top_k = st.slider(
        "Chunks to Retrieve",
        min_value=1,
        max_value=20,
        value=5,
    )

    st.divider()

    uploaded_files = st.file_uploader(
        "Upload PDFs",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        for uploaded_file in uploaded_files:

            with st.spinner(f"Ingesting {uploaded_file.name}..."):

                path = save_uploaded_pdf(uploaded_file)

                asyncio.run(
                    send_rag_ingest_event(path)
                )

                time.sleep(0.3)

            st.success(f" {uploaded_file.name} uploaded")

    st.divider()

    uploads_dir = Path("uploads")

    st.subheader("Uploaded Documents")

    if uploads_dir.exists():

        pdfs = list(uploads_dir.glob("*.pdf"))

        if pdfs:
            for pdf in pdfs:
                st.write(f" {pdf.name}")
        else:
            st.caption("No PDFs uploaded yet")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

st.title("📚 RAG AI Assistant")

st.caption(
    "Upload PDFs and ask intelligent questions "
    "using Retrieval-Augmented Generation"
)

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])=

prompt = st.chat_input(
    "Ask something about your PDFs..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        with st.spinner("Thinking..."):

            try:
                event_id = asyncio.run(
                    send_rag_query_event(
                        prompt,
                        int(top_k)
                    )
                )

                output = wait_for_run_output(event_id)

                answer = output.get("answer", "")
                sources = output.get("sources", [])

                full_response = ""

                for word in answer.split():

                    full_response += word + " "

                    response_placeholder.markdown(
                        full_response
                    )

                    time.sleep(0.02)

                if sources:

                    with st.expander("📄 Sources"):

                        for source in sources:
                            st.markdown(f"- {source}")

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as e:

                error_message = f"Error: {str(e)}"

                response_placeholder.error(
                    error_message
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_message
                    }
                )