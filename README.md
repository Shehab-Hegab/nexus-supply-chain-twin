# 🌍 Nexus: AI-Powered Supply Chain Digital Twin

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-red)
![AI](https://img.shields.io/badge/AI-Gemini%201.5%20Flash-orange)
![Status](https://img.shields.io/badge/Status-Live-success)

> **A Next-Generation Logistics Control Tower that combines Real-Time 3D Visualization, Predictive Machine Learning, and Generative AI to optimize global supply chains.**

📊 Dataset: https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis

## 📸 Application Gallery
*(Real-time screenshots of the Nexus System)*

![Dashboard Demo](dashboard_demo.png)
<img width="1862" height="992" alt="Main Dashboard View" src="https://github.com/user-attachments/assets/99aedacd-f1b6-4d12-abce-797e46230b9a" />
<img width="1856" height="992" alt="3D Map Visualization" src="https://github.com/user-attachments/assets/0b679701-f6a2-4457-a75b-56baaf372c4b" />
<img width="1852" height="993" alt="Predictive Analytics" src="https://github.com/user-attachments/assets/ad5902bc-33b5-447a-8d30-e90e11a84aca" />
<img width="1847" height="642" alt="AI Agent Interface" src="https://github.com/user-attachments/assets/3f3758fb-d82e-43af-872f-6720597fda8d" />
<img width="908" height="642" alt="Risk Analysis" src="https://github.com/user-attachments/assets/72890975-78fb-49ea-b73b-ff610c115ea4" />
<img width="1820" height="617" alt="Data Injection Port" src="https://github.com/user-attachments/assets/84041e28-40c6-4bcf-bf03-378416360220" />
<img width="1523" height="811" alt="KPI Metrics" src="https://github.com/user-attachments/assets/99bbaaf6-c242-441b-aea7-0b44fc507b28" />
<img width="1842" height="987" alt="Full System View" src="https://github.com/user-attachments/assets/846aafaa-6748-48b9-be75-e8036b0da1be" />
<img width="1840" height="991" alt="Geospatial Tracking" src="https://github.com/user-attachments/assets/602611da-d9f2-4b46-94de-af16b268872a" />
<img width="1841" height="892" alt="Real-time Chat" src="https://github.com/user-attachments/assets/258da009-e100-4937-a471-c553bddb50f4" />

---

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
