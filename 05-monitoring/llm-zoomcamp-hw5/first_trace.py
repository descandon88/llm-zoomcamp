from rag_helper import RAGBase
import time
from dataclasses import dataclass, field
from datetime import datetime




class RAGTraced(): 

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
         #   self.last_call: LLMCallRecord = None

    def llm(self, prompt):
        start_time = time.time()
        response = self._call_llm(prompt)
        response_time = time.time() - start_time
        self._log_response(prompt, response, response_time)
        return response.output_text