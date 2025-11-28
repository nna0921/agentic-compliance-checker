import streamlit as st
import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from config import POLICY_RULES
from rate_limiter import rate_limited, chat_limiter, embed_limiter


load_dotenv()

class RateLimitedEmbeddings(GoogleGenerativeAIEmbeddings):
    def embed_documents(self, texts):
        batch_size = 20 
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            embed_limiter.wait() 
            try:
                embeddings = super().embed_documents(batch)
                all_embeddings.extend(embeddings)
            except Exception as e:
                st.error(f"Error embedding batch: {e}")
                import time
                time.sleep(5)
                embeddings = super().embed_documents(batch)
                all_embeddings.extend(embeddings)
            
        return all_embeddings

    def embed_query(self, text):
        embed_limiter.wait()
        return super().embed_query(text)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

@rate_limited(chat_limiter)
def ask_gemini_safely(chain, inputs):
    return chain.invoke(inputs)

def process_pdf(uploaded_file):
    """Ingests PDF, chunks it, and creates a Vector Store."""
    temp_path = os.path.join("data", "temp.pdf")
    os.makedirs("data", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    loader = PyPDFLoader(temp_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)

    embeddings = RateLimitedEmbeddings(model="models/text-embedding-004")
    
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        collection_name="compliance_check_session"
    )
    return vectorstore

def check_compliance(vectorstore):
    """Iterates through rules and checks the document against them."""
    results = []
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    template = """
    You are a strict Compliance Officer. Compare the contract text to the rule.
    
    RULE: {rule}
    
    CONTRACT CONTEXT:
    {context}
    
    INSTRUCTIONS:
    1. Determine if the contract "PASS" (complies), "FAIL" (violates), or "MISSING" (not mentioned).
    2. Extract a short quote as EVIDENCE.
    3. If FAIL or MISSING, suggest a FIX.
    
    OUTPUT JSON ONLY:
    {{
        "status": "PASS" | "FAIL" | "MISSING",
        "evidence": "...",
        "fix": "..."
    }}
    """
    prompt = PromptTemplate(template=template, input_variables=["rule", "context"])
    chain = prompt | llm

    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, rule in enumerate(POLICY_RULES):
        progress = (i + 1) / len(POLICY_RULES)
        progress_bar.progress(progress)
        status_text.text(f"Checking Rule {i+1}/{len(POLICY_RULES)}: {rule['category']}...")
        
        relevant_docs = retriever.invoke(rule["search_query"])
        context_text = "\n\n".join([d.page_content for d in relevant_docs])

        try:
            response = ask_gemini_safely(chain, {
                "rule": rule["description"], 
                "context": context_text
            })
            
            raw_content = response.content.strip().replace('```json', '').replace('```', '')
            try:
                data = json.loads(raw_content)
            except json.JSONDecodeError:
                data = {"status": "ERROR", "evidence": "AI JSON Error", "fix": raw_content}

            results.append({
                "Rule ID": rule["id"],
                "Category": rule["category"],
                "Status": data.get("status", "UNKNOWN"),
                "Evidence": data.get("evidence", "No evidence found"),
                "Remediation": data.get("fix", "No fix needed")
            })
            
        except Exception as e:
            results.append({
                "Rule ID": rule["id"],
                "Category": rule["category"],
                "Status": "ERROR",
                "Evidence": str(e),
                "Remediation": "Check Logs"
            })

    status_text.empty()
    return results

st.set_page_config(page_title="Compliance Agent", layout="wide")

st.title("🤖 Agentic Compliance Checker")
st.markdown("""
* **Engine:** Gemini 2.5 Flash
* **Speed:** Optimized with dual-rate limiting (10 RPM Chat / 100 RPM Embeddings)
""")

uploaded = st.file_uploader("Upload Contract (PDF)", type="pdf")

if uploaded and st.button("Run Compliance Audit"):
    with st.spinner("Ingesting & Vectorizing Document..."):
        v_store = process_pdf(uploaded)
    
    st.success("Document Indexed. Starting Rule Check...")
    
    compliance_data = check_compliance(v_store)
    
    st.divider()
    st.subheader("📊 Compliance Comparison Table")
    
    df = pd.DataFrame(compliance_data)

    def color_status(val):
        if str(val).upper() == "FAIL":
            return 'background-color: #ffcccc; color: black;'
        elif str(val).upper() == "PASS":
            return 'background-color: #ccffcc; color: black;'
        elif str(val).upper() == "MISSING":
            return 'background-color: #ffffcc; color: black;'
        return ''

    if not df.empty:
        styled_df = df.style.map(color_status, subset=['Status'])
        st.dataframe(
            styled_df, 
            use_container_width=True,
            column_config={
                "Evidence": st.column_config.TextColumn("Evidence Found", width="medium"),
                "Remediation": st.column_config.TextColumn("Suggested Fix", width="medium"),
                "Status": st.column_config.TextColumn("Compliance Status", width="small")
            }
        )
        
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Audit Report (CSV)",
            data=csv,
            file_name="compliance_report.csv",
            mime="text/csv",
        )
    else:
        st.warning("No results found.")