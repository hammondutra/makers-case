# Makers Tech ChatBot - Revised
import streamlit as st
import os
import sys
from supabase import create_client, Client
import google.generativeai as genai
from dotenv import load_dotenv

# --- INITIALIZATION ---
def init_app():
    """Initializes environment variables and API clients."""
    load_dotenv()
    # Check for and configure Gemini API key
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        st.error("GEMINI_API_KEY not found. Please set it in your .env file.")
        st.stop()
    genai.configure(api_key=gemini_api_key)

    # Check for and create Supabase client
    supabase_url = os.environ.get("SUPABASE_URL")
    supabase_key = os.environ.get("SUPABASE_KEY")
    if not supabase_url or not supabase_key:
        st.error("Supabase URL or Key not found. Please set them in your .env file.")
        st.stop()
    supabase_client = create_client(supabase_url, supabase_key)
    
    return supabase_client

# --- DATA & AI FUNCTIONS ---
def get_product_data(db_client: Client):
    """
    Fetches product data from Supabase.
    
    Future Improvement: This should be replaced with a vector search
    to retrieve only relevant products based on the user's question.
    """
    try:
        # For now, we still fetch all, but the logic is isolated.
        response = db_client.table("Product Data").select("*").execute()
        return response.data if response.data else []
    except Exception as e:
        st.error(f"Error connecting to the database: {e}")
        return []

def get_ai_response(question: str, products: list) -> str:
    """Generates a response from the AI based on the user question and product data."""
    product_info = "\n".join([
        f"- {p['name']}: {p['description']} (${p['price']}, {p['stock_count']} in stock)"
        for p in products
    ])

    prompt = f"""
    You are a friendly and expert AI assistant for "Makers Tech", a technology ecommerce company.
    Your role is to answer user questions about our products based *only* on the inventory data provided below.
    If the information is not in the data, politely state that you don't have that information.
    
    Here is the current inventory:
    {product_info}
    ---
    User question: {question}
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"Error generating AI response: {e}")
        return "Sorry, I'm having trouble thinking right now. Please try again later."

# --- STREAMLIT UI ---
st.title("🤖 Makers Tech Inventory ChatBot")
st.write("Ask me anything about our products, prices, or stock!")

# Initialize clients and session state
supabase_client = init_app()
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])



# React to user input (chat-style UI)
if user_question := st.chat_input("What are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_question})
    with st.chat_message("user"):
        st.markdown(user_question)

    # Display bot response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # 1. Get data (fetch all products for now)
            products_response = supabase_client.table("Product Data").select("*").execute()
            products = products_response.data if products_response.data else []

            # 2. Format product info for Gemini
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

            # 3. Get response from Gemini AI
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            st.markdown(response.text)
            final_response = response.text
        
    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": final_response})