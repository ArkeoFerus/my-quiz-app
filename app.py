import streamlit as st
from PyPDF2 import PdfReader

# Check if google-generativeai is installed
try:
    import google.generativeai as genai
except ImportError:
    st.error("The 'google-generativeai' library is not installed. Please install it using: `pip install google-generativeai`")
    st.stop()

# Set up Gemini API
try:
    genai.configure(api_key="AIzaSyC1meCPDpOcegRFfjK0egpdI9NRBsAjjrs")  # Replace with your actual API key
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

# Initialize Gemini model
try:
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Failed to initialize Gemini model: {e}")
    st.stop()

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to generate quiz using Gemini
def generate_quiz(text, num_questions=5):
    prompt = f"""
    Generate a quiz with {num_questions} multiple-choice questions based on the following text:
    
    {text}
    
    Each question should have 4 options and a correct answer. Format the output as follows:
    
    Question 1: [Question text]
    A) [Option 1]
    B) [Option 2]
    C) [Option 3]
    D) [Option 4]
    Correct Answer: [Correct option]
    
    Repeat for all questions.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Failed to generate quiz: {e}")
        return None

# Streamlit App
st.title("Quiz Generator from PDF")
st.write("Upload a PDF file, and we'll generate a quiz for you!")

# File upload
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from PDF
    text = extract_text_from_pdf(uploaded_file)
    st.write("Text extracted from PDF successfully!")

    # Number of questions
    num_questions = st.slider("Number of questions", min_value=1, max_value=10, value=5)

    # Generate quiz
    if st.button("Generate Quiz"):
        st.write("Generating quiz...")
        quiz = generate_quiz(text, num_questions)
        if quiz:
            st.write("### Quiz:")
            st.write(quiz)
