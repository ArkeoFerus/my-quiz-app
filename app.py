import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai
import json

# Configure Gemini API
genai.configure(api_key="AIzaSyC1meCPDpOcegRFfjK0egpdI9NRBsAjjrs")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in doc)
    return text[:2000]  # Limit text to first 2000 chars

def generate_quiz(text):
    prompt = f"""
    Generate a short quiz (5 multiple-choice questions) from the following text:
    {text}
    Format: JSON with 'questions' (list of dicts with 'question', 'options', 'answer')
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return None

def main():
    st.title("📚 AI-Powered PDF Quiz Generator")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        text = extract_text_from_pdf(uploaded_file)
        st.write("Extracted text preview:", text[:500] + "...")
        
        if st.button("Generate Quiz"):
            quiz = generate_quiz(text)
            if quiz:
                st.session_state.quiz = quiz
                st.session_state.score = 0
                st.session_state.current_question = 0
            else:
                st.error("Failed to generate quiz. Try again.")
    
    if 'quiz' in st.session_state:
        quiz = st.session_state.quiz
        q_idx = st.session_state.current_question
        
        if q_idx < len(quiz['questions']):
            q = quiz['questions'][q_idx]
            st.subheader(f"Q{q_idx+1}: {q['question']}")
            choice = st.radio("Select an answer:", q['options'], key=q_idx)
            
            if st.button("Submit Answer"):
                if choice == q['answer']:
                    st.session_state.score += 1
                st.session_state.current_question += 1
                st.experimental_rerun()
        else:
            st.success(f"Quiz Completed! Your Score: {st.session_state.score}/{len(quiz['questions'])}")
            st.session_state.clear()

if __name__ == "__main__":
    main()
