from starter import index, client

from first_trace import RAGTraced, report_spans


def calc_cost(usage, input_price_per_million=0.05, output_price_per_million=0.08):
    input_cost = (usage.prompt_tokens / 1_000_000) * input_price_per_million
    output_cost = (usage.completion_tokens / 1_000_000) * output_price_per_million
    return input_cost + output_cost


assistant = RAGTraced(index=index, llm_client=client)

query = "How does the agentic loop keep calling the model until it stops?"
answer = assistant.rag(query)

print(answer)

report_spans()
