import streamlit as st
import pandas as pd
import numpy as np
import pickle
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="RainGuard AI",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CUSTOM CSS — PROFESSIONAL THEME + ANIMATIONS
# =========================================================

st.markdown("""
<style>

    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 10% 10%, #eef3fb 0%, #f7f9fc 40%, #eef2f9 100%);
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* ---------------- HERO ---------------- */

    @keyframes floatCloud {
        0%   { transform: translateY(0px) translateX(0px); opacity: 0.5; }
        50%  { transform: translateY(-14px) translateX(10px); opacity: 0.85; }
        100% { transform: translateY(0px) translateX(0px); opacity: 0.5; }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0px); }
    }

    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }

    @keyframes pulseGlow {
        0%   { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
        50%  { box-shadow: 0 0 35px rgba(59,130,246,0.35); }
        100% { box-shadow: 0 0 0px rgba(59,130,246,0.4); }
    }

    .hero {
        position: relative;
        overflow: hidden;
        padding: 3rem 2.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        background-size: 200% 200%;
        color: white;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease, pulseGlow 6s ease-in-out infinite;
        box-shadow: 0 20px 45px rgba(15, 23, 42, 0.35);
    }

    .hero::before {
        content: "☁️";
        position: absolute;
        font-size: 70px;
        top: -10px;
        right: 60px;
        animation: floatCloud 7s ease-in-out infinite;
        opacity: 0.5;
    }

    .hero::after {
        content: "🌦️";
        position: absolute;
        font-size: 50px;
        bottom: -5px;
        right: 200px;
        animation: floatCloud 9s ease-in-out infinite reverse;
        opacity: 0.4;
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.25);
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 13px;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
        backdrop-filter: blur(6px);
    }

    .hero h1 {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 6px;
        letter-spacing: -0.5px;
    }

    .hero p {
        font-size: 17px;
        opacity: 0.88;
        max-width: 600px;
        line-height: 1.5;
    }

    /* ---------------- SECTION TITLES ---------------- */

    .section-title {
        font-size: 20px;
        font-weight: 700;
        margin-top: 0.2rem;
        margin-bottom: 1.1rem;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 8px;
        animation: fadeInUp 0.6s ease;
    }

    .section-title::before {
        content: "";
        width: 5px;
        height: 20px;
        border-radius: 4px;
        background: linear-gradient(180deg, #2563eb, #60a5fa);
        display: inline-block;
    }

    /* ---------------- GLASS CARD WRAPPER ---------------- */

    .glass-card {
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.6);
        border-radius: 18px;
        padding: 1.4rem 1.6rem 0.6rem 1.6rem;
        margin-bottom: 1.6rem;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeInUp 0.5s ease;
    }

    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 14px 34px rgba(15, 23, 42, 0.1);
    }

    /* ---------------- INPUTS ---------------- */

    div[data-baseweb="select"] > div, .stNumberInput input, .stTextInput input {
        border-radius: 10px !important;
        transition: all 0.2s ease;
    }

    div[data-baseweb="select"] > div:focus-within, .stNumberInput input:focus {
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
        border-color: #2563eb !important;
    }

    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #2563eb, #60a5fa) !important;
    }

    /* ---------------- TABS ---------------- */

    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15,23,42,0.04);
        padding: 6px;
        border-radius: 14px;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 8px 18px;
        font-weight: 600;
        color: #475569;
        transition: all 0.25s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1e3a8a, #2563eb) !important;
        color: white !important;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
    }

    /* ---------------- BUTTON ---------------- */

    .stButton > button {
        background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 60%, #3b82f6 100%);
        color: white;
        font-weight: 700;
        font-size: 17px;
        border: none;
        border-radius: 14px;
        padding: 0.85rem 0;
        letter-spacing: 0.3px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.35);
    }

    .stButton > button:hover {
        transform: translateY(-2px) scale(1.01);
        box-shadow: 0 14px 32px rgba(37, 99, 235, 0.45);
        color: white;
    }

    .stButton > button:active {
        transform: translateY(0px) scale(0.99);
    }

    /* ---------------- PREDICTION CARD ---------------- */

    .prediction-card {
        padding: 2.5rem;
        border-radius: 22px;
        text-align: center;
        margin-top: 1.5rem;
        color: white;
        animation: fadeInUp 0.6s ease;
        box-shadow: 0 18px 40px rgba(0,0,0,0.18);
        position: relative;
        overflow: hidden;
    }

    .rain-card {
        background: linear-gradient(135deg, #0f172a, #1e3a8a, #2563eb);
    }

    .sunny-card {
        background: linear-gradient(135deg, #f59e0b, #f97316, #fb923c);
    }

    .prediction-card h2 {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .prediction-card p {
        font-size: 16px;
        opacity: 0.92;
    }

    /* ---------------- METRIC MINI CARDS ---------------- */

    .mini-metric {
        background: white;
        border-radius: 14px;
        padding: 14px 18px;
        text-align: center;
        box-shadow: 0 6px 16px rgba(15,23,42,0.06);
        animation: fadeInUp 0.5s ease;
    }

    .mini-metric .val {
        font-size: 22px;
        font-weight: 800;
        color: #1e3a8a;
    }

    .mini-metric .lab {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* ---------------- FOOTER ---------------- */

    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(15,23,42,0.08);
        color: #94a3b8;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD MODEL
# =========================================================

@st.cache_resource
def load_artifacts():
    with open("weather_model.pkl", "rb") as file:
        artifacts = pickle.load(file)
    return artifacts


artifacts = load_artifacts()

model = artifacts["model"]

iterative_imputer = artifacts["iterative_imputer"]
categorical_imputer = artifacts["categorical_imputer"]
median_imputer = artifacts["median_imputer"]
mean_imputer = artifacts["mean_imputer"]

rain_encoder = artifacts["rain_encoder"]

ohe_3pm = artifacts["ohe_3pm"]
ohe_9am = artifacts["ohe_9am"]
ohe_gust = artifacts["ohe_gust"]

location_encoder = artifacts["location_encoder"]

standard_scaler = artifacts["standard_scaler"]
power_transformer = artifacts["power_transformer"]

iterative_cols = artifacts["iterative_cols"]
standard_cols = artifacts["standard_cols"]
power_cols = artifacts["power_cols"]

feature_names = artifacts["feature_names"]


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ POWERED BY MACHINE LEARNING</div>
    <h1>🌧️ RainGuard AI</h1>
    <p>
        Intelligent rain-prediction system that reads today's weather signals
        and forecasts tomorrow's sky — instantly, accurately, beautifully.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================================================
# INPUTS — ORGANIZED IN TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📍 Location & Date",
    "🌡️ Temperature",
    "💧 Rain & Humidity",
    "💨 Wind",
    "🌤️ Atmosphere"
])

with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        location = st.selectbox(
            "Location",
            [
                "Adelaide", "Albany", "Albury", "AliceSprings",
                "BadgerysCreek", "Ballarat", "Bendigo", "Brisbane",
                "Cairns", "Canberra", "Cobar", "CoffsHarbour",
                "Dartmoor", "Darwin", "Dubbo", "EastSale",
                "Eden", "Geraldton", "GoldCoast", "Hobart",
                "Katherine", "Launceston", "Melbourne",
                "MelbourneAirport", "Mildura", "Moree", "MountGambier",
                "MountGinini", "Newcastle", "Nhil", "NorahHead",
                "NorfolkIsland", "Nuriootpa", "PearceRAAF",
                "Penrith", "Perth", "PerthAirport", "Portland",
                "Richmond", "Sale", "SalmonGums", "Sydney",
                "SydneyAirport", "Townsville", "Tuggeranong",
                "Uluru", "WaggaWagga", "Walpole", "Watsonia",
                "Williamtown", "Witchcliffe", "Wollongong",
                "Woomera"
            ]
        )

    with col2:
        year = st.number_input("Year", min_value=2007, max_value=2035, value=2016)

    with col3:
        month = st.slider("Month", 1, 12, 6)

    with col4:
        day = st.slider("Day", 1, 31, 15)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        min_temp = st.number_input("Min Temperature", value=10.0)

    with col2:
        max_temp = st.number_input("Max Temperature", value=20.0)

    with col3:
        temp_9am = st.number_input("Temperature 9am", value=15.0)

    with col4:
        temp_3pm = st.number_input("Temperature 3pm", value=19.0)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        rainfall = st.number_input("Rainfall (mm)", min_value=0.0, value=0.0)

    with col2:
        rain_today = st.selectbox("Rain Today?", ["No", "Yes"])

    with col3:
        humidity_9am = st.number_input("Humidity 9am", min_value=0.0, max_value=100.0, value=70.0)

    with col4:
        humidity_3pm = st.number_input("Humidity 3pm", min_value=0.0, max_value=100.0, value=50.0)
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    directions = [
        "N", "NNE", "NE", "ENE",
        "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW",
        "W", "WNW", "NW", "NNW"
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        wind_gust_dir = st.selectbox("Wind Gust Direction", directions)

    with col2:
        wind_dir_9am = st.selectbox("Wind Direction 9am", directions)

    with col3:
        wind_dir_3pm = st.selectbox("Wind Direction 3pm", directions)

    col1, col2, col3 = st.columns(3)

    with col1:
        wind_gust_speed = st.number_input("Wind Gust Speed", min_value=0.0, value=35.0)

    with col2:
        wind_speed_9am = st.number_input("Wind Speed 9am", min_value=0.0, value=15.0)

    with col3:
        wind_speed_3pm = st.number_input("Wind Speed 3pm", min_value=0.0, value=15.0)
    st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        evaporation = st.number_input("Evaporation", min_value=0.0, value=5.0)

    with col2:
        sunshine = st.number_input("Sunshine", min_value=0.0, value=7.0)

    with col3:
        pressure_9am = st.number_input("Pressure 9am", value=1015.0)

    with col4:
        pressure_3pm = st.number_input("Pressure 3pm", value=1012.0)

    col1, col2 = st.columns(2)

    with col1:
        cloud_9am = st.slider("Cloud 9am", 0, 8, 4)

    with col2:
        cloud_3pm = st.slider("Cloud 3pm", 0, 8, 4)
    st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# QUICK SUMMARY STRIP
# =========================================================

st.markdown('<div class="section-title">📊 Snapshot</div>', unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(f"""
    <div class="mini-metric">
        <div class="val">{location}</div>
        <div class="lab">Location</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="mini-metric">
        <div class="val">{max_temp}°C</div>
        <div class="lab">Max Temp Today</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="mini-metric">
        <div class="val">{humidity_3pm}%</div>
        <div class="lab">Humidity 3pm</div>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class="mini-metric">
        <div class="val">{rainfall} mm</div>
        <div class="lab">Rainfall Today</div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PREDICTION
# =========================================================

st.markdown("<br>", unsafe_allow_html=True)

predict = st.button("🚀 Predict Tomorrow's Weather", use_container_width=True)


if predict:

    with st.spinner("Analyzing atmospheric patterns..."):
        time.sleep(0.6)

        # ---------------------------------------------
        # Create raw input DataFrame
        # ---------------------------------------------

        input_df = pd.DataFrame({
            "Location": [location],
            "MinTemp": [min_temp],
            "MaxTemp": [max_temp],
            "Rainfall": [rainfall],
            "Evaporation": [evaporation],
            "Sunshine": [sunshine],
            "WindGustDir": [wind_gust_dir],
            "WindGustSpeed": [wind_gust_speed],
            "WindDir9am": [wind_dir_9am],
            "WindDir3pm": [wind_dir_3pm],
            "WindSpeed9am": [wind_speed_9am],
            "WindSpeed3pm": [wind_speed_3pm],
            "Humidity9am": [humidity_9am],
            "Humidity3pm": [humidity_3pm],
            "Pressure9am": [pressure_9am],
            "Pressure3pm": [pressure_3pm],
            "Cloud9am": [cloud_9am],
            "Cloud3pm": [cloud_3pm],
            "Temp9am": [temp_9am],
            "Temp3pm": [temp_3pm],
            "RainToday": [rain_today],
            "Year": [year],
            "Month": [month],
            "Day": [day]
        })

        # ---------------------------------------------
        # Iterative Imputation
        # ---------------------------------------------

        input_df[iterative_cols] = iterative_imputer.transform(input_df[iterative_cols])

        # ---------------------------------------------
        # Categorical Imputation
        # ---------------------------------------------

        categorical_cols = ["RainToday", "WindDir9am", "WindGustDir", "WindDir3pm"]

        input_df[categorical_cols] = categorical_imputer.transform(input_df[categorical_cols])

        # ---------------------------------------------
        # Median Imputation
        # ---------------------------------------------

        median_cols = ["Rainfall", "Evaporation"]

        input_df[median_cols] = median_imputer.transform(input_df[median_cols])

        # ---------------------------------------------
        # Mean Imputation
        # ---------------------------------------------

        mean_cols = ["Pressure9am", "Pressure3pm", "WindSpeed3pm"]

        input_df[mean_cols] = mean_imputer.transform(input_df[mean_cols])

        # ---------------------------------------------
        # RainToday Encoding
        # ---------------------------------------------

        input_df[["RainToday"]] = rain_encoder.transform(input_df[["RainToday"]])

        # ---------------------------------------------
        # Location Target Encoding
        # ---------------------------------------------

        input_df[["Location"]] = location_encoder.transform(input_df[["Location"]])

        # ---------------------------------------------
        # Wind OHE
        # ---------------------------------------------

        encoded_3pm = ohe_3pm.transform(input_df[["WindDir3pm"]])
        encoded_9am = ohe_9am.transform(input_df[["WindDir9am"]])
        encoded_gust = ohe_gust.transform(input_df[["WindGustDir"]])

        names_3pm = ohe_3pm.get_feature_names_out(["WindDir3pm"])
        names_9am = ohe_9am.get_feature_names_out(["WindDir9am"])
        names_gust = ohe_gust.get_feature_names_out(["WindGustDir"])

        input_df[names_3pm] = encoded_3pm
        input_df[names_9am] = encoded_9am
        input_df[names_gust] = encoded_gust

        input_df.drop(["WindDir3pm", "WindDir9am", "WindGustDir"], axis=1, inplace=True)

        # ---------------------------------------------
        # Standard Scaling
        # ---------------------------------------------

        input_df[standard_cols] = standard_scaler.transform(input_df[standard_cols])

        # ---------------------------------------------
        # Power Transformation
        # ---------------------------------------------

        input_df[power_cols] = power_transformer.transform(input_df[power_cols])

        # ---------------------------------------------
        # Make sure feature order matches training
        # ---------------------------------------------

        input_df = input_df.reindex(columns=feature_names, fill_value=0)

        # ---------------------------------------------
        # Prediction
        # ---------------------------------------------

        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

    # ---------------------------------------------
    # Result
    # ---------------------------------------------

    if prediction == 1:
        st.markdown(f"""
        <div class="prediction-card rain-card">
            <h2>🌧️ Rain Expected Tomorrow</h2>
            <p>The model predicts a {probability:.0%} chance of rain based on today's conditions.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="prediction-card sunny-card">
            <h2>☀️ No Rain Expected Tomorrow</h2>
            <p>The model predicts only a {probability:.0%} chance of rain — clear skies ahead.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(float(probability), text=f"Rain probability: {probability:.1%}")


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">
    RainGuard AI • Machine Learning Weather Prediction &nbsp;•&nbsp; Built with Streamlit
</div>
""", unsafe_allow_html=True)