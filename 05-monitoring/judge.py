import os
from pydantic import BaseModel
from typing import Literal
from openai import OpenAI
from dotenv import load_dotenv

from evaluation_utils import llm_structured_retry

JUDGE_INSTRUCTIONS = """
You are an expert evaluator for a RAG system.
Analyze the relevance of the generated answer to the given question.

Classify the answer as:
- RELEVANT: the answer addresses the question
- PARTLY_RELEVANT: the answer partially addresses the question
- NON_RELEVANT: the answer does not address the question
""".strip()

JUDGE_PROMPT = """
Question: {question}
Generated Answer: {answer}
""".strip()

class RelevanceVerdict(BaseModel):
    relevance: Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]
    explanation: str

def evaluate_relevance(question, answer, client=None):
    if client is None:
        client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )

    prompt = JUDGE_PROMPT.format(question=question, answer=answer)

    result, _ = llm_structured_retry(
        client,
        JUDGE_INSTRUCTIONS,
        prompt,
        RelevanceVerdict,
    )

    return result.relevance, result.explanation


if __name__ == "__main__":
    load_dotenv()

    question = "Can I still join the course?"
    answer = "Yes, you can still join. The course is self-paced."

    relevance, explanation = evaluate_relevance(question, answer)
    print(relevance)
    print(explanation)