import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Create Gemini Client
client = genai.Client(api_key=API_KEY)

# Page Configuration
st.set_page_config(
    page_title="AI Requirements Copilot",
    page_icon="🤖",
    layout="wide"
)

# Title
st.title("🤖 AI Requirements Copilot")
st.write("Generate Requirements, Acceptance Criteria and Test Cases using Gemini")

# Feature Description Input
feature_description = st.text_area(
    "Enter Feature Description",
    height=250,
    placeholder="""
Example:

Wireless Android Auto Connection

The infotainment system shall allow users to connect Android Auto wirelessly.
The system should reconnect automatically after vehicle restart.
Users shall receive a notification if connection fails.
"""
)

# Generate Button
if st.button("Generate Requirements", type="primary"):

    if not feature_description.strip():
        st.warning("Please enter a feature description.")
        st.stop()

    # Prompt
    prompt = f"""
You are a Senior Automotive Requirements Engineer.

Analyze the feature description and generate the following sections.

## 1. Functional Requirements
- Use SHALL statements
- Number each requirement (FR-001, FR-002...)
- Use professional automotive requirement language

## 2. Non Functional Requirements
Cover:
- Performance
- Reliability
- Security
- Usability

Number each requirement (NFR-001, NFR-002...)

## 3. Acceptance Criteria
Provide measurable acceptance criteria.

## 4. Test Cases
Generate:
- Test Case ID
- Test Case Description
- Expected Result

Feature Description:

{feature_description}
"""

    try:

        with st.spinner("Generating Requirements..."):

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        st.success("Requirements Generated Successfully")

        st.markdown(response.text)

    except Exception as e:
        st.error(f"Error: {str(e)}")