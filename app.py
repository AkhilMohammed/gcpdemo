import streamlit as st
import base64
from cryptography.fernet import Fernet
from google.cloud import aiplatform
from google.oauth2 import service_account
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Image

PROJECT_ID = "genai-project-447217"
REGION = "us-central1"
vertexai.init(project=PROJECT_ID, location=REGION)
generative_multimodal_model = GenerativeModel("gemini-1.5-flash-002")

# Generate and load encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Google Vertex AI Setup
def get_vertex_ai_response(encrypted_prompt):
    decrypted_prompt = cipher_suite.decrypt(encrypted_prompt.encode()).decode()

    # Send decrypted prompt to Vertex AI model and get response
    response = generative_multimodal_model.generate_content([decrypted_prompt])

    # Extract and return the answer text
    if response and response.candidates:
        return response.candidates[0].content.parts[0].text
    else:
        return "No response received from the model."

# Streamlit Interface
def main():
    st.title("Google Vertex AI with Encryption")
    
    # Get the user's input
    prompt = st.text_input("Enter your prompt:")

    if st.button("Send to Google Vertex AI"):
        if prompt:
            # Encrypt the input
            encrypted_prompt = cipher_suite.encrypt(prompt.encode()).decode()

            # Send encrypted prompt to Google Vertex AI
            st.write(f"Encrypted Prompt: {encrypted_prompt}")
            response = get_vertex_ai_response(encrypted_prompt)
            
            # Show only the answer
            st.write("Response from Vertex AI:")
            st.write(response)
        else:
            st.error("Please enter a prompt to send.")
        
if __name__ == "__main__":
    main()
