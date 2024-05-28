import time

import requests
import streamlit as st

# Define the API endpoint
API_ENDPOINT = "http://0.0.0.0:8888/ask"  # Replace with your actual API endpoint


# Function to call the API
def get_response_from_api(prompt):
    # Create the query parameter
    params = {"query": prompt}
    response = requests.get(API_ENDPOINT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": "API request failed with status code {}".format(
                response.status_code
            )
        }


# Function to inject custom typing effect animation
def inject_typing_animation():
    st.markdown(
        """
    <style>
    .dot-container {
        display: flex;
        justify-content: left;
        align-items: left;
        height: 100px;
    }
    .dot {
        width: 10px;
        height: 10px;
        margin: 0 5px;
        background-color: gray;
        border-radius: 50%;
        animation: jump 1s infinite;
    }
    .dot:nth-child(2) {
        animation-delay: 0.1s;
    }
    .dot:nth-child(3) {
        animation-delay: 0.2s;
    }
    @keyframes jump {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    </style>
    <div class="dot-container">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    </div>
    """,
        unsafe_allow_html=True,
    )


# Streamlit app
def main():
    st.title("Prompt Input and API Response App")

    # Create a form for user input
    user_input = st.text_area("Enter your prompt here:")

    # Handle form submission
    if user_input:
        # Inject typing animation
        typing_container = st.empty()
        with typing_container:
            inject_typing_animation()

        # Call API
        response = get_response_from_api(user_input)

        # Clear typing animation
        typing_container.empty()

        if "error" in response:
            st.error(response["error"])
        else:
            # st.success("API response received!")
            response_text = response.get("assistant", "No response content")
            typing_container.markdown(
                f"""
            <div style="padding: 15px; border-radius: 5px; border: 1px solid #ccc;">
                {response_text}
            </div>
            """,
                unsafe_allow_html=True,
            )
    # else:
        # st.warning("Please enter a prompt before submitting.")


if __name__ == "__main__":
    main()
