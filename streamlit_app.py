import streamlit as st

try:
    # OpenAI Python library v1
    from openai import OpenAI
    _use_client = True
except ImportError:  # pragma: no cover - fallback for OpenAI < 1.0
    import openai
    OpenAI = None
    _use_client = False

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client. Support both v1 and older versions of the
    # library so the app works regardless of the installed package version.
    if _use_client:
        client = OpenAI(api_key=openai_api_key)
    else:
        openai.api_key = openai_api_key
        client = openai

    # Let the user upload a file via `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via `st.text_area`.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        # Generate an answer using the OpenAI API.
        if _use_client:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )
        else:
            stream = client.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                stream=True,
            )

        # Stream the response to the app using `st.write_stream`.
        st.write_stream(stream)
