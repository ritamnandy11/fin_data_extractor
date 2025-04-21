import google.generativeai as genai
import json
import pandas as pd
import os
import streamlit as st
#from dotenv import load_dotenv

#load_dotenv()
GOOGLE_API_KEY=st.secrets["GOOGLE_API_KEY"]
#GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

def get_prompt_financial():
    return '''Extract following financial data from the article:
- Company Name (official full name)
- CEO (full name)
- Market Capitalization (latest)
- Financial Quarter (format: QX FYXX)
- Stock Symbol (official exchange code)
- Revenue (convert to USD $ using 1 USD = 83 INR)
- Net Income (convert to USD $ using 1 USD = 83 INR)

Return STRICT JSON format:
{
    "Company": "Reliance Industries Limited",
    "CEO": "Mukesh Dhirubhai Ambani",
    "Market Capital": "$255.8 billion",
    "Quarter": "Q3 FY2024",
    "Stock Name": "RELIANCE.BSE",
    "Revenue": "$32.05 billion",
    "Net income": "$2.23 billion"
}

Rules:
1. Convert all currency to USD
2. Format numbers as "$X.XX billion/million"
3. Maintain field order exactly
4. For missing values please search web and fill


News Article:
'''

def extract_financial_data(text):
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    prompt = get_prompt_financial() + text
    
    try:
        response = model.generate_content(prompt)
        content = response.text
        
        # Clean JSON response
        content = content.replace('```json', '').replace('```', '').strip()
        data = json.loads(content)
        
        # Create ordered DataFrame
        return pd.DataFrame([{
            "Company": data.get("Company", "N/A"),
            "CEO": data.get("CEO", "N/A"),
            "Market Capital": data.get("Market Capital", "N/A"),
            "Quarter": data.get("Quarter", "N/A"),
            "Stock Name": data.get("Stock Name", "N/A"),
            "Revenue": data.get("Revenue", "N/A"),
            "Net income": data.get("Net income", "N/A")
        }])
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return pd.DataFrame([{
            "Company": "N/A", 
            "CEO": "N/A",
            "Market Capital": "N/A",
            "Quarter": "N/A",
            "Stock Name": "N/A",
            "Revenue": "N/A",
            "Net income": "N/A"
        }])

if __name__ == "__main__":
    article_text = '''Reliance Industries Ltd reported a 7% year-on-year (YoY) increase in consolidated net profit to Rs 18,540 crore for Q3, with revenues from operations rising 7% YoY to Rs 2.43 lakh crore. Reliance Jio Infocomm reported a 26% rise in consolidated net profit for the December quarter, reaching Rs 6,861 crore, up from Rs 5,447 crore in the same period last year. It posted a 12% year-on-year increase in average revenue per user, reaching Rs 203.3.'''
    
    df = extract_financial_data(article_text)
    print(df.to_string(index=False))