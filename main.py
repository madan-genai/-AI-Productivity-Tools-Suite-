from fastapi import FastAPI, UploadFile , File, Form
from workflow import app as workflow_app
from summarization import AgentState
from summarization import SummarizationRequest
from translation import TranslationRequest
from grammar_check import GrammarCheckRequest
from image_describer import ImageDescriberRequest
import os
import shutil


app = FastAPI(title="AI Productivity Tools Suite")

# -------------------------
# SUMMARIZATION
# -------------------------
@app.post("/summarize")
async def summarize(request: SummarizationRequest):

    state = AgentState(
        task_type="summary",
        text=request.text,
        summary_length=request.summary_length,
        target_language=None,
        explanation=None,
        result=None
    )

    result = workflow_app.invoke(state)

    return {
        "summary": result["result"]
    }


# -------------------------
# TRANSLATION
# -------------------------
@app.post("/translate")
async def translate(request: TranslationRequest):
    state = AgentState(
        task_type="translation",
        text=request.text,
        target_language=request.target_language,
        summary_length=None,
        explanation=None,
        result=None
    )

    result = workflow_app.invoke(state)

    return {
        "translation": result["result"]
    }


# -------------------------
# GRAMMAR CHECK
# -------------------------
@app.post("/grammar_check")
async def grammar_check(request: GrammarCheckRequest):

    state = AgentState(
        task_type="grammar_check",
        text=request.text,
        explanation=request.explanation,
        summary_length=None,
        target_language=None,
        result=None
    )

    result = workflow_app.invoke(state)

    return {
        "grammar_check_result": result["result"]
    }

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/describe-image")
async def describe_image(
    file: UploadFile = File(...),
    text: str = Form(default="")
):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    state = {
        "task_type": "image_describer",
        "image_path": file_path,
        "text": text,
        "result": None
    }

    result = workflow_app.invoke(state)

    return {
        "description": result["result"]
    }

    