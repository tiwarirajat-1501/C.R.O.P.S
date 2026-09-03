# 🌱 C.R.O.P.S. — Climate & Resource-Optimized Predictive System

A state-of-the-art **AI Crop Recommendation, Soil Health, & Precision Agronomic Advisory Platform** built with Python, Scikit-Learn, and Streamlit.

---

## 🌟 Key Features

1. **High-Precision Machine Learning Backbone**:
   - Trained on 2,200 agro-ecological records across 22 major agricultural crops.
   - Evaluates **Random Forest Classifier (99.55% test accuracy)** against **XGBoost Classifier (98.86%)**.
   - Standardized feature space spanning Nitrogen (N), Phosphorus (P), Potassium (K), Soil pH, Temperature, Humidity, and Seasonal Rainfall.

2. **Commercial 50kg Bag Sizing & Land Area Scaler**:
   - Custom farm land size configuration (Acres / Hectares).
   - Translates theoretical nutrient gaps into exact quantities of **commercial 50kg bags** of **Urea (46% N)**, **DAP (18-46-0)**, and **MOP (60% K2O)**.
   - Stage-by-stage split application timetable (Basal at sowing, 30-day vegetative top dressing, flowering stage).

3. **Crop Economics & Financial ROI Engine**:
   - Projects estimated yield in Quintals, gross market revenue (based on Government MSP / Mandi rates), and cultivation costs.
   - Computes expected net profit and Return on Investment (ROI %) with a comparative side-by-side analysis for the Top-3 recommended crops.

4. **Smart Irrigation & Seasonal Water Management**:
   - Crop duration, seasonal classification (Kharif, Rabi, Zaid, Perennial), and water need tiers.
   - Analyzes precipitation deficits/surpluses to prescribe supplemental irrigation cycles.
   - Recommends modern water-saving technologies (Precision Drip, Micro-Sprinklers, Alternate Wetting & Drying).

5. **Explainable AI (XAI) & Model Transparency**:
   - Gini feature importance breakdown.
   - Ensemble model benchmark comparison.
   - Interactive 22×22 multiclass confusion matrix heatmap.

6. **Offline-Resilient Climate Integration**:
   - Connects to live OpenWeatherMap API when online.
   - Seamlessly falls back to pre-compiled agro-climatic profiles for major farming zones (Punjab, Maharashtra, Uttar Pradesh, Karnataka, Kerala, West Bengal, Gujarat, etc.) for bulletproof live exhibition demos.

---

## 🚀 Quick Start & Exhibition Launch

### 1. One-Click Launch (Windows)
Double-click `run_app.bat` to launch the **3D Modern Web Platform** immediately at **`http://localhost:5000`**.

### 2. Manual Command Line Launch
```bash
# Launch the 3D Modern Web Application (Default)
python server.py
# Open: http://localhost:5000

# Or launch the Streamlit Dashboard
streamlit run app.py
# Open: http://localhost:8501
```

---

## 🏗️ Project Structure

```
C.R.O.P.S/
├── frontend/                      # Web UI Assets
│   ├── index.html                 # 3D Web UI structure
│   ├── style.css                  # Clean 3D modern dark design system
│   └── app.js                     # 3D interactive logic & API engine
├── backend/                       # Backend Python (.py) Files Only
│   ├── server.py                  # Production Python REST API & web server
│   ├── agronomic_data.py          # Economics & benchmarks knowledge base
│   ├── weather_service.py         # Weather API & regional fallback presets
│   ├── report_generator.py        # Printable Soil Health Card generator
│   ├── train_model.py             # ML training pipeline (Random Forest & XGBoost)
│   └── app.py                     # Alternate Streamlit dashboard
├── models/                        # ML Model Artifacts (Root)
│   ├── crop_model.pkl             # Trained Random Forest Classifier (99.55% acc)
│   ├── scaler.pkl                 # StandardScaler fitted on continuous features
│   ├── label_encoder.pkl          # LabelEncoder for crop target classes
│   ├── crop_benchmarks.json       # Ideal N-P-K, pH & climate thresholds per crop
│   └── metrics.json               # Evaluation metrics, importances & confusion matrix
├── data/                          # Dataset (Root)
│   └── crop_recommendation.csv    # 2,200 agronomic records across 22 crops
├── server.py                      # Root launcher delegating to backend/server.py
├── run_app.bat                    # 1-Click Windows desktop launcher
└── requirements.txt               # Project dependencies
```
