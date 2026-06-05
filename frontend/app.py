import streamlit as st
import requests

# ==================================
# CONFIG
# ==================================
st.set_page_config(
    page_title="AI Productivity Suite",
    page_icon="🧠",
    layout="wide"
)

BASE_URL = "http://localhost:8000"


# ==================================
# RESPONSE HANDLER
# ==================================
def handle_response(response, expected_key):
    try:
        response.raise_for_status()

        data = response.json()

        if expected_key not in data:
            st.error(
                f"Expected key '{expected_key}' not found.\n\n"
                f"Response: {data}"
            )
            return None

        return data[expected_key]

    except requests.exceptions.JSONDecodeError:
        st.error(
            "Backend returned invalid JSON.\n\n"
            f"Response:\n{response.text}"
        )

    except requests.exceptions.HTTPError:
        st.error(
            f"HTTP Error: {response.status_code}\n\n"
            f"Response:\n{response.text}"
        )

    except Exception as e:
        st.error(str(e))

    return None


# ==================================
# API FUNCTIONS
# ==================================
def summarize(text, length):
    try:
        response = requests.post(
            f"{BASE_URL}/summarize",
            json={
                "text": text,
                "summary_length": length
            },
            timeout=120
        )

        return handle_response(response, "summary")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI server.\n\n"
            "Start backend first:\n"
            "uvicorn main:app --reload"
        )

    except Exception as e:
        st.error(str(e))

    return None


def translate(text, lang):
    try:
        response = requests.post(
            f"{BASE_URL}/translate",
            json={
                "text": text,
                "target_language": lang
            },
            timeout=120
        )

        return handle_response(response, "translation")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI server.\n\n"
            "Start backend first."
        )

    except Exception as e:
        st.error(str(e))

    return None


def grammar_check(text, explanation):
    try:
        response = requests.post(
            f"{BASE_URL}/grammar_check",
            json={
                "text": text,
                "explanation": explanation
            },
            timeout=120
        )

        return handle_response(
            response,
            "grammar_check_result"
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI server."
        )

    except Exception as e:
        st.error(str(e))

    return None


def describe_image(file, text=""):
    try:
        response = requests.post(
            f"{BASE_URL}/describe-image",
            files={"file": file},
            data={"text": text},
            timeout=180
        )

        return handle_response(response, "description")

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to FastAPI server."
        )

    except Exception as e:
        st.error(str(e))

    return None


# ==================================
# UI HEADER
# ==================================
st.markdown(
    """
    <h1 style='text-align:center;color:#4F46E5'>
        🧠 AI Productivity Suite
    </h1>

    <p style='text-align:center;color:gray'>
        Summarization • Translation • Grammar Check • Vision AI
    </p>

    <hr>
    """,
    unsafe_allow_html=True
)


# ==================================
# SIDEBAR
# ==================================
choice = st.sidebar.radio(
    "Select Tool",
    [
        "📝 Summarizer",
        "🌍 Translator",
        "✍️ Grammar Check",
        "🖼️ Image Describer"
    ]
)


# ==================================
# RESULT DISPLAY
# ==================================
def show_result(title, result):
    st.markdown(f"### {title}")
    st.success(result)


# ==================================
# SUMMARIZER
# ==================================
if choice == "📝 Summarizer":

    st.subheader("Text Summarization Engine")

    text = st.text_area(
        "Enter your text",
        height=200
    )

    length = st.selectbox(
        "Summary Type",
        [
            "short",
            "medium",
            "detailed"
        ]
    )

    if st.button("Generate Summary"):

        if not text.strip():
            st.warning("Please enter text.")
        else:
            with st.spinner("Generating summary..."):
                result = summarize(
                    text,
                    length
                )

            if result:
                show_result(
                    "📌 Summary",
                    result
                )


# ==================================
# TRANSLATOR
# ==================================
elif choice == "🌍 Translator":

    st.subheader("AI Translation Engine")

    text = st.text_area(
        "Enter text",
        height=200
    )

    lang = st.text_input(
        "Target Language"
    )

    if st.button("Translate"):

        if not text.strip():
            st.warning("Enter text.")

        elif not lang.strip():
            st.warning("Enter target language.")

        else:
            with st.spinner("Translating..."):
                result = translate(
                    text,
                    lang
                )

            if result:
                show_result(
                    "🌍 Translation",
                    result
                )


# ==================================
# GRAMMAR CHECKER
# ==================================
elif choice == "✍️ Grammar Check":

    st.subheader(
        "Grammar & Writing Assistant"
    )

    text = st.text_area(
        "Enter text",
        height=200
    )

    explanation = st.checkbox(
        "Show explanations"
    )

    if st.button("Check Grammar"):

        if not text.strip():
            st.warning("Enter text first.")

        else:
            with st.spinner(
                "Checking grammar..."
            ):
                result = grammar_check(
                    text,
                    explanation
                )

            if result:
                show_result(
                    "✍️ Grammar Result",
                    result
                )


# ==================================
# IMAGE DESCRIBER
# ==================================
elif choice == "🖼️ Image Describer":

    st.subheader(
        "Vision AI Image Analyzer"
    )

    uploaded_file = st.file_uploader(
        "Upload Image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )

    context = st.text_input(
        "Optional context"
    )

    if uploaded_file:
        st.image(
            uploaded_file,
            caption="Image Preview",
            use_container_width=True
        )

    if st.button("Analyze Image"):

        if not uploaded_file:
            st.warning(
                "Upload an image first."
            )

        else:
            with st.spinner(
                "Analyzing image..."
            ):
                result = describe_image(
                    uploaded_file,
                    context
                )

            if result:
                show_result(
                    "🖼️ Image Analysis",
                    result
                )


# ==================================
# FOOTER
# ==================================
st.markdown("---")

st.markdown(
    """
    <p style='text-align:center;color:gray'>
        Built with Streamlit + FastAPI + LangGraph
    </p>
    """,
    unsafe_allow_html=True
)

