'''
Task: Assist a technology ecommerce company named
"Makers Tech" in creating a ChatBot that responds
to and informs users through a graphical interface
about the inventory, features, and prices of the
products currently available. This is based on the 
question asked.

Main Goal: use an AI system to provide real-time
inventory information through a personalized
conversation.

What do we have in our project?
- A main.py file that contains the main logic of the chatbot.
- A requirements.txt file that lists the dependencies needed for the chatbot to run.
- A README.md file that provides an overview of the project and how to set it up.

- A Supabase simple database that stores the product information.
- Streamlit for creating the web application interface.
- An AI model for processing user queries and providing relevant responses.
'''

# Makers Tech ChatBot
import streamlit as st
import os, sys
from supabase import create_client, Client
from google import genai
from dotenv import load_dotenv


load_dotenv() # Load environment variables from .env file

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
gemini_api_key = os.environ.get("GEMINI_API_KEY")
if not gemini_api_key:
    st.error("GEMINI_API_KEY not found in environment variables. Please set it in your .env file.")
    st.stop()
gemini_client = genai.Client(api_key=gemini_api_key)

# Initializing the Supabase client
supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

st.title("Makers Agentic Inventory ChatBot")
st.write("Ask a question about our inventory below:")

user_question = st.text_input("Your Question:")


if st.button("Submit"):
    if user_question:
        # Example: fetch all products (improvements needed in the future)
        products_response = supabase.table("Product Data").select("*").execute()
        products = products_response.data if products_response.data else []

        # Format product info for Gemini
        product_info = ""
        for p in products:
            product_info += f"- {p['name']}: {p['description']} (${p['price']}, {p['stock_count']} in stock)\n"

        prompt = f"""
        You are an expert AI assistant for Makers Tech.
        Here is the current inventory:
        {product_info}
        ---
        User question: {user_question}
        Answer the user's question using only the inventory above.
        """

        # Get response from Gemini AI
        response = gemini_client.models.generate_content(
              model="gemini-2.5-flash",
              contents=prompt
        )
        # Print the response
        st.write(response.text)
    else:
        st.error("Please enter a question.")