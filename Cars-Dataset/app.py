import time
import joblib
import pandas as pd
import streamlit as st

# ================= 1. Configuration & Setup =================

st.set_page_config(
    page_title="HyperDrive Price Predictor",
    page_icon="🏎️",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# تحميل الموديل والـ Scaler الخاص بالـ Target
@st.cache_resource
def load_assets():
    model = joblib.load("car_price_model.pkl")
    try:
        scaler = joblib.load("target_scaler.pkl")
    except Exception:
        scaler = None
    return model, scaler


try:
    model, target_scaler = load_assets()
except Exception as e:
    model, target_scaler = None, None


# ================= 2. Dynamic Car Image Database =================

CAR_IMAGES = {
    "BMW": "https://images.unsplash.com/photo-1555215695-3004980ad54e?q=80&w=1000&auto=format&fit=crop",
    "Mercedes": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?q=80&w=1000&auto=format&fit=crop",
    "Audi": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?q=80&w=1000&auto=format&fit=crop",
    "Toyota": "https://images.unsplash.com/photo-1621007947382-bb3c3994e3fb?q=80&w=1000&auto=format&fit=crop",
    "Honda": "https://images.unsplash.com/photo-1606152421802-db97b9c7a11b?q=80&w=1000&auto=format&fit=crop",
    "Ford": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?q=80&w=1000&auto=format&fit=crop",
    "Nissan": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?q=80&w=1000&auto=format&fit=crop",
    "Hyundai": "https://images.unsplash.com/photo-1629897048514-3dd7414fe72a?q=80&w=1000&auto=format&fit=crop",
}


# ================= 3. High-Octane CSS Animations =================

st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800;900&family=Rajdhani:wght@500;600;700&display=swap" rel="stylesheet">

<style>
.stApp {
    background: #080B10;
    background-image: 
        radial-gradient(circle at 50% 0%, rgba(255, 85, 0, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 85% 90%, rgba(0, 229, 255, 0.08) 0%, transparent 40%);
    color: #E2E8F0;
    font-family: 'Rajdhani', sans-serif;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

@keyframes pulseGlow {
    0% { box-shadow: 0 0 15px rgba(255, 85, 0, 0.2); }
    50% { box-shadow: 0 0 30px rgba(255, 85, 0, 0.6); }
    100% { box-shadow: 0 0 15px rgba(255, 85, 0, 0.2); }
}

@keyframes slideUp {
    from { transform: translateY(20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.dashboard-header {
    background: linear-gradient(135deg, #101522 0%, #0A0D14 100%);
    border: 1px solid #1E293B;
    border-left: 5px solid #FF5500;
    border-radius: 12px;
    padding: 20px 30px;
    margin-bottom: 20px;
    animation: pulseGlow 4s infinite ease-in-out;
}
.header-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 28px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: 2px;
}
.header-title span { color: #FF5500; }

.spec-card {
    background: rgba(16, 21, 34, 0.7);
    backdrop-filter: blur(10px);
    border: 1px solid #1E2A3C;
    border-radius: 12px;
    padding: 24px;
    transition: all 0.3s ease;
}
.spec-card:hover {
    border-color: #FF5500;
    transform: translateY(-2px);
}

.car-preview-container {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #1E2A3C;
    height: 100%;
    min-height: 280px;
}
.car-preview-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}
.car-preview-container:hover .car-preview-img {
    transform: scale(1.05);
}
.car-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(360deg, #080B10 100%, transparent 0%);
    padding: 15px;
    font-family: 'Orbitron', sans-serif;
    font-size: 18px;
    color: #FFFFFF;
    font-weight: 700;
}

div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: #0B0E14 !important;
    border: 1px solid #243044 !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
}
label {
    color: #94A3B8 !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #FF5500 0%, #FF2200 100%);
    color: #FFFFFF;
    font-family: 'Orbitron', sans-serif;
    font-weight: 800;
    font-size: 18px;
    letter-spacing: 2px;
    padding: 16px 0;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    box-shadow: 0 0 20px rgba(255, 85, 0, 0.4);
    transition: all 0.3s ease;
    margin-top: 10px;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #FF6611 0%, #FF3311 100%);
    box-shadow: 0 0 35px rgba(255, 85, 0, 0.8);
    transform: scale(1.01);
    color: #FFFFFF;
}

.gauge-box {
    animation: slideUp 0.5s ease-out forwards;
    background: linear-gradient(180deg, #101726 0%, #090D15 100%);
    border: 2px solid #00E5FF;
    border-radius: 14px;
    padding: 30px;
    text-align: center;
    box-shadow: 0 0 30px rgba(0, 229, 255, 0.2);
    margin-top: 25px;
}
.gauge-val {
    font-family: 'Orbitron', sans-serif;
    font-size: 60px;
    font-weight: 900;
    color: #00E5FF;
    text-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
}
.badge {
    display: inline-block;
    background: rgba(0, 229, 255, 0.1);
    border: 1px solid #00E5FF;
    color: #00E5FF;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 13px;
    margin: 3px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ================= 4. Header UI =================

st.markdown(
    """
<div class="dashboard-header">
    <div class="header-title">🏎️ HYPER<span>DRIVE</span> VALUATION</div>
    <p style="color: #64748B; margin: 0; font-size: 14px;">Next-Gen AI Vehicle Price Intelligence</p>
</div>
""",
    unsafe_allow_html=True,
)


# ================= 5. Interactive Form & Image Preview =================

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown('<div class="spec-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        brand = st.selectbox(
            "🏎️ Brand", list(CAR_IMAGES.keys()), key="brand_select"
        )
        fuel_type = st.selectbox(
            "⛽ Fuel Type", ["Petrol", "Diesel", "Hybrid", "Electric"]
        )
        transmission = st.selectbox("🕹️ Transmission", ["Automatic", "Manual"])

    with c2:
        car_age = st.number_input(
            "📅 Car Age (Years)", min_value=0, max_value=30, value=3
        )
        mileage = st.number_input(
            "🛣️ Mileage (KM)", min_value=0.0, value=35000.0, step=1000.0
        )
        engine_size = st.number_input(
            "⚙️ Engine Size (L)",
            min_value=0.5,
            max_value=10.0,
            value=2.0,
            step=0.1,
        )

    previous_owners = st.slider("👥 Previous Owners", 0, 5, 1)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    selected_img = CAR_IMAGES.get(brand, CAR_IMAGES["BMW"])
    st.markdown(
        f"""
    <div class="car-preview-container">
        <img src="{selected_img}" class="car-preview-img" alt="Car Image">
        <div class="car-overlay">
            {brand} Performance Spec
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

predict_clicked = st.button("⚡ CALCULATE FAIR MARKET VALUE")


# ================= 6. Prediction Logic & Scaler Inverse =================

if predict_clicked:
    if model is None:
        st.error(
            "⚠️ Model file 'car_price_model.pkl' missing! Please upload it."
        )
    else:
        input_data = pd.DataFrame(
            {
                "Brand": [brand],
                "Car_Age": [car_age],
                "Mileage": [mileage],
                "Engine_Size": [engine_size],
                "Fuel_Type": [fuel_type],
                "Transmission": [transmission],
                "Previous_Owners": [previous_owners],
            }
        )

        try:
            # 1. توقع السعر بالموديل
            raw_prediction = model.predict(input_data)

            # 2. إرجاع السعر للقيم الحقيقية عبر Inverse Transform
            if target_scaler is not None:
                # التحويل يتطلب شكل (1, 1)
                scaled_pred = raw_prediction.reshape(-1, 1)
                real_price = target_scaler.inverse_transform(scaled_pred)[0][0]
            else:
                # في حالة عدم وجود ملف الـ scaler يتوقع السعر كقيمة مباشرة
                real_price = raw_prediction[0]

            # 3. عرض النتيجة بالعداد المتحرك
            gauge_placeholder = st.empty()

            steps = 25
            for i in range(1, steps + 1):
                current_value = (real_price / steps) * i
                gauge_placeholder.markdown(
                    f"""
                <div class="gauge-box">
                    <div style="font-family: Orbitron; color: #94A3B8; letter-spacing: 2px; font-size: 14px;">ESTIMATED VALUE</div>
                    <div class="gauge-val">${current_value:,.0f}</div>
                    <div style="margin-top: 10px;">
                        <span class="badge">{brand}</span>
                        <span class="badge">{fuel_type}</span>
                        <span class="badge">{transmission}</span>
                        <span class="badge">{mileage:,.0f} KM</span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )
                time.sleep(0.015)

        except Exception as e:
            st.error(f"Error executing valuation: {e}")