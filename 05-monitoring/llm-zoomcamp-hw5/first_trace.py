import os
import sqlite3

from dotenv import load_dotenv
from openai import OpenAI

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor, SpanExporter, SpanExportResult
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from ingest import load_faq_data, build_index
from rag_helper import RAGBase

load_dotenv()


class SQLiteSpanExporter(SpanExporter):

    def __init__(self, db_path="traces.db"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spans (
                name TEXT,
                start_time INTEGER,
                end_time INTEGER,
                input_tokens INTEGER,
                output_tokens INTEGER,
                cost REAL
            )
        """)
        self.conn.commit()

    def export(self, spans):
        for span in spans:
            attrs = dict(span.attributes or {})
            self.conn.execute(
                "INSERT INTO spans VALUES (?, ?, ?, ?, ?, ?)",
                (
                    span.name,
                    span.start_time,
                    span.end_time,
                    attrs.get("input_tokens"),
                    attrs.get("output_tokens"),
                    attrs.get("cost"),
                ),
            )
        self.conn.commit()
        return SpanExportResult.SUCCESS

    def shutdown(self):
        self.conn.close()

    def force_flush(self, timeout_millis=30000):
        return True


memory_exporter = InMemorySpanExporter()

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

provider.add_span_processor(SimpleSpanProcessor(memory_exporter))
provider.add_span_processor(SimpleSpanProcessor(SQLiteSpanExporter("traces.db")))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)


class RAGTraced(RAGBase):

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm") as span:
            messages = [
                {"role": "system", "content": self.instructions},
                {"role": "user", "content": prompt}
            ]

            response = self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            usage = response.usage
            span.set_attribute("input_tokens", usage.prompt_tokens)
            span.set_attribute("output_tokens", usage.completion_tokens)

            print(f"input_tokens={usage.prompt_tokens} output_tokens={usage.completion_tokens}")

            return response

    def rag(self, query):
        with tracer.start_as_current_span("rag"):
            return super().rag(query)


def create_traced_assistant():
    documents = load_faq_data()
    index = build_index(documents)

    return RAGTraced(
        index=index,
        llm_client=OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        ),
    )


def report_spans():
    spans = memory_exporter.get_finished_spans()

    print()
    print(f"Total spans: {len(spans)}")

    for span in spans:
        duration_ms = (span.end_time - span.start_time) / 1_000_000
        print(f"  {span.name}: {duration_ms:.2f} ms")


if __name__ == "__main__":
    assistant = create_traced_assistant()

    query = "How does the agentic loop keep calling the model until it stops?"
    answer = assistant.rag(query)

    print()
    print(answer)

    report_spans()


