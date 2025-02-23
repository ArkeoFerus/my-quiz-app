import streamlit as st

st.title("Simple Calculator")

# Input fields
num1 = st.number_input("Enter first number", value=0.0)
num2 = st.number_input("Enter second number", value=0.0)

# Operation selection
operation = st.selectbox("Select operation", ["+", "-", "*", "/"])

# Calculation function
def calculate(num1, num2, operation):
    if operation == "+":
        return num1 + num2
    elif operation == "-":
        return num1 - num2
    elif operation == "*":
        return num1 * num2
    elif operation == "/":
        if num2 == 0:
            return "Cannot divide by zero"
        else:
            return num1 / num2
    else:
        return "Invalid operation"

# Calculate and display result
if st.button("Calculate"):
    result = calculate(num1, num2, operation)
    st.write("Result:", result)
