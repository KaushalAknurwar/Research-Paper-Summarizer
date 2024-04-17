import openai
import json
import os
import fitz
import streamlit as st
import time
from functools import lru_cache

# Function to retrieve OpenAI API key from a JSON file
def get_openai_key():
    with open(r'\Users\ASUS\OneDrive\Desktop\hoho\OpenAI.json', 'r') as file_to_read:
        json_data = json.load(file_to_read)
        return json_data["OPENAI_API_KEY"]

# Memoization (caching) decorator for the Summarize function
@lru_cache(maxsize=None)
def summarize_cached(pdf_file_name):
    return Summarize(pdf_file_name)

# Function to summarize text from a PDF file using GPT-3
def Summarize(pdf_file_name):
    openai.api_key = get_openai_key()
    doc = fitz.open(r'\Users\ASUS\AIRST-research-paper-summarization\pdf_folder\\' + pdf_file_name + '.pdf')
    summary_list = []

    for page in doc:
        text = page.get_text("text")
        prompt = "Summarize " + pdf_file_name + " by Introduction " + text
        response = make_request_with_rate_limit(prompt)
        summary_list.append(response["choices"][0]["text"])

    summary_text = ' '.join(summary_list)
    return summary_text

# Function to make API requests with rate limiting
def make_request_with_rate_limit(prompt):
    max_requests_per_minute = 3
    seconds_per_request = 60 / max_requests_per_minute

    # Ensure rate limit compliance
    time_since_last_request = time.time() - make_request_with_rate_limit.last_request_time
    if time_since_last_request < seconds_per_request:
        time.sleep(seconds_per_request - time_since_last_request)

    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    make_request_with_rate_limit.last_request_time = time.time()
    return response

make_request_with_rate_limit.last_request_time = 0

# Main function
def main():
    st.set_page_config(page_title='Paper Summarization', page_icon=':memo:', layout='wide')
    st.sidebar.title("Drag your Paper here for Summarization :')))")

    uploaded_file = st.sidebar.file_uploader("", type="pdf")
    pdf_file_name = None

    if uploaded_file is not None:
        pdf_file_name = uploaded_file.name.replace('.pdf', '')

    if pdf_file_name is not None:
        my_bar = st.progress(0)
        summary_text = summarize_cached(pdf_file_name)  # Use the cached function
        my_bar.progress(100)
        st.title("Summarization")
        st.write(summary_text)

    st.title("Ask a question")
    s = st.text_input("Type something you want to ask about this paper summarization:")

    if pdf_file_name is not None and s:
        prompt = s + " " + summary_text
        response = make_request_with_rate_limit(prompt)
        st.write(response["choices"][0]["text"])

if __name__ == '__main__':
    main()
