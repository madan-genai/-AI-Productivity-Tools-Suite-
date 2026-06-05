from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from summarization import AgentState, llm
from typing import Dict, Any
from pydantic import BaseModel, Field

parser = StrOutputParser()

class TranslationRequest(BaseModel):
    text: str = Field(..., description= "The text to be translated")
    target_language: str = Field(..., description= "The language to translate the text into (e.g., 'French', 'Spanish', 'Chinese')")

def translation(state: AgentState) -> AgentState:

    if not state["text"]:
        raise ValueError("Missing input text for translation")

    if not state["target_language"]:
        raise ValueError("Missing target_language in state")

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an expert AI Translation System.

Translate text into the specified target language while preserving meaning, tone, and intent.

Capabilities:
- Accurate translation
- Tone preservation (formal/informal/technical/conversational)
- Natural fluency in target language

Rules:
1. Do not change meaning
2. Do not add explanations or extra content
3. Preserve tone and intent
4. Keep names, numbers, dates, and technical terms unchanged
5. Maintain formatting (paragraphs, lists)
6. Return ONLY translated text
7. If already in target language, return as-is

Target Language: {target_language}
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
        "target_language": state["target_language"]
    })

    return {
        **state,
        "result": result
    }