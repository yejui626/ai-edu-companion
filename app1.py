import streamlit as st
import base64

def display_pdf(pdf_path):
    try:
        with open(pdf_path, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # Display PDF using PDF.js viewer
        pdf_display = f"""
            <iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"PDF file not found: {pdf_path}")

def chatbot_interface():
    st.title("AI Teaching Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask a question about the material"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Add assistant response (placeholder for now)
        response = "This is a placeholder response. You'll need to integrate your preferred AI model here."
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Display assistant response
        with st.chat_message("assistant"):
            st.markdown(response)

# Main layout
pdf_path = "example.pdf"  # Replace with your PDF path

# Create two columns with custom widths (70% for PDF, 30% for chat)
col1, col2 = st.columns([0.7, 0.3])

with col1:
    display_pdf(pdf_path)

with col2:
    chatbot_interface()

# Custom CSS to ensure the chat column stays fixed
st.markdown("""
    <style>
        [data-testid="stHorizontalBlock"] {
            align-items: flex-start;
        }
    </style>
    """, unsafe_allow_html=True)