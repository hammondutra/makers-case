# 🤖 Makers Tech Inventory ChatBot

A simple yet powerful chatbot built with Streamlit and Google's Gemini AI to answer customer questions about product inventory. The chatbot connects to a Supabase database to fetch real-time product information, providing an interactive conversational experience for users of the "Makers Tech" e-commerce store.

![ChatBot Demo](https://drive.google.com/file/d/1RRYX6NBSkGxpdlUeGlePlQMecxmXzctO/view?usp=sharing) 
*Note: You should replace the link above with a real screenshot or GIF of your application.*

---

## ✨ Features

* **Conversational AI**: Powered by Google's `Gemini-1.5-Flash` model for natural and context-aware responses.
* **Real-time Data**: Fetches live product inventory, pricing, and descriptions directly from a Supabase database.
* **Interactive UI**: A clean and user-friendly chat interface built with Streamlit.
* **Session History**: Maintains the context of the conversation for a seamless user experience.
* **Easy Setup**: Simple configuration using environment variables.

---

## 🛠️ Tech Stack

* **App Framework**: [Streamlit](https://streamlit.io/)
* **AI Model**: [Google Gemini](https://ai.google.dev/)
* **Database**: [Supabase](https://supabase.io/)
* **Language**: [Python](https://www.python.org/)

---

## 🚀 Getting Started

Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* Python 3.8+
* A Google AI API Key. You can get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
* A Supabase account and project. You can sign up at [Supabase](https://supabase.com/).

### 1. Clone the Repository

```bash
git clone [https://github.com/hammondutra/makers-case.git](https://github.com/hammondutra/makers-case.git)
cd makers-case
```

### 2. Install Dependencies

It's recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate # On Windows, use `venv\Scripts\activate`

# Install the required packages
pip install -r requirements.txt
```
*(Note: You will need to create a `requirements.txt` file containing `streamlit`, `google-generativeai`, `supabase`, and `python-dotenv`)*

### 3. Set Up Environment Variables

Create a file named `.env` in the root of your project directory and add your API keys and Supabase credentials.

```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
SUPABASE_KEY="YOUR_SUPABASE_ANON_KEY"
```

### 4. Set Up Your Supabase Database

1.  In your Supabase project, create a new table named `Product Data`.
2.  Ensure the table has the following columns:
    * `name` (type: `text`)
    * `description` (type: `text`)
    * `price` (type: `numeric`)
    * `stock_count` (type: `int4` or `integer`)
3.  Add some product data to the table so the chatbot has information to share.

### 5. Run the Application

Once the setup is complete, run the following command in your terminal:

```bash
streamlit run app.py
```
*(Assuming your Python script is named `app.py`)*

Your browser should automatically open a new tab with the chatbot interface running.

---

## 🔮 Future Improvements

This project serves as a great proof-of-concept. Here are some planned enhancements:

* **Implement Vector Search**: Replace the current method of fetching all products with a more efficient **Retrieval-Augmented Generation (RAG)** pipeline. This involves creating vector embeddings for product descriptions and performing a semantic search to retrieve only the most relevant products for the AI's context window.
* **Enhanced Error Handling**: Improve user-facing error messages for database connection issues or API failures.
* **Streaming Responses**: Modify the app to stream the AI's response token-by-token for a more responsive, real-time feel.

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
