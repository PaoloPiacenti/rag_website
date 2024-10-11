import streamlit as st
import requests
import uuid
import time

import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load environment variables from .env file
load_dotenv()

# Retrieve the values from the environment
from_email = os.getenv("EMAIL_USER")  # Load email from .env file
email_password = os.getenv("EMAIL_PASS")  # Load app password from .env file

# Hardcoded dictionary to map source filenames to URLs
source_mapping = {
    "00-Setup_01-Setup.pdf": "https://kitt.lewagon.com/camps/1758/lectures/00-Setup",
    "01-Python_01-Programming-Basics.pdf": "https://kitt.lewagon.com/camps/1758/lectures/01-Python%2F01-Programming-Basics",
    "01-Python_02-Data-Sourcing.pdf": "https://kitt.lewagon.com/camps/1758/lectures/01-Python%2F02-Data-Sourcing",
    "01-Python_03-SQL-Basics.pdf": "https://kitt.lewagon.com/camps/1758/lectures/01-Python%2F03-SQL-Basics",
    "01-Python_04-SQL-Advanced.pdf": "https://kitt.lewagon.com/camps/1758/lectures/01-Python%2F04-SQL-Advanced",
    "02-Data-Toolkit_01-Data-Analysis.pdf": "https://kitt.lewagon.com/camps/1758/lectures/02-Data-Toolkit%2F01-Data-Analysis",
    "02-Data-Toolkit_02-Data-Sourcing.pdf": "https://kitt.lewagon.com/camps/1758/lectures/02-Data-Toolkit%2F02-Data-Sourcing",
    "02-Data-Toolkit_03-Data-Visualization.pdf": "https://kitt.lewagon.com/camps/1758/lectures/02-Data-Toolkit%2F03-Data-Visualization",
    "03-Maths_01-Algebra-Calculus.pdf": "https://kitt.lewagon.com/camps/1758/lectures/03-Maths%2F01-Algebra-Calculus",
    "03-Maths_02-Statistics-Probabilities.pdf": "https://kitt.lewagon.com/camps/1758/lectures/03-Maths%2F02-Statistics-Probabilities",
    "04-Decision-Science_01-Project-Setup.pdf": "https://kitt.lewagon.com/camps/1758/lectures/04-Decision-Science%2F01-Project-Setup",
    "04-Decision-Science_02-Statistical-Inference.pdf": "https://kitt.lewagon.com/camps/1758/lectures/04-Decision-Science%2F02-Statistical-Inference",
    "04-Decision-Science_03-Linear-Regression.pdf": "https://kitt.lewagon.com/camps/1758/lectures/04-Decision-Science%2F03-Linear-Regression",
    "04-Decision-Science_04-Logistic-Regression.pdf": "https://kitt.lewagon.com/camps/1758/lectures/04-Decision-Science%2F04-Logistic-Regression",
    "04-Decision-Science_05-Communicate.pdf": "https://kitt.lewagon.com/camps/1758/lectures/04-Decision-Science%2F05-Communicate",
    "05-ML_01-Fundamentals-of-Machine-Learning.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F01-Fundamentals-of-Machine-Learning",
    "05-ML_02-Data-preparation.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F02-Data-preparation",
    "05-ML_03-Linear-Models.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F03-Linear-Models",
    "05-ML_04-Tree-based-Models.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F04-Tree-based-Models",
    "05-ML_05-Unsupervised-Learning.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F05-Unsupervised-Learning",
    "05-ML_06-Model-interpretability.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F06-Model-interpretability",
    "05-ML_07-Ensemble-Methods.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F07-Ensemble-Methods",
    "05-ML_08-Workflow.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F08-Workflow",
    "05-ML_09-Time-Series.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F09-Time-Series",
    "05-ML_10-Natural-Language-Processing.pdf": "https://kitt.lewagon.com/camps/1758/lectures/05-ML%2F10-Natural-Language-Processing",
    "06-DL_01-Fundamentals-of-Deep-Learning.pdf": "https://kitt.lewagon.com/camps/1758/lectures/06-Deep-Learning%2F01-Fundamentals-of-Deep-Learning",
    "06-DL_02-Optimizer-loss-and-fitting.pdf": "https://kitt.lewagon.com/camps/1758/lectures/06-Deep-Learning%2F02-Optimizer-loss-and-fitting",
    "06-DL_03-Convolutional-Neural-Networks.pdf": "https://kitt.lewagon.com/camps/1758/lectures/06-Deep-Learning%2F03-Convolutional-Neural-Networks",
    "06-DL_04-RNN_NLP.pdf": "https://kitt.lewagon.com/camps/1758/lectures/06-Deep-Learning%2F04-RNN-and-NLP",
    "06-DL_05-Transformers.pdf": "https://kitt.lewagon.com/camps/1758/lectures/06-Deep-Learning%2F05-Transformers",
    "07-ML-Ops_01-Train-at-scale.pdf": "https://kitt.lewagon.com/camps/1758/lectures/07-ML-Ops%2F01-Train-at-scale",
    "07-ML-Ops_02-Cloud-training.pdf": "https://kitt.lewagon.com/camps/1758/lectures/07-ML-Ops%2F02-Cloud-training",
    "07-ML-Ops_03-Automate-model-lifecycle.pdf": "https://kitt.lewagon.com/camps/1758/lectures/07-ML-Ops%2F03-Automate-model-lifecycle",
    "07-ML-Ops_04-Predict-in-production.pdf": "https://kitt.lewagon.com/camps/1758/lectures/07-ML-Ops%2F04-Predict-in-production",
    "07-ML-Ops_05-User-interface.pdf": "https://kitt.lewagon.com/camps/1758/lectures/07-ML-Ops%2F05-User-interface",
    "08-Projects_01-Coding-as-a-team.pdf": "https://kitt.lewagon.com/camps/1758/lectures/08-Projects%2F01",
    "08-Projects_02-CI_CD.pdf": "https://kitt.lewagon.com/camps/1758/lectures/08-Projects%2F02",
    "08-Projects_03-Gen_AI.pdf": "https://kitt.lewagon.com/camps/1758/lectures/08-Projects%2F03",
    "08-Projects_04-XAI.pdf": "https://kitt.lewagon.com/camps/1758/lectures/08-Projects%2F04"
}

