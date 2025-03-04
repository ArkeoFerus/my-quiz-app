import streamlit as st
import fitz  # PyMuPDF for PDF extraction
from transformers import T5ForConditionalGeneration, T5Tokenizer
import random

# Load Pre-trained T5 Model (Offline)
model_name = "allenai/t5-small-squad2-question-generation"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = "\n".join(page.get_text("text") for page in doc)
    return text[:3000]  # Limit text for efficiency

# Function to Generate Questions using T5 Model
def generate_questions(text):
    input_text = f"generate questions: {text}"
    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    outputs = model.generate(input_ids, max_length=128, num_return_sequences=5)
    questions = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]

    quiz = []
    for q in questions:
        options = [q, "Option B", "Option C", "Option D"]
        random.shuffle(options)
        correct_answer = q  # First option is always correct
        quiz.append({"question": q, "options": options, "answer": correct_answer})
    
    return quiz

# Streamlit App
st.title("📚 AI-Powered PDF Quiz Generator (Offline)")

# File Upload
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    st.write("Extracted Text Preview:", text[:500] + "...")
    
    if st.button("Generate Quiz"):
        quiz = generate_questions(text)
        st.session_state.quiz = quiz
        st.session_state.score = 0
        st.session_state.current_question = 0

# Quiz Section
if 'quiz' in st.session_state:
    quiz = st.session_state.quiz
    q_idx = st.session_state.current_question
    
    if q_idx < len(quiz):
        q = quiz[q_idx]
        st.subheader(f"Q{q_idx+1}: {q['question']}")
        choice = st.radio("Select an answer:", q['options'], key=q_idx)
        
        if st.button("Submit Answer"):
            if choice == q['answer']:
                st.session_state.score += 1
            st.session_state.current_question += 1
            st.experimental_rerun()
    else:
        st.success(f"Quiz Completed! Your Score: {st.session_state.score}/{len(quiz)}")
        st.session_state.clear()

