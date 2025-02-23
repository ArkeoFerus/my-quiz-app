import streamlit as st
import nltk
import re
import random
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import pos_tag

# Download required NLTK datasets
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# Step 1: Preprocess the Text
def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)  # Remove extra spaces
    sentences = sent_tokenize(text)  # Split text into sentences
    return sentences

# Step 2: Generate Quiz Questions
def generate_questions(sentences, num_questions=5):
    quiz_questions = []
    
    for _ in range(min(num_questions, len(sentences))):
        sentence = random.choice(sentences)  # Pick a random sentence
        words = word_tokenize(sentence)  # Tokenize into words
        tagged_words = pos_tag(words)  # Get POS tags
        
        # Identify nouns/proper nouns to replace with blanks
        blanks = [word for word, tag in tagged_words if tag in ["NN", "NNP"]]

        if blanks:
            word_to_replace = random.choice(blanks)
            question = sentence.replace(word_to_replace, "_____")  # Replace word with blank
            quiz_questions.append((question, word_to_replace))  # Store question + answer

    return quiz_questions

# Step 3: Evaluate Answers
def evaluate_answers(user_answers, correct_answers):
    score = 0
    for ua, ca in zip(user_answers, correct_answers):
        if ua.strip().lower() == ca.lower():  # Case-insensitive exact match
            score += 1
    return score

# Example Usage
text = """Albert Einstein was a physicist who developed the theory of relativity. 
He was born in Germany and later moved to the United States. 
Einstein received the Nobel Prize for his work on the photoelectric effect."""

sentences = preprocess_text(text)
quiz_questions = generate_questions(sentences)

print("Generated Quiz:")
for i, (question, answer) in enumerate(quiz_questions):
    print(f"Q{i+1}: {question} (Answer: {answer})")


# Calculate and display result
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write("Result:", result)