# Function to send feedback email
def send_email(feedback, conversation):
    to_email = "work.paolopiacenti@gmail.com"
    subject = "RAG Feedback - LeWagon"

    # Set up the MIME
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject

    # Construct the email body
    email_body = f"User Feedback:\n{feedback}\n\nConversation History:\n{conversation}"
    message.attach(MIMEText(email_body, "plain"))

    try:
        # Sending the mail using Gmail's SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, email_password)  # Use the app password loaded from env variable
        text = message.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        st.success("Feedback submitted and email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")


# Function to make API request
def get_bot_response(question, session_id):
    url = "https://chat-api-523296903372.europe-west1.run.app/ask"
    headers = {"Content-Type": "application/json"}
    data = {
        "question": question,
        "session_id": session_id
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# Initialize session state for the conversation and feedback
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'feedback_given' not in st.session_state:
    st.session_state['feedback_given'] = False
if 'feedback_text' not in st.session_state:
    st.session_state['feedback_text'] = ""
if 'input_key' not in st.session_state:
    st.session_state['input_key'] = str(uuid.uuid4())  # Use a unique key for each session

# Chat display function with chat bubbles
def display_chat():
    # Container to hold chat history and autoscroll
    chat_container = st.empty()
    with chat_container.container():
        for message in st.session_state['history']:
            if message["type"] == "user":
                st.markdown(f"""
                    <div class='message-row'>
                        <div class='icon'>
                            <img src='https://img.icons8.com/color/48/000000/user-male-circle--v1.png' width='40' />
                        </div>
                        <div class='message user-message'>
                            {message['content']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class='message-row'>
                        <div class='icon'>
                            <img src='https://img.icons8.com/color/48/000000/robot-2.png' width='40' />
                        </div>
                        <div class='message bot-message'>
                            {message['content']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        # Scroll to the latest message
        st.markdown(f"<div id='chat-end'></div>", unsafe_allow_html=True)
        st.markdown(f"<script>document.getElementById('chat-end').scrollIntoView();</script>", unsafe_allow_html=True)

# Inject CSS for sticky input and chat bubble styling
st.markdown("""
    <style>
    .message-row {
        display: flex;
        align-items: center;
        margin-bottom: 10px;
    }
    .icon {
        flex-shrink: 0;
        margin-right: 10px;
    }
    .message {
        padding: 10px;
        border-radius: 10px;
        max-width: 80%;
    }
    .user-message {
        background-color: #daf7dc;
        text-align: left;
        animation: fadeIn 0.5s;
    }
    .bot-message {
        background-color: #f0f0f5;
        text-align: left;
        animation: fadeIn 0.5s;
    }
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    .fixed-input {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: white;
        padding: 10px;
        z-index: 999;
        border-top: 2px solid #ccc;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🤖 The Bot Teaching Assistant")

# Introductory paragraph
st.markdown("""
**Hello!** Welcome to the Bot Teaching Assistant for the Data Science and AI course.
This bot has been fine-tuned using all the PDFs from the course, with the goal of helping students easily retrieve course content.

**Author**: Paolo Piacenti, Batch #1758
[**LinkedIn**](https://www.linkedin.com/in/paolopiacenti/)

*Note*: The bot may provide some inaccurate answers, so please use it with caution!
""")

# Display chat history
display_chat()

# Create a fixed input box at the bottom of the screen
input_container = st.container()

# Input for user's query (Submit on ENTER)
with input_container:
    user_input = st.text_input(
        "Ask a question",
        key=st.session_state['input_key'],
        placeholder="Type your message here...",
        on_change=lambda: st.session_state.update({"send_button": True}),
        args=()
    )

# Process the input when the button or ENTER key is pressed
if "send_button" in st.session_state and st.session_state['send_button']:
    # Add user message to the conversation
    if user_input:
        st.session_state['history'].append({"type": "user", "content": user_input})

        # Show a loading spinner while waiting for bot response
        with st.spinner("🤖 Bot is thinking..."):
            time.sleep(1)  # Simulate a short delay for effect
            try:
                # Call the chatbot API to get the response
                result = get_bot_response(user_input, st.session_state.session_id)
                answer = result['answer']
                sources = result['sources']

                # If the answer is not "I don't know.", include sources as clickable links
                if answer.lower() != "i don't know.":
                    # Remove duplicate sources
                    sources = list(set(sources))
                    if sources:
                        sources_text = "\n\n**Sources:**\n" + "\n".join([f"- [{source}]({source_mapping.get(source, '#')})" for source in sources])
                        answer += sources_text

                # Add bot message to the conversation
                st.session_state['history'].append({"type": "bot", "content": answer})

            except Exception as e:
                st.error(f"An error occurred: {e}")

        # Clear the input field after submission
        st.session_state['input_key'] = str(uuid.uuid4())  # Generate a new key to reset the input field
        st.session_state['send_button'] = False  # Reset the send button state

        # Rerun to update the displayed conversation
        st.experimental_rerun()

# Sidebar for feedback submission
with st.sidebar:
    st.subheader("End Session and Provide Feedback")

    # Show feedback input if feedback not already given
    if not st.session_state['feedback_given']:
        st.session_state['feedback_text'] = st.text_area("Please provide your feedback:", value=st.session_state['feedback_text'])

        # Submit feedback button
        if st.button("Submit Feedback", key="feedback_button"):
            if st.session_state['feedback_text']:
                # Construct the conversation history as a string
                conversation = "\n".join([f"{msg['type'].capitalize()}: {msg['content']}" for msg in st.session_state['history']])

                # Send the email with the feedback and conversation
                send_email(st.session_state['feedback_text'], conversation)

                # Mark feedback as given
                st.session_state['feedback_given'] = True
            else:
                st.warning("Please enter some feedback before submitting.")
    else:
        st.info("Feedback already submitted. Thank you!")
