import streamlit as st
import base64
from cryptography.fernet import Fernet
from google.cloud import aiplatform
from google.oauth2 import service_account

# Generate and load encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Google Vertex AI Setup
def get_vertex_ai_response(encrypted_prompt):
    # Replace with your Google Cloud credentials JSON file
    credentials_path = "secrets.json"
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    print(credentials)
    
    # Initialize Vertex AI
    aiplatform.init(credentials=credentials, project="genai-project-447217", location="us-central1")
    aiplatform.init(credentials=credentials)
    model_resource_name = "projects/genai-project-447217/locations/us-central1/models/publishers/google/models/gemini-1.5-flash-002"

    # Initialize the model
    model = aiplatform.Model(model_resource_name)

    # Assuming you're using a text generation model in Vertex AI
    # model = aiplatform.Model("projects/genai-project-447217/locations/us-central1/models/publishers/google/models/gemini-1.5-flash-002")
    
    decrypted_prompt = cipher_suite.decrypt(encrypted_prompt.encode()).decode()

    # Send decrypted prompt to Vertex AI model and get response
    response = model.predict([decrypted_prompt])
    return response.predictions[0]

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
            
            # Show the response
            st.write("Response from Vertex AI:")
            st.write(response)
        else:
            st.error("Please enter a prompt to send.")
        
if __name__ == "__main__":
    main()
