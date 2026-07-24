import os

from dotenv import load_dotenv
from openai import OpenAI

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

from ingest import load_faq_data, build_index
from rag_helper import RAGBase

load_dotenv()

provider = TracerProvider()
provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)


class RAGTraced(RAGBase):

    def search(self, query, num_results=5):
        with tracer.start_as_current_span("search"):
            return super().search(query, num_results=num_results)

    def llm(self, prompt):
        with tracer.start_as_current_span("llm"):
            return super().llm(prompt)

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


if __name__ == "__main__":
    assistant = create_traced_assistant()

    query = "How does the agentic loop keep calling the model until it stops?"
    answer = assistant.rag(query)

    print()
    print(answer)
