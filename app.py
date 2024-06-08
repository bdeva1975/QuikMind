import streamlit as st
from transformers import pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from openai import OpenAI

# Initialize Sentiment Analyzer
sentiment_analyzer = SentimentIntensityAnalyzer()

# Initialize text summarization pipeline
summarizer = pipeline("summarization")

# Function for sentiment analysis
def analyze_sentiment(text):
    return sentiment_analyzer.polarity_scores(text)

# Function for personality traits (simplified example)
def determine_personality(text):
    # A placeholder function to simulate personality traits
    if "help" in text.lower():
        return "Helpful"
    elif "book" in text.lower():
        return "Organized"
    else:
        return "Friendly"

# Function to summarize text
def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return summary[0]['summary_text']

# Function to summarize from URL or file
def summarize_content(content):
    # Assume content is preprocessed to extract text
    return summarize_text(content)

# Chatbot response generator
def generate_response(user_input, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that goes through user input and answers the questions in a polite manner."
            },
            {
                "role": "user",
                "content": f'\n\n QUESTION: {user_input}'
            }
        ],
        temperature=0.35,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content
# Your OpenAI API key
api_key = '<OPENAI-API-KEY>'

# Streamlit App
st.title("QuikMind - Conversational AI Chatbot")

# User input
user_input = st.text_input("You: ")

# Display chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if user_input:
    # Analyze sentiment
    sentiment = analyze_sentiment(user_input)
    personality = determine_personality(user_input)
    
    # Generate response
    response = generate_response(user_input)
    
    # Update chat history
    st.session_state.chat_history.append({"User": user_input, "Bot": response, "Sentiment": sentiment, "Personality": personality})
    
    # Display chat history
    for chat in st.session_state.chat_history:
        st.write(f"User: {chat['User']}")
        st.write(f"Bot: {chat['Bot']}")
        st.write(f"Sentiment: {chat['Sentiment']}")
        st.write(f"Personality: {chat['Personality']}")
        st.write("---")

# Additional functionalities
st.header("Additional Functionalities")

# News summarization
st.subheader("Summarize News Articles")
text_input = st.text_area("Enter text or URL:")
file_input = st.file_uploader("Upload a file")

if st.button("Summarize"):
    if text_input:
        summary = summarize_text(text_input)
        st.write(summary)
    elif file_input:
        content = file_input.read().decode('utf-8')
        summary = summarize_content(content)
        st.write(summary)

# Appointment booking
st.subheader("Book an Appointment")
name = st.text_input("Name")
email = st.text_input("Email")
date = st.date_input("Appointment Date")
time = st.time_input("Appointment Time")

if st.button("Book Appointment"):
    st.write(f"Appointment booked for {name} on {date} at {time}. Confirmation sent to {email}.")