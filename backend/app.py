"""
C.R.O.P.S. — Climate & Resource-Optimized Predictive System
Production-grade AI Crop Recommendation & Soil Health Platform
Enhanced with Land Scaler, Commercial Fertilizer Sizing, Crop Economics, & Smart Irrigation.
"""

import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import weather_service
import agronomic_data
import report_generator

# -----------------------------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="C.R.O.P.S. | AI Precision Agriculture",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling (Emerald Agricultural Theme + Glassmorphism)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 50%, #047857 100%);
        color: #ffffff;
        padding: 24px 30px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(6, 78, 59, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-header h1 {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin: 0;
        color: #f0fdf4;
    }
    
    .main-header p {
        font-size: 1.05rem;
        color: #a7f3d0;
        margin-top: 6px;
        margin-bottom: 0;
    }
    
    .metric-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 600;
        color: #ecfdf5;
        margin-right: 8px;
        margin-top: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .crop-card {
        background: linear-gradient(145deg, #ffffff 0%, #f0fdf4 100%);
        border: 1px solid #bbf7d0;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.08);
        margin-bottom: 20px;
    }
    
    .prescription-box {
        background: #f8fafc;
        border-left: 5px solid #059669;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 12px;
    }
    
    .economic-card {
        background: #ffffff;
        border-radius: 14px;
        padding: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
    }
    
    .water-box {
        background: #f0fdfa;
        border-left: 5px solid #0d9488;
        border-radius: 10px;
        padding: 16px 20px;
        margin-top: 12px;
    }
    
    .tag-low {
        background-color: #fee2e2;
        color: #991b1b;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .tag-optimal {
        background-color: #dcfce7;
        color: #166534;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .tag-high {
        background-color: #fef3c7;
        color: #92400e;
        padding: 3px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.8rem;
    }
    
    .bag-badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0369a1;
        padding: 4px 10px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
if not os.path.exists(MODELS_DIR):
    MODELS_DIR = "models"

@st.cache_resource
def load_ml_assets():
    model_path = os.path.join(MODELS_DIR, "crop_model.pkl")
    scaler_path = os.path.join(MODELS_DIR, "scaler.pkl")
    encoder_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    
    if not (os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(encoder_path)):
        return None, None, None
        
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    encoder = joblib.load(encoder_path)
    return model, scaler, encoder

@st.cache_data
def load_metadata():
    metrics_path = os.path.join(MODELS_DIR, "metrics.json")
    benchmarks_path = os.path.join(MODELS_DIR, "crop_benchmarks.json")
    
    metrics = None
    benchmarks = None
    
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)
            
    if os.path.exists(benchmarks_path):
        with open(benchmarks_path, "r") as f:
            benchmarks = json.load(f)
            
    return metrics, benchmarks

model, scaler, encoder = load_ml_assets()
metrics, benchmarks = load_metadata()

# Crop icons dictionary for visual enhancement
CROP_ICONS = {
    "rice": "🌾", "maize": "🌽", "chickpea": "🌱", "kidneybeans": "🫘",
    "pigeonpeas": "🌿", "mothbeans": "🫘", "mungbean": "🌱", "blackgram": "🫘",
    "lentil": "🍲", "pomegranate": "🍎", "banana": "🍌", "mango": "🥭",
    "grapes": "🍇", "watermelon": "🍉", "muskmelon": "🍈", "apple": "🍏",
    "orange": "🍊", "papaya": "🥭", "coconut": "🥥", "cotton": "🧶",
    "jute": "🧵", "coffee": "☕"
}

# Crop Category Classification
CROP_CATEGORIES = {
    "rice": "Cereals & Grains", "maize": "Cereals & Grains",
    "chickpea": "Pulses & Legumes", "kidneybeans": "Pulses & Legumes",
    "pigeonpeas": "Pulses & Legumes", "mothbeans": "Pulses & Legumes",
    "mungbean": "Pulses & Legumes", "blackgram": "Pulses & Legumes",
    "lentil": "Pulses & Legumes",
    "pomegranate": "Horticulture & Fruits", "banana": "Horticulture & Fruits",
    "mango": "Horticulture & Fruits", "grapes": "Horticulture & Fruits",
    "watermelon": "Horticulture & Fruits", "muskmelon": "Horticulture & Fruits",
    "apple": "Horticulture & Fruits", "orange": "Horticulture & Fruits",
    "papaya": "Horticulture & Fruits",
    "coconut": "Plantation & Cash Crops", "cotton": "Fiber & Cash Crops",
    "jute": "Fiber & Cash Crops", "coffee": "Plantation & Cash Crops"
}

# -----------------------------------------------------------------------------
# 3. SIDEBAR CONTROLS & EXHIBITION PRESETS
# -----------------------------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=400&q=80", use_container_width=True)
st.sidebar.title("🌱 Exhibition Control")
st.sidebar.caption("Real-Time Climate, Soil & Farm Area Engine")

# Exhibition Presets
EXHIBITION_PRESETS = {
    "Custom / Manual": None,
    "Indo-Gangetic Alluvial (Rice / Jute)": {
        "N": 85, "P": 50, "K": 40, "ph": 6.6, "temp": 26.0, "humidity": 82.0, "rain": 210.0,
        "region": "West Bengal (Hooghly / Burdwan)"
    },
    "Deccan Black Cotton Soil (Cotton)": {
        "N": 120, "P": 45, "K": 20, "ph": 6.8, "temp": 24.5, "humidity": 80.0, "rain": 80.0,
        "region": "Maharashtra (Nashik / Vidarbha)"
    },
    "Semi-Arid Dryland (Mothbeans)": {
        "N": 20, "P": 55, "K": 20, "ph": 6.2, "temp": 28.0, "humidity": 55.0, "rain": 50.0,
        "region": "Gujarat (Anand / Saurashtra)"
    },
    "Southern Humid Coastal (Coconut)": {
        "N": 22, "P": 18, "K": 32, "ph": 6.0, "temp": 27.5, "humidity": 95.0, "rain": 175.0,
        "region": "Kerala (Wayanad / Palakkad)"
    },
    "Sub-Temperate Hill Orchard (Apple)": {
        "N": 22, "P": 138, "K": 198, "ph": 5.9, "temp": 22.0, "humidity": 92.0, "rain": 112.0,
        "region": "Punjab (Ludhiana)"
    },
    "High Plateau Cash Crop (Coffee)": {
        "N": 100, "P": 30, "K": 30, "ph": 6.8, "temp": 25.5, "humidity": 68.0, "rain": 160.0,
        "region": "Karnataka (Bengaluru / Mandya)"
    }
}

selected_preset = st.sidebar.selectbox(
    "⚡ Quick Exhibition Demo Presets:",
    list(EXHIBITION_PRESETS.keys()),
    index=1  # Default to Gangetic Alluvial for instant impressive showcase
)

preset_vals = EXHIBITION_PRESETS[selected_preset]

# Weather / Regional Synchronizer
st.sidebar.markdown("---")
st.sidebar.subheader("⛅ Climate Synchronizer")
available_regions = weather_service.get_available_regions()

default_region_idx = 0
if preset_vals and preset_vals.get("region") in available_regions:
    default_region_idx = available_regions.index(preset_vals["region"])

selected_region = st.sidebar.selectbox("Agro-Climatic Zone:", available_regions, index=default_region_idx)

api_key_input = st.sidebar.text_input("OpenWeather API Key (Optional):", type="password", help="Leave blank to use pre-compiled agronomic climate database")

if st.sidebar.button("🔄 Sync Weather to Sliders"):
    weather_info = weather_service.get_weather(selected_region, api_key_input)
    st.session_state["weather_temp"] = weather_info["temperature"]
    st.session_state["weather_humidity"] = weather_info["humidity"]
    st.session_state["weather_rain"] = weather_info["rainfall"]
    st.sidebar.success(f"Synced {weather_info['region']} ({weather_info['source']})")

# Determine default slider values
def get_val(key, default_val):
    if preset_vals is not None and key in preset_vals:
        return preset_vals[key]
    return default_val

initial_n = get_val("N", 90)
initial_p = get_val("P", 42)
initial_k = get_val("K", 43)
initial_ph = get_val("ph", 6.5)
initial_temp = st.session_state.get("weather_temp", get_val("temp", 26.0))
initial_humidity = st.session_state.get("weather_humidity", get_val("humidity", 80.0))
initial_rain = st.session_state.get("weather_rain", get_val("rain", 200.0))

# Farm Land Area Configuration in Sidebar
st.sidebar.markdown("---")
st.sidebar.subheader("📐 Farm Land Size")
col_land1, col_land2 = st.sidebar.columns([1.6, 1.2])
with col_land1:
    farm_area = st.number_input("Land Size:", min_value=0.25, max_value=500.0, value=2.5, step=0.5)
with col_land2:
    area_unit = st.selectbox("Unit:", ["Acres", "Hectares"], index=0)

# Convert land area to both Acres and Hectares
if area_unit == "Acres":
    total_acres = float(farm_area)
    total_hectares = float(farm_area) / 2.47105
else:
    total_hectares = float(farm_area)
    total_acres = float(farm_area) * 2.47105

st.sidebar.caption(f"📍 Sizing: **{total_acres:.2f} Acres** ({total_hectares:.2f} Hectares)")

# Farmer Identification for Soil Health Card
st.sidebar.markdown("---")
st.sidebar.subheader("👨‍🌾 Farmer Identification")
farmer_name = st.sidebar.text_input("Farmer Name:", value="Ramesh Kumar", help="Printed on official Soil Health Card")
field_id = st.sidebar.text_input("Plot / Field ID:", value="Plot #4-B", help="Field identifier printed on official Soil Health Card")

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip for Judges**: Select any preset above to instantly demonstrate different crop suitability, soil nutrient gaps, fertilizer schedules, economics, and irrigation.")

# -----------------------------------------------------------------------------
# 4. HEADER & TOP BANNER
# -----------------------------------------------------------------------------
st.markdown(f"""
<div class="main-header">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <h1>🌱 C.R.O.P.S.</h1>
            <p>Climate & Resource-Optimized Predictive System — Precision Agronomic & Economic Intelligence</p>
        </div>
        <div>
            <span class="metric-badge">🎯 Model Accuracy: 99.55%</span>
            <span class="metric-badge">🌾 22 Crop Profiles</span>
            <span class="metric-badge">💰 Economic Engine</span>
            <span class="metric-badge">💧 Smart Irrigation</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Safety check for trained model
if model is None:
    st.error("⚠️ Trained ML models not found in `models/`. Please train the model to proceed.")
    if st.button("🚀 Train Model Now"):
        with st.spinner("Training Random Forest and XGBoost classifiers..."):
            import train_model
            train_model.train_pipeline()
            st.success("Model trained successfully! Please refresh the page.")
    st.stop()

# -----------------------------------------------------------------------------
# 5. TABS INTERFACE
# -----------------------------------------------------------------------------
tab_rec, tab_xai, tab_catalog, tab_arch = st.tabs([
    "🌾 AI Crop Predictor & Prescription",
    "📊 Explainable AI & Model Metrics",
    "📚 Agronomic Crop Catalog",
    "🏗️ Architecture & Specs"
])

# =============================================================================
# TAB 1: AI PREDICTOR & COMPREHENSIVE FARM ADVISORY
# =============================================================================
with tab_rec:
    st.subheader("1. Soil & Atmospheric Parameters")
    st.caption("Adjust sliders or use the sidebar exhibition presets to simulate real farm conditions.")
    
    col_soil, col_env = st.columns(2)
    
    with col_soil:
        st.markdown("#### 🧪 Soil Chemistry")
        input_n = st.slider("Nitrogen (N) [kg/ha]:", 0, 150, int(initial_n), help="Available soil nitrogen content")
        input_p = st.slider("Phosphorus (P) [kg/ha]:", 5, 150, int(initial_p), help="Available soil phosphorus content")
        input_k = st.slider("Potassium (K) [kg/ha]:", 5, 210, int(initial_k), help="Available soil potassium content")
        input_ph = st.slider("Soil pH level:", 3.5, 9.5, float(initial_ph), step=0.1, help="Acidity/Alkalinity level (Optimal: 6.0 - 7.5)")
        
    with col_env:
        st.markdown("#### ⛅ Environmental & Climate")
        input_temp = st.slider("Ambient Temperature (°C):", 8.0, 45.0, float(initial_temp), step=0.5)
        input_humidity = st.slider("Relative Humidity (%):", 10.0, 100.0, float(initial_humidity), step=1.0)
        input_rain = st.slider("Annual / Seasonal Rainfall (mm):", 20.0, 300.0, float(initial_rain), step=5.0)
        
    predict_btn = st.button("🚀 Run Precision Recommendation Engine", type="primary", use_container_width=True)
    
    # Process Prediction
    feature_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    user_features_df = pd.DataFrame(
        [[input_n, input_p, input_k, input_temp, input_humidity, input_ph, input_rain]],
        columns=feature_cols
    )
    user_features_scaled = scaler.transform(user_features_df)
    
    probabilities = model.predict_proba(user_features_scaled)[0]
    top3_indices = np.argsort(probabilities)[::-1][:3]
    top3_crops = [encoder.classes_[i] for i in top3_indices]
    top3_probs = [probabilities[i] * 100 for i in top3_indices]
    
    primary_crop = top3_crops[0]
    primary_prob = top3_probs[0]
    primary_icon = CROP_ICONS.get(primary_crop, "🌱")
    primary_category = CROP_CATEGORIES.get(primary_crop, "Standard Crop")
    
    st.markdown("---")
    st.subheader("2. Recommendation Results")
    
    res_col1, res_col2 = st.columns([1.1, 1.2])
    
    with res_col1:
        st.markdown(f"""
        <div class="crop-card">
            <div style="font-size: 3rem; margin-bottom: 8px;">{primary_icon}</div>
            <h2 style="margin: 0; color: #065f46; text-transform: capitalize;">{primary_crop}</h2>
            <p style="color: #047857; font-weight: 600; margin-top: 4px;">{primary_category}</p>
            <div style="margin-top: 15px;">
                <span style="font-size: 2.2rem; font-weight: 800; color: #064e3b;">{primary_prob:.1f}%</span>
                <span style="font-size: 0.95rem; color: #4b5563; font-weight: 500;"> Prediction Confidence</span>
            </div>
            <p style="color: #374151; font-size: 0.9rem; margin-top: 12px; line-height: 1.5;">
                Optimal ecological harmony match across Nitrogen, Phosphorus, Potassium, Humidity, and Seasonal Rainfall parameters.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    with res_col2:
        st.markdown("#### 🏆 Top-3 Suitability Probabilities")
        
        # Horizontal Bar Chart for Top 3
        fig, ax = plt.subplots(figsize=(6, 2.8))
        colors = ['#059669', '#10b981', '#6ee7b7']
        y_pos = np.arange(len(top3_crops))
        
        bars = ax.barh(y_pos, top3_probs, color=colors, height=0.55, edgecolor='none')
        ax.set_yticks(y_pos)
        ax.set_yticklabels([f"{CROP_ICONS.get(c, '🌱')} {c.capitalize()}" for c in top3_crops], fontsize=11, fontweight='600')
        ax.invert_yaxis()
        ax.set_xlabel('Model Probability (%)', fontsize=10, fontweight='600')
        ax.set_xlim(0, 105)
        ax.grid(axis='x', linestyle='--', alpha=0.3)
        
        for bar in bars:
            width = bar.get_width()
            ax.text(width + 2, bar.get_y() + bar.get_height()/2, f"{width:.1f}%", 
                    va='center', ha='left', fontsize=10, fontweight='700', color='#064e3b')
                    
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # -------------------------------------------------------------------------
    # FEATURE 1: NUTRIENT GAP & COMMERCIAL 50KG BAG CALCULATION
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader(f"3. Soil Nutrient Gap & Commercial Fertilizer Prescription")
    st.caption(f"Scaled for **{total_acres:.2f} Acres** ({total_hectares:.2f} Hectares) of **{primary_crop.capitalize()}** cultivation.")
    
    if benchmarks and primary_crop in benchmarks:
        crop_bm = benchmarks[primary_crop]
        
        # Benchmarks
        bench_n = crop_bm["N"]["mean"]
        bench_p = crop_bm["P"]["mean"]
        bench_k = crop_bm["K"]["mean"]
        bench_ph = crop_bm["ph"]["mean"]
        
        diff_n = input_n - bench_n
        diff_p = input_p - bench_p
        diff_k = input_k - bench_k
        diff_ph = input_ph - bench_ph
        
        g1, g2, g3, g4 = st.columns(4)
        
        def render_nutrient_metric(col, label, current, ideal, diff, unit="kg/ha"):
            with col:
                st.metric(
                    label=label,
                    value=f"{current} {unit}",
                    delta=f"{diff:+.1f} vs Ideal ({ideal} {unit})"
                )
                if diff < -10:
                    st.markdown('<span class="tag-low">⚠️ Deficit</span>', unsafe_allow_html=True)
                elif diff > 15:
                    st.markdown('<span class="tag-high">⚠️ Excess</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="tag-optimal">✔ Optimal</span>', unsafe_allow_html=True)
                    
        render_nutrient_metric(g1, "Nitrogen (N)", input_n, bench_n, diff_n)
        render_nutrient_metric(g2, "Phosphorus (P)", input_p, bench_p, diff_p)
        render_nutrient_metric(g3, "Potassium (K)", input_k, bench_k, diff_k)
        render_nutrient_metric(g4, "Soil pH", input_ph, bench_ph, diff_ph, unit="")
        
        # Calculate Scaled Quantities
        urea_per_ha = max(0.0, round(abs(diff_n) / 0.46, 1)) if diff_n < -5 else 0.0
        dap_per_ha = max(0.0, round(abs(diff_p) / 0.46, 1)) if diff_p < -5 else 0.0
        mop_per_ha = max(0.0, round(abs(diff_k) / 0.60, 1)) if diff_k < -5 else 0.0
        
        total_urea_kg = round(urea_per_ha * total_hectares, 1)
        total_dap_kg = round(dap_per_ha * total_hectares, 1)
        total_mop_kg = round(mop_per_ha * total_hectares, 1)
        
        urea_bags = round(total_urea_kg / 50.0, 1)
        dap_bags = round(total_dap_kg / 50.0, 1)
        mop_bags = round(total_mop_kg / 50.0, 1)
        
        st.markdown("#### 🛍️ Commercial Fertilizer Bag Requirement (50 kg Bags):")
        b1, b2, b3, b4 = st.columns(4)
        
        with b1:
            st.markdown(f"""
            <div class="economic-card">
                <div style="font-size: 0.85rem; color: #475569; font-weight: 600;">Urea (46% N)</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #0369a1; margin: 4px 0;">{urea_bags} Bags</div>
                <div style="font-size: 0.8rem; color: #64748b;">Total: {total_urea_kg} kg ({urea_per_ha} kg/ha)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with b2:
            st.markdown(f"""
            <div class="economic-card">
                <div style="font-size: 0.85rem; color: #475569; font-weight: 600;">DAP (18-46-0)</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #059669; margin: 4px 0;">{dap_bags} Bags</div>
                <div style="font-size: 0.8rem; color: #64748b;">Total: {total_dap_kg} kg ({dap_per_ha} kg/ha)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with b3:
            st.markdown(f"""
            <div class="economic-card">
                <div style="font-size: 0.85rem; color: #475569; font-weight: 600;">MOP (60% K2O)</div>
                <div style="font-size: 1.6rem; font-weight: 800; color: #d97706; margin: 4px 0;">{mop_bags} Bags</div>
                <div style="font-size: 0.8rem; color: #64748b;">Total: {total_mop_kg} kg ({mop_per_ha} kg/ha)</div>
            </div>
            """, unsafe_allow_html=True)
            
        with b4:
            ph_status = "Neutral (Optimal)"
            ph_color = "#166534"
            ph_remedy = "No amendment required"
            if input_ph < 5.8:
                ph_status = "Acidic Soil"
                ph_color = "#991b1b"
                lime_kg = round(1800 * total_hectares, 0)
                ph_remedy = f"Apply ~{lime_kg:.0f} kg Agricultural Lime"
            elif input_ph > 7.8:
                ph_status = "Alkaline Soil"
                ph_color = "#92400e"
                gyp_kg = round(1500 * total_hectares, 0)
                ph_remedy = f"Apply ~{gyp_kg:.0f} kg Gypsum / Sulfur"
                
            st.markdown(f"""
            <div class="economic-card">
                <div style="font-size: 0.85rem; color: #475569; font-weight: 600;">Soil pH Status</div>
                <div style="font-size: 1.25rem; font-weight: 800; color: {ph_color}; margin: 6px 0;">{ph_status}</div>
                <div style="font-size: 0.8rem; color: #64748b;">{ph_remedy}</div>
            </div>
            """, unsafe_allow_html=True)
            
        # Split Application Timetable
        st.markdown("#### 📅 Seasonal Split Application Timetable:")
        schedule_data = {
            "Crop Growth Stage": [
                "Stage 1: Basal Application (At Sowing / Field Prep)",
                "Stage 2: Vegetative Growth (30-40 Days After Sowing)",
                "Stage 3: Panicle Initiation / Flowering (60-70 Days)"
            ],
            "Urea Dose": [
                f"{round(total_urea_kg * 0.3, 1)} kg ({round(urea_bags * 0.3, 1)} bags - 30%)",
                f"{round(total_urea_kg * 0.4, 1)} kg ({round(urea_bags * 0.4, 1)} bags - 40%)",
                f"{round(total_urea_kg * 0.3, 1)} kg ({round(urea_bags * 0.3, 1)} bags - 30%)"
            ],
            "DAP Dose": [
                f"{total_dap_kg} kg ({dap_bags} bags - 100% Basal)",
                "None (Phosphorus applied as basal)",
                "None"
            ],
            "MOP Dose": [
                f"{total_mop_kg} kg ({mop_bags} bags - 100% Basal)",
                "None",
                "None (or 1% foliar spray if drought)"
            ]
        }
        st.table(pd.DataFrame(schedule_data))

    # -------------------------------------------------------------------------
    # FEATURE 2: CROP ECONOMICS & PROFITABILITY ESTIMATOR
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader(f"4. Crop Economics & Financial Projections")
    st.caption(f"Estimated yield, market revenues, and net profits calculated for **{total_acres:.2f} Acres**.")
    
    econ_primary = agronomic_data.get_crop_economics(primary_crop)
    
    # Financial metrics for primary crop
    yield_qtl_total = round(econ_primary["yield_per_acre_qtl"] * total_acres, 1)
    gross_revenue = round(yield_qtl_total * econ_primary["market_price_per_qtl"], 0)
    total_cost = round(econ_primary["cost_per_acre"] * total_acres, 0)
    net_profit = round(gross_revenue - total_cost, 0)
    roi_pct = round((net_profit / total_cost) * 100, 1) if total_cost > 0 else 0
    
    e1, e2, e3, e4 = st.columns(4)
    with e1:
        st.metric("🌾 Projected Total Yield", f"{yield_qtl_total:,.1f} Quintals", f"{econ_primary['yield_per_acre_qtl']} Qtl/Acre")
    with e2:
        st.metric("💵 Projected Gross Revenue", f"₹{gross_revenue:,.0f}", f"@ ₹{econ_primary['market_price_per_qtl']:,}/Qtl")
    with e3:
        st.metric("📉 Estimated Total Cost", f"₹{total_cost:,.0f}", f"₹{econ_primary['cost_per_acre']:,}/Acre")
    with e4:
        st.metric("💰 Net Profit Potential", f"₹{net_profit:,.0f}", f"ROI: +{roi_pct}%")
        
    # Top-3 Crops Comparative Profitability Matrix
    st.markdown("#### ⚖️ Top-3 Crops Comparative Profitability Analysis:")
    top3_econ_list = []
    for c in top3_crops:
        ec = agronomic_data.get_crop_economics(c)
        y_tot = round(ec["yield_per_acre_qtl"] * total_acres, 1)
        rev = round(y_tot * ec["market_price_per_qtl"], 0)
        cost = round(ec["cost_per_acre"] * total_acres, 0)
        prof = round(rev - cost, 0)
        roi = round((prof / cost) * 100, 1) if cost > 0 else 0
        top3_econ_list.append({
            "Crop": f"{CROP_ICONS.get(c, '🌱')} {c.capitalize()}",
            "Est. Yield (Qtl)": f"{y_tot:,.1f}",
            "Market / MSP (₹/Qtl)": f"₹{ec['market_price_per_qtl']:,}",
            "Est. Cultivation Cost (₹)": f"₹{cost:,.0f}",
            "Gross Revenue (₹)": f"₹{rev:,.0f}",
            "Net Profit (₹)": f"₹{prof:,.0f}",
            "ROI (%)": f"{roi:+.1f}%"
        })
    st.dataframe(pd.DataFrame(top3_econ_list), use_container_width=True)

    # -------------------------------------------------------------------------
    # FEATURE 3: SMART IRRIGATION & WATER MANAGEMENT ADVISORY
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader(f"5. Smart Irrigation & Seasonal Water Management")
    st.caption("Custom water budget analysis based on crop water requirements vs ambient seasonal rainfall.")
    
    w_col1, w_col2 = st.columns([1.1, 1.2])
    
    with w_col1:
        st.markdown(f"""
        <div class="water-box">
            <h3 style="margin: 0; color: #0f766e;">💧 {primary_crop.capitalize()} Water Profile</h3>
            <div style="margin-top: 10px; font-size: 0.95rem; color: #1e293b; line-height: 1.8;">
                • <strong>Cropping Season:</strong> {econ_primary.get('season', 'Kharif/Rabi')}<br>
                • <strong>Crop Duration:</strong> {econ_primary.get('duration_days', '100 - 120')} days<br>
                • <strong>Water Need Tier:</strong> <span style="font-weight:700; color:#0d9488;">{econ_primary.get('water_need', 'Moderate')}</span><br>
                • <strong>Recommended Technology:</strong> {econ_primary.get('irrigation_type', 'Precision Drip')}<br>
            </div>
            <div style="margin-top: 12px; font-size: 0.88rem; color: #047857; background: #ffffff; padding: 10px; border-radius: 8px; border: 1px dashed #99f6e4;">
                💡 <strong>Agronomic Pro-Tip:</strong> {econ_primary.get('water_saving_tip', 'Maintain uniform moisture during critical flowering stages.')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with w_col2:
        # Water Balance & Deficit Assessment
        crop_mean_rain = crop_bm["rainfall"]["mean"] if (benchmarks and primary_crop in benchmarks) else 120.0
        rain_diff = input_rain - crop_mean_rain
        
        st.markdown("#### 🌧️ Seasonal Rainfall Balance Assessment")
        st.metric(
            label="Current Input Rainfall vs Crop Requirement",
            value=f"{input_rain:.1f} mm",
            delta=f"{rain_diff:+.1f} mm (Ideal: {crop_mean_rain:.1f} mm)"
        )
        
        if rain_diff < -20:
            supp_irrigations = max(1, int(round(abs(rain_diff) / 45.0, 0)))
            st.warning(
                f"⚠️ **Moisture Deficit Detected:** Rainfall is {abs(rain_diff):.1f} mm below optimum for {primary_crop.capitalize()}.\n\n"
                f"• Provide approximately **{supp_irrigations} supplemental irrigations** (~45-50 mm each) during critical vegetative, flowering, and pod/grain formation stages.\n"
                f"• Deploy **{econ_primary.get('irrigation_type', 'Drip / Sprinkler')}** to minimize evapotranspiration losses."
            )
        elif rain_diff > 40:
            st.info(
                f"🌧️ **Ample Precipitation:** Input rainfall is {rain_diff:+.1f} mm higher than baseline.\n\n"
                f"• Natural rainfall is sufficient. Prioritize **field drainage channels** and broad-bed furrowing to prevent root hypoxia/waterlogging.\n"
                f"• Monitor for fungal foliar pathogens favored by prolonged leaf wetness."
            )
        else:
            st.success(
                f"✔ **Optimum Moisture Regime:** Ambient rainfall ({input_rain:.1f} mm) is in near-perfect equilibrium with the agronomic requirements of {primary_crop.capitalize()}!"
            )

    # -------------------------------------------------------------------------
    # RADAR / COMPARISON CHART
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### 📈 Soil Parameters vs Ideal Agronomic Baseline")
    comp_df = pd.DataFrame({
        "Parameter": ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "Rainfall"],
        "Current Farm Soil": [input_n, input_p, input_k, input_temp, input_humidity, input_rain],
        f"Ideal for {primary_crop.capitalize()}": [
            bench_n, bench_p, bench_k, 
            crop_bm["temperature"]["mean"], 
            crop_bm["humidity"]["mean"], 
            crop_bm["rainfall"]["mean"]
        ]
    })
    
    fig2, ax2 = plt.subplots(figsize=(10, 3.5))
    bar_w = 0.35
    x_idx = np.arange(len(comp_df))
    
    ax2.bar(x_idx - bar_w/2, comp_df["Current Farm Soil"], width=bar_w, label="Current Input", color="#0284c7")
    ax2.bar(x_idx + bar_w/2, comp_df[f"Ideal for {primary_crop.capitalize()}"], width=bar_w, label=f"Ideal {primary_crop.capitalize()}", color="#10b981")
    
    ax2.set_xticks(x_idx)
    ax2.set_xticklabels(comp_df["Parameter"], fontsize=10, fontweight='600')
    ax2.set_ylabel("Quantity / Metric Value", fontsize=10)
    ax2.legend(frameon=True, facecolor="#ffffff")
    ax2.grid(axis='y', linestyle=':', alpha=0.5)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    # -------------------------------------------------------------------------
    # FEATURE 4: 1-CLICK PRINTABLE SOIL HEALTH CARD
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.subheader("6. 📄 Official Farmer Soil Health Card (1-Click Export)")
    st.caption("Generate a certified, print-ready agronomic card formatted for A4 paper and PDF export.")
    
    soil_inputs_dict = {
        "N": input_n, "P": input_p, "K": input_k, "ph": input_ph,
        "temp": input_temp, "humidity": input_humidity, "rain": input_rain
    }
    fertilizer_plan_dict = {
        "urea_kg": total_urea_kg, "urea_bags": urea_bags,
        "dap_kg": total_dap_kg, "dap_bags": dap_bags,
        "mop_kg": total_mop_kg, "mop_bags": mop_bags
    }
    irrigation_plan_dict = {
        "season": econ_primary.get("season", "Kharif"),
        "duration_days": econ_primary.get("duration_days", "110-130"),
        "water_need": econ_primary.get("water_need", "Moderate"),
        "irrigation_type": econ_primary.get("irrigation_type", "Precision Drip"),
        "water_saving_tip": econ_primary.get("water_saving_tip", "Maintain uniform moisture during flowering.")
    }
    economics_dict = {
        "yield_total": yield_qtl_total,
        "gross_revenue": gross_revenue,
        "total_cost": total_cost,
        "net_profit": net_profit,
        "roi": roi_pct
    }
    
    card_html = report_generator.generate_soil_health_card_html(
        farmer_name=farmer_name,
        field_id=field_id,
        region=selected_region,
        total_acres=total_acres,
        total_hectares=total_hectares,
        primary_crop=primary_crop,
        primary_prob=primary_prob,
        primary_category=primary_category,
        top3_crops=top3_crops,
        top3_probs=top3_probs,
        soil_inputs=soil_inputs_dict,
        crop_benchmarks=crop_bm,
        fertilizer_plan=fertilizer_plan_dict,
        irrigation_plan=irrigation_plan_dict,
        economics=economics_dict
    )
    
    col_rep1, col_rep2 = st.columns([1.5, 1])
    with col_rep1:
        file_safe_name = f"Soil_Health_Card_{farmer_name.replace(' ', '_')}_{primary_crop}.html"
        st.download_button(
            label="📥 Download Official Soil Health Card (Print-Ready HTML / PDF)",
            data=card_html,
            file_name=file_safe_name,
            mime="text/html",
            type="primary",
            use_container_width=True
        )
    with col_rep2:
        st.caption("💡 Open the downloaded file in any browser and click **'Print / Save to PDF'** or press **Ctrl+P** for instant A4 printing.")
        
    with st.expander("👁️ Preview Soil Health Card Inside Dashboard"):
        st.components.v1.html(card_html, height=750, scrolling=True)

# =============================================================================
# TAB 2: EXPLAINABLE AI & MODEL INTELLIGENCE
# =============================================================================
with tab_xai:
    st.subheader("Explainable AI (XAI) & Model Transparency")
    st.caption("Detailed diagnostics on feature importance, model accuracy, and multiclass classification performance.")
    
    if metrics:
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Production Model", metrics.get("best_model", "Random Forest"))
        m2.metric("Overall Accuracy", f"{metrics.get('best_accuracy', 0.9955) * 100:.2f}%")
        m3.metric("Macro Avg F1-Score", f"{metrics.get('macro_avg_f1', 0.9955):.4f}")
        m4.metric("Evaluation Samples", "440 (Stratified 20%)")
        
        st.markdown("---")
        c_xai1, c_xai2 = st.columns([1.1, 1.1])
        
        with c_xai1:
            st.markdown("#### 🌟 Global Feature Importance (Gini Impurity)")
            st.caption("How strongly each agronomic factor drives the crop prediction algorithm.")
            
            fi = metrics.get("feature_importances", {})
            sorted_fi = sorted(fi.items(), key=lambda x: x[1], reverse=True)
            feat_names = [x[0] for x in sorted_fi]
            feat_scores = [x[1] * 100 for x in sorted_fi]
            
            fig_fi, ax_fi = plt.subplots(figsize=(6, 4))
            pal = sns.color_palette("mako", len(feat_names))
            sns.barplot(x=feat_scores, y=feat_names, palette=pal, ax=ax_fi)
            ax_fi.set_xlabel("Relative Importance Weight (%)", fontsize=10, fontweight='600')
            ax_fi.set_ylabel("Agronomic Variable", fontsize=10, fontweight='600')
            ax_fi.grid(axis='x', linestyle='--', alpha=0.4)
            
            for i, v in enumerate(feat_scores):
                ax_fi.text(v + 0.5, i, f"{v:.1f}%", va='center', fontsize=9, fontweight='600')
                
            plt.tight_layout()
            st.pyplot(fig_fi)
            plt.close()
            
        with c_xai2:
            st.markdown("#### ⚔️ Classifier Architecture Comparison")
            st.caption("Empirical benchmark of ensemble models on held-out test split.")
            
            rf_score = metrics.get("random_forest_accuracy", 0.9955) * 100
            xgb_score = metrics.get("xgboost_accuracy", 0.9886) * 100
            
            fig_comp, ax_comp = plt.subplots(figsize=(6, 3.5))
            models = ["Random Forest (Production)", "XGBoost Classifier"]
            scores = [rf_score, xgb_score]
            bars_c = ax_comp.bar(models, scores, color=['#059669', '#3b82f6'], width=0.45)
            ax_comp.set_ylim(95, 101)
            ax_comp.set_ylabel("Accuracy Score (%)", fontsize=10, fontweight='600')
            ax_comp.grid(axis='y', linestyle='--', alpha=0.3)
            
            for b in bars_c:
                h = b.get_height()
                ax_comp.text(b.get_x() + b.get_width()/2., h + 0.3, f"{h:.2f}%", 
                             ha='center', va='bottom', fontsize=11, fontweight='700')
                             
            plt.tight_layout()
            st.pyplot(fig_comp)
            plt.close()
            
        st.markdown("---")
        st.markdown("#### 🎯 Multiclass Confusion Matrix (22 Target Crops)")
        st.caption("Evaluating cross-crop classification precision across the test partition.")
        
        cm = np.array(metrics.get("confusion_matrix", []))
        classes = [c.capitalize() for c in metrics.get("classes", [])]
        
        if len(cm) > 0:
            fig_cm, ax_cm = plt.subplots(figsize=(11, 8.5))
            sns.heatmap(
                cm, 
                annot=True, 
                fmt='d', 
                cmap='Greens', 
                xticklabels=classes, 
                yticklabels=classes, 
                cbar=False,
                linewidths=0.5,
                linecolor='#e5e7eb',
                ax=ax_cm
            )
            plt.xticks(rotation=45, ha='right', fontsize=9)
            plt.yticks(rotation=0, fontsize=9)
            ax_cm.set_xlabel("Predicted Crop Class", fontsize=11, fontweight='700', labelpad=10)
            ax_cm.set_ylabel("True Crop Class", fontsize=11, fontweight='700', labelpad=10)
            plt.tight_layout()
            st.pyplot(fig_cm)
            plt.close()

# =============================================================================
# TAB 3: AGRONOMIC CROP CATALOG & ECONOMIC DATABASE
# =============================================================================
with tab_catalog:
    st.subheader("📚 Comprehensive 22-Crop Agronomic & Economic Catalog")
    st.caption("Explore verified agronomic thresholds, economics, and optimum growing conditions.")
    
    search_q = st.text_input("🔍 Filter crops by name:", "")
    cat_filter = st.selectbox("Filter by Category:", ["All Categories"] + sorted(list(set(CROP_CATEGORIES.values()))))
    
    if benchmarks:
        filtered_crops = []
        for c, bm in benchmarks.items():
            cat = CROP_CATEGORIES.get(c, "Standard")
            if search_q.lower() in c.lower() and (cat_filter == "All Categories" or cat == cat_filter):
                filtered_crops.append(c)
                
        filtered_crops.sort()
        
        # Grid Display of Crop Cards
        cols_per_row = 3
        for i in range(0, len(filtered_crops), cols_per_row):
            row_crops = filtered_crops[i:i+cols_per_row]
            row_cols = st.columns(cols_per_row)
            
            for col, crop_name in zip(row_cols, row_crops):
                bm = benchmarks[crop_name]
                icon = CROP_ICONS.get(crop_name, "🌱")
                cat = CROP_CATEGORIES.get(crop_name, "Standard")
                ec = agronomic_data.get_crop_economics(crop_name)
                
                with col:
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 16px; margin-bottom: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                        <div style="font-size: 1.8rem;">{icon} <strong style="text-transform: capitalize; color: #0f172a;">{crop_name}</strong></div>
                        <div style="color: #059669; font-weight: 600; font-size: 0.82rem; margin-bottom: 8px;">{cat} • {ec.get('season', 'Seasonal')}</div>
                        <div style="font-size: 0.84rem; color: #334155; line-height: 1.6;">
                            • <strong>N-P-K:</strong> {bm['N']['mean']} - {bm['P']['mean']} - {bm['K']['mean']} kg/ha<br>
                            • <strong>Soil pH:</strong> {bm['ph']['min']} - {bm['ph']['max']} (Avg: {bm['ph']['mean']})<br>
                            • <strong>Climate:</strong> {bm['temperature']['mean']}°C | {bm['humidity']['mean']}% Hum<br>
                            • <strong>Rainfall:</strong> {bm['rainfall']['mean']} mm<br>
                            • <strong>Avg Yield:</strong> {ec['yield_per_acre_qtl']} Qtl/Acre<br>
                            • <strong>Market / MSP:</strong> ₹{ec['market_price_per_qtl']:,}/Qtl<br>
                            • <strong>Cost of Cultivation:</strong> ₹{ec['cost_per_acre']:,}/Acre
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

# =============================================================================
# TAB 4: ARCHITECTURE & EXHIBITION SPECS
# =============================================================================
with tab_arch:
    st.subheader("🏗️ System Architecture & Specifications")
    
    st.markdown("""
    ### System Workflow Overview
    
    ```
    +---------------------------+       +------------------------------+
    | Live / Simulated Weather  |       | Soil Chemistry Laboratory    |
    | OpenWeatherMap / Presets  |       | N, P, K & pH Sensor Readings |
    +-------------+-------------+       +--------------+---------------+
                  |                                    |
                  +-----------------+------------------+
                                    |
                                    v
                  +------------------------------------+
                  | Scikit-Learn Feature Preprocessor  |
                  | StandardScaler Continuous Pipeline |
                  +-----------------+------------------+
                                    |
                                    v
                  +------------------------------------+
                  | High-Precision Ensemble Classifier |
                  | Random Forest (99.55% Test Acc)    |
                  +-----------------+------------------+
                                    |
        +---------------------------+---------------------------+
        |                           |                           |
        v                           v                           v
    +-------------------+   +--------------------+   +----------------------+
    | Top-3 Crop Suit.  |   | Soil Nutrient Gap  |   | Crop Economics &     |
    | Confidence Probs  |   | & 50kg Bag Sizing  |   | Profit Estimator     |
    +-------------------+   +--------------------+   +----------------------+
                                    |
                                    v
                            +--------------------+
                            | Smart Irrigation & |
                            | Water Management   |
                            +--------------------+
    ```
    
    ---
    
    ### Key Engineering Highlights for Exhibition Evaluation
    
    1. **Robust Agronomic ML Backbone**:
       - 2,200 real-world agro-ecological records evaluated across 22 crops.
       - Stratified 80/20 train/test evaluation with cross-validation.
       - Random Forest Classifier outperforming XGBoost with **99.55% accuracy** and **0.9955 Macro F1-score**.
    
    2. **Land Size Scaler & Commercial 50kg Fertilizer Sizing**:
       - Translates abstract scientific kg/ha into physical **50kg commercial bags** (Urea, DAP, MOP) tailored to the farmer's specific landholding.
       - Provides an actionable 3-phase split application timetable (Basal, 30-day Vegetative, Flowering).
       
    3. **Crop Economics & Financial ROI Projections**:
       - Computes estimated yield (Quintals), gross revenue (based on Mandi/MSP prices), cultivation costs, and net profit margins.
       - Delivers a comparative Top-3 financial analysis so farmers and judges can evaluate economic viability.
       
    4. **Smart Water Budgeting & Irrigation Technology**:
       - Assesses rainfall deficit/surplus against target crop needs and prescribes supplemental irrigation cycles.
       - Recommends optimal water-saving systems (Drip with Fertigation, Micro-Sprinklers, Alternate Wetting & Drying).
       
    5. **Offline-Resilient Weather Integration**:
       - Dual-mode weather architecture: queries OpenWeatherMap live REST API when online, and seamlessly falls back to pre-compiled agro-climatic profiles for major farming states (Punjab, Maharashtra, UP, Karnataka, Kerala, etc.).
    """)
    
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.85rem; padding: 12px;'>"
    "C.R.O.P.S. — Climate & Resource-Optimized Predictive System | Developed with Streamlit, Scikit-Learn & Python"
    "</div>", 
    unsafe_allow_html=True
)
