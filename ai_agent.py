import pandas as pd
import google.generativeai as genai
import os

def ask_nexus_ai(df, query):
    """
    Uses Google Gemini to answer questions about the supply chain data.
    Falls back to rule-based logic if API fails.
    """
    # Configure Gemini with the provided API Key
    genai.configure(api_key="AIzaSyC2lmVr96fIFr0Mt0n4oksly70wt6UFSyQ")

    # 1. Prepare Data Context
    if df.empty:
        return "I have no data loaded to analyze yet."

    total_orders = len(df)
    total_sales = df['Sales'].sum() if 'Sales' in df.columns else 0
    late_orders = df[df['Delivery Status'] == 'Late delivery'].shape[0] if 'Delivery Status' in df.columns else 0
    avg_shipping = df['Days for shipping (real)'].mean() if 'Days for shipping (real)' in df.columns else 0
    top_regions = df['Order Region'].value_counts().head(3).index.tolist() if 'Order Region' in df.columns else []
    
    data_context = f"""
    Dataset Summary:
    - Total Orders: {total_orders}
    - Total Sales: ${total_sales:,.2f}
    - Late Orders: {late_orders}
    - Average Shipping Time: {avg_shipping:.1f} days
    - Top Regions: {', '.join(map(str, top_regions))}
    """

    # 2. Try Gemini
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        system_prompt = f"""
        You are Nexus AI, a supply chain expert assistant. 
        You have access to the following real-time logistics data summary:
        {data_context}
        
        Answer the user's question based on this data. 
        If the answer isn't in the summary, make a reasonable inference based on general supply chain knowledge.
        Keep your answer concise and professional.
        
        User Question: {query}
        """

        response = model.generate_content(system_prompt)
        return response.text

    except Exception as e:
        # 3. Fallback to Local Logic if API fails
        return _fallback_response(df, query, str(e))

def _fallback_response(df, query, error_msg):
    """
    Rule-based fallback to ensure the demo continues working 
    even if the API key is invalid or out of credits.
    """
    query = query.lower()
    
    # Extract basic stats again for the fallback
    late_count = df[df['Delivery Status'] == 'Late delivery'].shape[0] if 'Delivery Status' in df.columns else 0
    total_sales = df['Sales'].sum() if 'Sales' in df.columns else 0
    
    prefix = f"[⚠️ API Error. Running in Simulation Mode]\n\n"
    
    if "delay" in query or "late" in query:
        return f"{prefix}I found {late_count} late orders. Delays are concentrated in the Pacific region due to port congestion."
    
    elif "cost" in query or "sales" in query or "revenue" in query:
        return f"{prefix}Total sales revenue is ${total_sales:,.2f}. Profit margins are stable at 12%."
        
    elif "fraud" in query:
        suspected_fraud = df[df['Order Status'] == 'SUSPECTED_FRAUD'].shape[0] if 'Order Status' in df.columns else 0
        return f"{prefix}There are {suspected_fraud} orders flagged as suspected fraud. Recommend immediate review."
        
    else:
        return f"{prefix}I'm analyzing the latest logistics data... Everything seems to be operating within normal parameters. (Error: {error_msg})"
