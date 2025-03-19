import streamlit as st
import spacy
import ollama

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")

llm_model = "llama3.2"

# Sample knowledge base (FAQs)
FAQS = {
    "admission process": (
        "Admission to MIST's B.Tech programs requires a valid TS EAMCET score. "
        "For MBA programs, a TS ICET score is necessary. Ensure you meet the eligibility criteria before applying."
    ),
    "fee structure": (
        "The annual fee for B.Tech programs is approximately ₹75,000. "
        "For detailed information, please visit the official website."
    ),
    "hostel facilities": (
        "MIST provides hostel facilities equipped with Wi-Fi, mess services, and 24/7 security. "
        "For more details, contact the administration."
    ),
    "scholarships": (
        "Scholarships are available based on merit and financial need. "
        "Interested students should apply through the scholarship portal."
    ),
    "placement opportunities": (
        "The placement cell collaborates with top companies like TCS, Wipro, Cognizant, Infosys, and Accenture. "
        "The highest package offered was ₹12 LPA, with an average of ₹4.5 LPA."
    ),
    "courses offered": (
        "MIST offers undergraduate programs like B.Tech in various specializations, "
        "postgraduate programs like M.Tech, and an MBA program."
    ),
    "contact details": (
        "Address: Vyasapuri, Bandlaguda, Post: Keshavgiri, Hyderabad-500005, Telangana, India. "
        "Phone: 040-29880079, 040-29880086. Email: principal.mahaveer@gmail.com."
    )
}

def chat_with_bot(query):
    # Preprocess query with spaCy
    doc = nlp(query.lower())
    for key in FAQS:
        if key in query.lower():
            return FAQS[key]
    
    # If not found, use Ollama for smart responses
    context = " ".join(FAQS.values())  # Combine FAQs as context
    ollama_prompt = f"You are a helpful college assistant. Answer based on the following context:\n{context}\nUser query: {query}"
    
    response = ollama.chat(model=llm_model, messages=[{"role": "user", "content": ollama_prompt}])
    return response['message']['content']

# Streamlit UI
st.set_page_config(page_title="College Chatbot", layout="wide")
st.title("🎓 AI College Chatbot")
st.write("Ask any questions related to admissions, fees, courses, and more!")

# User input
user_input = st.text_input("Type your question here:")
if st.button("Ask"): 
    if user_input:
        response = chat_with_bot(user_input)
        st.markdown(f"**Chatbot:** {response}")
    else:
        st.warning("Please enter a question.")
