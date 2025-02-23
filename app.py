import tempfile
import streamlit as st
import base64
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

groq_api_key = st.secrets["GROQ_API_KEY"]

# Instantiate the ChatGroq model for translation
llm = ChatGroq(
    groq_api_key=groq_api_key,
    model="llama-3.3-70b-versatile",
    temperature=0,
)

def translate_text(text, target_lang="Malay"):
    # Define a system prompt that instructs the model to translate text.
    system_message = f"You are a helpful translation assistant. Translate the following text from English to {target_lang}. Provide only the translated text."
    # Create a prompt template using LangChain
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_message),
        ("user", "{input_text}")
    ])
    # Chain the prompt to the Groq LLM
    chain = prompt.pipe(llm)
    # Invoke the chain with the input text
    result = chain.invoke({"input_text": text})
    return result.content

def display_pdf(pdf_path):
    # Open and read the PDF file
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Display PDF using PDF.js viewer
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"PDF file not found: {pdf_path}")

st.set_page_config(layout="wide",menu_items={"About":"This is a simple app that allows you to translate text from English to Malay."})

# Sidebar
st.sidebar.title("Translation Settings")


# Main body
st.title("AI Education Companion")

# Add a file uploader for the PDF files
pdf_file_1 = st.file_uploader("Upload your file", type="pdf")

if pdf_file_1:
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(pdf_file_1.getvalue())
        temp_pdf_path = tmp_file.name
    
    # Display the uploaded PDF
    display_pdf(temp_pdf_path)
    tab1, tab2, tab3 = st.tabs(["PDF Translator", "Dog", "Owl"])

    with tab1:
        st.header("PDF Translator")

        # Add language selection dropdowns
        col_lang1, col_lang2 = st.columns(2)
        
        with col_lang1:
            # Detect source language using the LLM
            sample_text = "Extract some text from PDF for language detection"  # You'll need to implement PDF text extraction
            detected_lang = llm.invoke(f"What language is this text written in? Only respond with the language name: {sample_text}")
            st.write(f"Detected language: {detected_lang.content}")
            source_language = detected_lang.content
            source_language = st.selectbox(
                "Translate From:",
                ["Malay", "English", "Chinese", "Spanish", "French", "German"],
                index=0,
                disabled=True
            )
            
        with col_lang2:
            target_language = st.selectbox(
                "Translate to:",
                ["Malay", "English", "Chinese", "Spanish", "French", "German"],
                index=0
            )
            
        if source_language == target_language:
            st.warning("Please select different languages for translation")

        # Sample PDF paths (make sure these files exist in your directory)
        pdf_path_1 = "example1.pdf"
        pdf_path_2 = "translated_output.pdf"

        # Create two columns for side-by-side display
        col1, col2 = st.columns(2)

        with col1:
            display_pdf(pdf_path_1)

        with col2:
            display_pdf(pdf_path_2)

    with tab2:
        st.header("A dog")
        st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    with tab3:
        st.header("An owl")
        st.image("https://static.streamlit.io/examples/owl.jpg", width=200)

