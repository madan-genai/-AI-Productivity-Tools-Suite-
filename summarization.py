from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from typing import TypedDict, Optional, Literal
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

parser = StrOutputParser()

class AgentState(TypedDict):
    task_type: str

    text: Optional[str]
    image_path: Optional[str]

    summary_length: Optional[str]
    target_language: Optional[str]
    explanation: Optional[bool]

    result: Optional[dict]

def route(state):
    task = state["task_type"]

    if task == "summary":
        return "summarization_state"
    elif task == "translation":
        return "translation"
    elif task == "grammar_check":
        return "grammar_check_state"
    elif task == "image_describer" or task == "image":
        return "image_describer"
    return END


class SummarizationRequest(BaseModel):
    text: str = Field(..., description= "The text to be summarized")
    summary_length: Literal["short", "medium", "detailed"] = Field(..., description =" the desired length of the summary: short (1-3 sentences), medium (1-2 paragraphs), or detailed (comprehensive summary)")


def summarization_state(state: AgentState) -> AgentState:
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert AI Text Summarizer.

Your goal is to generate a high-quality summary.

Summary Length: {summary_length}

Rules:
- Preserve meaning and context
- No hallucination or added information
- Remove redundancy
- Keep important facts
- Return only the summary
"""
        ),
        (
            "human",
            "Text:\n{text}"
        )
    ])

    chain = prompt | llm | parser

    response = chain.invoke({
        "text": state["text"],
        "summary_length": state["summary_length"]
    })

    return {
        **state,
        "result": response
    }