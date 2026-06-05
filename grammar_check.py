from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from summarization import AgentState, llm
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field 

parser = StrOutputParser()

class GrammarCheckRequest(BaseModel):
    text: str = Field(..., description= "The text to be grammar checked")
    explanation: Optional[bool] = Field(False, description= "Whether to provide explanations for the corrections (default: False)")
def grammar_check_state(state: AgentState) -> AgentState:

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert AI Grammar and Writing Assistant.

Your task is to correct grammar, spelling, punctuation, and sentence structure errors.

Rules:
- Preserve meaning and intent
- Do not add new information
- Make only necessary corrections
- Maintain original tone and formatting
- If no errors exist, return the original text and state no issues found

Explanation Mode: {explanation}

If explanation is True:
- List each correction briefly with reason

Output Format:
Corrected Text:
<corrected text>

If explanation is True:
Corrections:
- bullet points

Status (if no errors):
No grammar or spelling errors detected.
"""
        ),
        (
            "human",
            "Text:\n{text}"
        )
    ])

    chain = prompt | llm | parser

    result = chain.invoke({
        "text": state["text"],
        "explanation": state.get("explanation", False)
    })

    return {
        **state,
        "result": result
    }