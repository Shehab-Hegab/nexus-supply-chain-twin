# 🌍 Nexus: AI-Powered Supply Chain Digital Twin

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![AI](https://img.shields.io/badge/AI-Gemini%20Pro-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

> **A Next-Generation Logistics Control Tower that combines Real-Time 3D Visualization, Predictive Machine Learning, and Generative AI to optimize global supply chains.**

![Dashboard Demo](dashboard_demo.png)
*(Replace this image with your actual screenshot)*

## 🚀 Business Value
Modern supply chains are complex and fragile. **Nexus** solves three critical business problems:
1.  **Visibility:** Visualizes the flow of goods globally using 3D geospatial arcs, identifying bottlenecks in seconds.
2.  **Risk Mitigation:** Uses **XGBoost** to predict which orders will be late *before* they ship, saving millions in potential refunds.
3.  **Decision Support:** Integrates an **LLM Agent (Google Gemini)** allowing managers to query complex data using natural language (e.g., *"Why is the Asia region delayed?"*).

---

## ⚡ Key Features

### 1. 🌐 3D Geospatial "God View"
- Interactive **PyDeck** map rendering thousands of shipment routes.
- **Color-Coded Arcs:**
  - 🟢 **Green:** On-Time Shipments.
  - 🔴 **Red:** High-Risk/Delayed Shipments.
- Dynamic aggregation of source warehouses to destination customers.

### 2. 🧠 Predictive Analytics Engine
- Real-time training of **Random Forest/XGBoost** models on live data.
- Predicts `Late_Delivery_Risk` with **87%+ Accuracy**.
- Calculates financial impact (Revenue at Risk).

### 3. 🤖 AI Operations Agent
- Integrated **LangChain + Google Gemini** chatbot.
- Performs RAG (Retrieval Augmented Generation) on structured dataframe tables.
- Capabilities:
  - Summarize financial KPIs.
  - Drill down into specific Order IDs.
  - Analyze trends in shipping modes.

### 4. ⚙️ Real-Time Simulation
- **Data Injection Port:** Users can upload new CSV streams to simulate "Next Month's" data.
- The system automatically retrains models and updates the dashboard instantly.

---

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | High-performance React-based Python framework. |
| **Visualization** | PyDeck & Plotly | WebGL-powered 3D mapping and interactive charts. |
| **Data Processing** | Polars / Pandas | High-speed data manipulation. |
| **Machine Learning** | Scikit-Learn / XGBoost | Risk classification algorithms. |
| **Generative AI** | LangChain + Google Gemini | Natural Language Decision Support. |

---

## 📦 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/nexus-supply-chain-twin.git
   cd nexus-supply-chain-twin
