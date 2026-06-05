from typing import Optional

from fastapi import UploadFile

from summarization import AgentState, llm
from pydantic import BaseModel, Field

import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

class ImageDescriberRequest(BaseModel):
    text: Optional[str] = Field("", description= "Optional context or description to accompany the image")
    image: UploadFile = Field(..., description= "The image file to be described")


def image_describer(state: AgentState) -> AgentState:

    if not state.get("image_path"):
        raise ValueError("image_path is required")

    image_base64 = encode_image(state["image_path"])

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
You are an advanced Vision AI system.

Your tasks:
1. Describe the image in detail
2. Extract visible text (OCR-like)
3. Explain objects, scenes, and context
4. Provide an accessibility-friendly description
5. Generate a short caption

Return structured, clear output.
"""
        ),
        (
            "human",
            [
                {
                    "type": "text",
                    "text": "Context: {text}"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image}"
                    }
                }
            ]
        )
    ])

    chain = prompt | llm | parser

    result = chain.invoke({
        "text": state.get("text", ""),
        "image": image_base64
    })

    return {
        **state,
        "result": result
    }