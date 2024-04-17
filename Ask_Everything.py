import streamlit as st
import openai

# Set up OpenAI API credentials
openai.api_key = "sk-proj-Go6sRTuWL6T8JDH9XRLtT3BlbkFJIWkx924U7hejNRoM0WMb"

def generate_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        temperature=0.7,
        max_tokens=400,
        top_p=0.9,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    message = response.choices[0].text
    return message

def Ask_Everything():
    st.title(":dog: :green[AIRST] ")
    if 'generated' not in st.session_state:
        st.session_state['generated'] = []

    if 'past' not in st.session_state:
        st.session_state['past'] = []

    def get_text():
        input_text = st.text_input("The Good Doctor: You can ask more than just medical related questions", key="input")
        return input_text

    user_input = get_text()

    if user_input:
        output = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated']) - 1, -1, -1):
            st.write(st.session_state['generated'][i], key=str(i))
            st.write(st.session_state['past'][i], is_user=True, key=str(i) + '_user')

if __name__ == '__main__':
    Ask_Everything()
