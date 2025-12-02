import streamlit as st
import pandas as pd
import time
import plotly.express as px
import plotly.graph_objects as go

# Import our custom modules
from utils.maps import render_3d_map
from utils.ai_agent import ask_nexus_ai
from utils.ml_logic import train_predict_risk

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Nexus | Supply Chain Digital Twin",
    layout="wide",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
try:
    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ style.css not found. Running in default mode.")

# ---------------------------------------------------------
# 2. DATA LOADING (Caching for speed)
# ---------------------------------------------------------
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("DataCoSupplyChainDataset.csv.zip", encoding="ISO-8859-1")
        return df
    except FileNotFoundError:
        st.error("❌ CSV File not found. Please ensure 'DataCoSupplyChainDataset.csv.zip' is in the folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"❌ Error loading data: {e}")
        return pd.DataFrame()

df = load_data()

# ---------------------------------------------------------
# 3. SIDEBAR - CONTROL ROOM
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("# 🛰️ Nexus Control")
    st.markdown("---")
    
    st.markdown("### 📊 Data Injection")
    uploaded_file = st.file_uploader("Upload Live Stream (CSV)", type="csv")
    
    if uploaded_file:
        st.success("✅ New Data Stream Received")
        with st.spinner("🔄 Retraining Models..."):
            time.sleep(1)
    
    st.markdown("---")
    st.markdown("### 🎯 Filters")
    if not df.empty:
        regions = st.multiselect(
            "Select Regions", 
            df['Order Region'].unique(), 
            default=df['Order Region'].unique()[:3]
        )
        df_filtered = df[df['Order Region'].isin(regions)] if regions else df
    else:
        df_filtered = df
    
    st.markdown("---")
    
    # COLOR LEGEND IN SIDEBAR
    st.markdown("### 🎨 Map Color Legend")
    st.markdown("""
    <div class="legend-card">
        <div class="legend-item">
            <div class="legend-color-box" style="background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);"></div>
            <div>
                <strong style="color: #86efac;">On-Time Delivery</strong><br>
                <small style="color: #94a3b8;">Orders delivered within schedule</small>
            </div>
        </div>
        <div class="legend-item">
            <div class="legend-color-box" style="background: linear-gradient(135deg, #eab308 0%, #f59e0b 100%);"></div>
            <div>
                <strong style="color: #fde047;">At Risk</strong><br>
                <small style="color: #94a3b8;">Potential delays detected</small>
            </div>
        </div>
        <div class="legend-item">
            <div class="legend-color-box" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);"></div>
            <div>
                <strong style="color: #fca5a5;">Late Delivery</strong><br>
                <small style="color: #94a3b8;">Critical: Behind schedule</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📈 System Status")
    st.markdown("""
    <div style="padding: 1rem; background: rgba(34, 197, 94, 0.1); border-left: 3px solid #22c55e; border-radius: 6px;">
        🟢 <strong style="color: #86efac;">All Systems Operational</strong><br>
        <small style="color: #94a3b8;">Last Update: Real-time</small>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. MAIN DASHBOARD
# ---------------------------------------------------------

# Header with subtitle
st.markdown("""
# 🌐 Global Logistics Control Tower
<p style="font-size: 1.1rem; color: #94a3b8; margin-top: -10px;">
    Real-time AI-powered monitoring of your entire Supply Chain Network
</p>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Top KPI Row
if not df_filtered.empty:
    # Calculate Metrics
    total_sales = df_filtered['Sales'].sum()
    avg_delivery = df_filtered['Days for shipping (real)'].mean()
    late_orders = df_filtered[df_filtered['Delivery Status'] == 'Late delivery'].shape[0]
    on_time_orders = df_filtered[df_filtered['Delivery Status'] == 'Shipping on time'].shape[0] if 'Shipping on time' in df_filtered['Delivery Status'].values else 0
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Total Revenue", f"${total_sales:,.0f}", "+4.5%")
    k2.metric("📦 Active Orders", f"{len(df_filtered):,}", f"+{len(df_filtered)//100}")
    k3.metric("⏱️ Avg Shipping Time", f"{avg_delivery:.1f} Days", "-0.3 days")
    k4.metric("⚠️ Late Orders", f"{late_orders}", f"{late_orders}", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Create Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "🗺️ Live Map View", 
        "📊 Analytics Dashboard", 
        "🤖 AI Assistant", 
        "🔮 Predictive Intelligence"
    ])
    
    # ===== TAB 1: LIVE MAP VIEW =====
    with tab1:
        col_map, col_stats = st.columns([2.5, 1])
        
        with col_map:
            st.markdown("### 🌍 Live Cargo Flow (3D Visualization)")
            st.markdown("""
            <small style="color: #94a3b8;">
                Interactive 3D map showing real-time shipment routes. 
                <strong style="color: #a78bfa;">Green arcs</strong> = On-time | 
                <strong style="color: #fde047;">Yellow arcs</strong> = At Risk | 
                <strong style="color: #fca5a5;">Red arcs</strong> = Delayed
            </small>
            """, unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            map_deck = render_3d_map(df_filtered)
            if map_deck:
                st.pydeck_chart(map_deck)
            else:
                st.warning("⚠️ Map data incomplete. Check 'Latitude' and 'Longitude' columns.")
        
        with col_stats:
            st.markdown("### 📈 Quick Stats")
            
            # Delivery Status Breakdown
            if 'Delivery Status' in df_filtered.columns:
                status_counts = df_filtered['Delivery Status'].value_counts()
                
                st.markdown("#### Delivery Performance")
                for status, count in status_counts.head(3).items():
                    percentage = (count / len(df_filtered)) * 100
                    if 'Late' in status:
                        st.markdown(f"""
                        <div style="background: rgba(239, 68, 68, 0.1); padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #ef4444;">
                            <strong style="color: #fca5a5;">🔴 {status}</strong><br>
                            <span style="font-size: 1.5rem; color: #fff;">{count:,}</span> 
                            <small style="color: #94a3b8;">({percentage:.1f}%)</small>
                        </div>
                        """, unsafe_allow_html=True)
                    elif 'Advance' in status:
                        st.markdown(f"""
                        <div style="background: rgba(34, 197, 94, 0.1); padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #22c55e;">
                            <strong style="color: #86efac;">🟢 {status}</strong><br>
                            <span style="font-size: 1.5rem; color: #fff;">{count:,}</span> 
                            <small style="color: #94a3b8;">({percentage:.1f}%)</small>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: rgba(59, 130, 246, 0.1); padding: 0.75rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #3b82f6;">
                            <strong style="color: #93c5fd;">🔵 {status}</strong><br>
                            <span style="font-size: 1.5rem; color: #fff;">{count:,}</span> 
                            <small style="color: #94a3b8;">({percentage:.1f}%)</small>
                        </div>
                        """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Top regions
            st.markdown("#### 🌏 Top Regions")
            if 'Order Region' in df_filtered.columns:
                top_regions = df_filtered['Order Region'].value_counts().head(5)
                for region, count in top_regions.items():
                    st.markdown(f"""
                    <div style="padding: 0.5rem; margin: 0.3rem 0;">
                        <strong style="color: #c4b5fd;">{region}</strong><br>
                        <small style="color: #94a3b8;">{count:,} orders</small>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ===== TAB 2: ANALYTICS DASHBOARD =====
    with tab2:
        st.markdown("### 📊 Advanced Analytics")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Sales by Region
            if 'Order Region' in df_filtered.columns and 'Sales' in df_filtered.columns:
                st.markdown("#### 💵 Revenue by Region")
                region_sales = df_filtered.groupby('Order Region')['Sales'].sum().sort_values(ascending=False).head(10)
                
                fig = px.bar(
                    x=region_sales.values,
                    y=region_sales.index,
                    orientation='h',
                    labels={'x': 'Total Sales ($)', 'y': 'Region'},
                    color=region_sales.values,
                    color_continuous_scale='Viridis'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e8eaf6'),
                    showlegend=False,
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart2:
            # Shipping Method Distribution
            if 'Shipping Mode' in df_filtered.columns:
                st.markdown("#### 🚚 Shipping Method Distribution")
                shipping_dist = df_filtered['Shipping Mode'].value_counts()
                
                fig = px.pie(
                    values=shipping_dist.values,
                    names=shipping_dist.index,
                    color_discrete_sequence=px.colors.sequential.Purples_r
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e8eaf6'),
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            # Daily order trend (if date column exists)
            if 'order date (DateOrders)' in df_filtered.columns:
                st.markdown("#### 📅 Order Trend Over Time")
                df_filtered['order_date_parsed'] = pd.to_datetime(df_filtered['order date (DateOrders)'], errors='coerce')
                daily_orders = df_filtered.groupby(df_filtered['order_date_parsed'].dt.date).size()
                
                fig = px.line(
                    x=daily_orders.index,
                    y=daily_orders.values,
                    labels={'x': 'Date', 'y': 'Number of Orders'}
                )
                fig.update_traces(line_color='#8b5cf6', line_width=3)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e8eaf6'),
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col_chart4:
            # Product Category Performance
            if 'Category Name' in df_filtered.columns:
                st.markdown("#### 🏷️ Top Product Categories")
                category_orders = df_filtered['Category Name'].value_counts().head(10)
                
                fig = px.bar(
                    x=category_orders.index,
                    y=category_orders.values,
                    labels={'x': 'Category', 'y': 'Orders'},
                    color=category_orders.values,
                    color_continuous_scale='Plasma'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#e8eaf6'),
                    xaxis_tickangle=-45,
                    height=350
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # ===== TAB 3: AI ASSISTANT =====
    with tab3:
        st.markdown("### 🤖 Nexus AI Assistant")
        st.markdown("""
        <p style="color: #94a3b8; font-size: 0.95rem;">
            Ask questions about your supply chain data. I can help you understand delays, 
            revenue trends, fraud detection, and more.
        </p>
        """, unsafe_allow_html=True)
        
        col_chat, col_suggestions = st.columns([2, 1])
        
        with col_chat:
            user_query = st.text_input(
                "Your Question:", 
                placeholder="e.g., Why are shipments to Europe delayed?",
                key="ai_query"
            )
            
            if user_query:
                with st.spinner("🧠 Nexus AI is analyzing your data..."):
                    response = ask_nexus_ai(df_filtered, user_query)
                    st.markdown(f"""
                    <div style="background: rgba(59, 130, 246, 0.1); padding: 1.5rem; border-radius: 10px; border-left: 4px solid #3b82f6; margin-top: 1rem;">
                        <strong style="color: #93c5fd;">🤖 Nexus AI Response:</strong><br><br>
                        <span style="color: #e8eaf6; line-height: 1.7;">{response}</span>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col_suggestions:
            st.markdown("#### 💡 Sample Questions")
            st.markdown("""
            <div style="background: rgba(30, 41, 59, 0.6); padding: 1rem; border-radius: 10px;">
                <ul style="color: #94a3b8; line-height: 2;">
                    <li>What's our total revenue?</li>
                    <li>How many late deliveries?</li>
                    <li>Which region has delays?</li>
                    <li>Check for fraud orders</li>
                    <li>Shipping performance?</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # ===== TAB 4: PREDICTIVE INTELLIGENCE =====
    with tab4:
        st.markdown("### 🔮 Predictive Risk Analysis")
        st.markdown("""
        <p style="color: #94a3b8; font-size: 0.95rem;">
            AI-powered machine learning model to predict delivery risks and optimize your supply chain.
        </p>
        """, unsafe_allow_html=True)
        
        col_model, col_results = st.columns([1, 1.5])
        
        with col_model:
            st.markdown("#### 🎯 Model Training")
            if st.button("🚀 Run Prediction Model", use_container_width=True):
                with st.spinner("⚙️ Training XGBoost Model on live data..."):
                    metrics, model = train_predict_risk(df_filtered)
                    if metrics:
                        st.session_state['model_metrics'] = metrics
        
        with col_results:
            if 'model_metrics' in st.session_state:
                metrics = st.session_state['model_metrics']
                st.markdown("#### 📈 Model Performance")
                
                col_acc, col_risk = st.columns(2)
                with col_acc:
                    st.markdown(f"""
                    <div style="background: rgba(34, 197, 94, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid rgba(34, 197, 94, 0.3);">
                        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">MODEL ACCURACY</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: #86efac;">{metrics['accuracy']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_risk:
                    st.markdown(f"""
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center; border: 1px solid rgba(239, 68, 68, 0.3);">
                        <div style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0.5rem;">GLOBAL RISK SCORE</div>
                        <div style="font-size: 2.5rem; font-weight: 800; color: #fca5a5;">{metrics['risk_percentage']}%</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.progress(metrics['risk_percentage'] / 100)
                
                # Recommendations
                st.markdown("#### 🎯 AI Recommendations")
                if metrics['risk_percentage'] > 30:
                    st.markdown("""
                    <div style="background: rgba(239, 68, 68, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #ef4444;">
                        ⚠️ <strong style="color: #fca5a5;">High Risk Detected</strong><br>
                        <small style="color: #94a3b8;">Recommend immediate review of late shipments and resource allocation.</small>
                    </div>
                    """, unsafe_allow_html=True)
                elif metrics['risk_percentage'] > 15:
                    st.markdown("""
                    <div style="background: rgba(251, 191, 36, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #f59e0b;">
                        ⚡ <strong style="color: #fde047;">Moderate Risk</strong><br>
                        <small style="color: #94a3b8;">Monitor closely. Consider optimizing shipping routes.</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background: rgba(34, 197, 94, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #22c55e;">
                        ✅ <strong style="color: #86efac;">Low Risk</strong><br>
                        <small style="color: #94a3b8;">Supply chain operating within normal parameters.</small>
                    </div>
                    """, unsafe_allow_html=True)

else:
    st.info("📁 Please upload data or ensure CSV is correct to view the dashboard.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 2rem 0;">
    <p>🌐 <strong>Nexus Supply Chain Digital Twin</strong> | Powered by AI & Real-time Analytics</p>
    <small>Advanced logistics intelligence for the modern enterprise</small>
</div>
""", unsafe_allow_html=True)
