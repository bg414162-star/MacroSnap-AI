# -*- coding: utf-8 -*-
"""
MacroSnap AI - Vision & Expiry Engine
Production-grade Multimodal Vision, Safety Inspection & Expiry Engine.
Built with Streamlit, Google GenAI SDK (gemini-3.8-flash), and Cyberpunk Glassmorphic UI.
"""

import os
import sys
import json
import time
import asyncio
import warnings
import re
from urllib.parse import quote, quote_plus
from dotenv import load_dotenv
from PIL import Image
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# 0️⃣ Platform OS Fixes & Environment Configuration
# ---------------------------------------------------------------------------
if sys.platform.startswith("win"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass

warnings.filterwarnings("ignore", category=RuntimeWarning, message=".*Proactor.*")
warnings.filterwarnings("ignore", message=".*Proactor event loop.*")

load_dotenv()

# ---------------------------------------------------------------------------
# 1️⃣ Streamlit Page Configuration & Cyberpunk Glassmorphism Styling
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="MacroSnap AI | Vision & Expiry Engine",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #030712 !important;
        background-image: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #0f172a 50%, #030712 100%) !important;
        background-attachment: fixed !important;
        color: #f1f5f9 !important;
    }

    #MainMenu, footer, header {
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Cyberpunk Glass Container */
    .glass-panel {
        background: rgba(17, 24, 39, 0.75) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5) !important;
        margin-bottom: 1.5rem !important;
    }

    /* Gradient Brand Title */
    .brand-title {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
    }

    /* Operator Profile Chip */
    .operator-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.35);
        padding: 0.35rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.85rem;
        font-weight: 600;
    }

    /* Primary Cyber Action Button */
    .stButton>button {
        background: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #0ea5e9 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 14px !important;
        padding: 0.8rem 1.8rem !important;
        transition: all 0.25s ease-in-out !important;
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.45) !important;
        width: 100% !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px) scale(1.01) !important;
        box-shadow: 0 8px 30px rgba(14, 165, 233, 0.6) !important;
        border-color: #38bdf8 !important;
    }

    /* Streamlit Input Styling */
    .stTextInput input {
        background: rgba(15, 23, 42, 0.85) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 0.75rem 1rem !important;
        font-size: 0.95rem !important;
    }

    .stTextInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
    }

    /* Tab Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding-bottom: 8px !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        padding: 8px 18px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        background: rgba(56, 189, 248, 0.15) !important;
        border: 1px solid #38bdf8 !important;
        color: #ffffff !important;
    }

    /* Ultra-High Contrast AI Inspection Report Box */
    .report-card {
        background-color: #0f172a !important;
        border: 2px solid #38bdf8 !important;
        border-radius: 18px !important;
        padding: 2rem !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        line-height: 1.75 !important;
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.25) !important;
        margin-top: 1.5rem !important;
    }

    .report-card h3 {
        color: #38bdf8 !important;
        margin-top: 0 !important;
        margin-bottom: 1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
    }

    .macro-chip-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 12px 0 16px 0;
    }

    .macro-chip {
        background: rgba(30, 41, 59, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 10px;
        padding: 6px 14px;
        font-size: 0.9rem;
        font-weight: 700;
        color: #ffffff;
    }

    .macro-chip span {
        color: #38bdf8;
    }

    .status-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .status-safe {
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid #22c55e;
    }

    .status-warning {
        background: rgba(234, 179, 8, 0.2);
        color: #facc15;
        border: 1px solid #eab308;
    }

    .status-danger {
        background: rgba(239, 68, 68, 0.2);
        color: #f87171;
        border: 1px solid #ef4444;
    }

    /* WhatsApp Dispatch Deep-Link Button */
    .whatsapp-btn {
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.9rem 1.8rem !important;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(37, 211, 102, 0.4) !important;
        transition: all 0.25s ease-in-out !important;
        margin-top: 1.5rem !important;
        width: 100% !important;
        text-align: center !important;
    }

    .whatsapp-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(37, 211, 102, 0.6) !important;
        color: #ffffff !important;
        text-decoration: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# 2️⃣ Dual-Language Localization Engine (English & Hindi)
# ---------------------------------------------------------------------------
DICT = {
    "English": {
        "title": "MacroSnap AI",
        "subtitle": "Multimodal Expiry Tracking, Safety Inspection & Automated Dispatch",
        "login_header": "Operator Authentication",
        "login_sub": "Enter your verified operator details to initialize the engine.",
        "name_lbl": "Operator Full Name",
        "phone_lbl": "WhatsApp Mobile Number",
        "login_btn": "Authenticate & Launch Workspace",
        "welcome": "Active Operator",
        "active_mode": "Environment Inspection Mode",
        "home": "Personal / Household",
        "shop": "Enterprise / Retail Stock",
        "cam_heading": "📷 Live Camera Scan",
        "upload_heading": "📁 Upload Image File",
        "cam_btn": "Capture Product Snapshot",
        "upload_btn": "Choose Image (JPG, PNG, WEBP)",
        "logout": "Disconnect",
        "analyze_btn": "⚡ Run AI Multimodal Analysis",
        "send_wa": "📲 Dispatch Inspection Report to WhatsApp",
        "invalid_phone": "Please enter a valid 10-digit mobile number.",
        "no_image": "📸 Capture via camera or upload a clear product image above to begin inspection.",
        "processing": "Analyzing multimodal imagery with Gemini 3.8 Flash...",
        "report_header": "📋 MacroSnap AI Multimodal Inspection Report",
        "prod_name": "Product & Brand",
        "expiry": "Expiry / Best Before",
        "health_status": "Safety & Health Risk",
        "macros": "Nutritional Breakdown",
        "ingredients": "Key Ingredients",
        "allergens": "Allergen Alerts",
    },
    "Hindi": {
        "title": "मैक्रोसनैप विज़न एआई",
        "subtitle": "मल्टीमॉडल एक्सपायरी ट्रैकिंग, स्वास्थ्य सुरक्षा और स्वचालित व्हाट्सएप डिस्पैच",
        "login_header": "ऑपरेटर प्रमाणीकरण",
        "login_sub": "कार्यक्षेत्र शुरू करने के लिए अपना प्रमाणित विवरण दर्ज करें।",
        "name_lbl": "ऑपरेटर का पूरा नाम",
        "phone_lbl": "व्हाट्सएप मोबाइल नंबर",
        "login_btn": "प्रमाणित करें और कार्यक्षेत्र खोलें",
        "welcome": "सक्रिय ऑपरेटर",
        "active_mode": "कार्यक्षेत्र निरीक्षण मोड",
        "home": "घरेलू / व्यक्तिगत",
        "shop": "दुकान / रिटेल स्टॉक",
        "cam_heading": "📷 लाइव कैमरा स्कैनर",
        "upload_heading": "📁 इमेज फ़ाइल अपलोड",
        "cam_btn": "उत्पाद की फ़ोटो लें",
        "upload_btn": "इमेज चुनें (JPG, PNG, WEBP)",
        "logout": "लॉगआउट",
        "analyze_btn": "⚡ एआई मल्टीमॉडल विश्लेषण चलाएं",
        "send_wa": "📲 व्हाट्सएप पर निरीक्षण रिपोर्ट भेजें",
        "invalid_phone": "कृपया 10 अंकों का सही मोबाइल नंबर दर्ज करें।",
        "no_image": "📸 विश्लेषण शुरू करने के लिए ऊपर कैमरे से फोटो लें या इमेज फ़ाइल अपलोड करें।",
        "processing": "Gemini 3.8 Flash के साथ मल्टीमॉडल विश्लेषण किया जा रहा है...",
        "report_header": "📋 मैक्रोसनैप एआई निरीक्षण रिपोर्ट",
        "prod_name": "उत्पाद और ब्रांड",
        "expiry": "एक्सपायरी / उपयोग की अंतिम तिथि",
        "health_status": "सुरक्षा और स्वास्थ्य जोखिम",
        "macros": "पोषण विवरण (न्यूट्रिशन)",
        "ingredients": "मुख्य सामग्री",
        "allergens": "एलर्जी चेतावनी (Allergens)",
    },
}

# ---------------------------------------------------------------------------
# 3️⃣ Persistent State Management via st.session_state & st.query_params
# ---------------------------------------------------------------------------
def sync_authentication():
    """Sync authentication seamlessly between session_state and URL query parameters."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    if "user_phone" not in st.session_state:
        st.session_state.user_phone = ""
    if "language" not in st.session_state:
        st.session_state.language = "English"

    # Read persistent query parameters if present
    qp_name = st.query_params.get("user_name")
    qp_phone = st.query_params.get("user_phone")

    if qp_name and qp_phone and not st.session_state.authenticated:
        st.session_state.authenticated = True
        st.session_state.user_name = qp_name
        st.session_state.user_phone = qp_phone

sync_authentication()
txt = DICT[st.session_state.language]

# ---------------------------------------------------------------------------
# 4️⃣ Gemini 3.8 Flash Client Initializer
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def init_gemini_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return None
    try:
        return genai.Client(api_key=api_key)
    except Exception:
        return None

gemini_client = init_gemini_client()

# ---------------------------------------------------------------------------
# 5️⃣ SCREEN 1: Sleek Glassmorphic Authentication Console
# ---------------------------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("<div style='max-width: 480px; margin: 8vh auto 0 auto;'>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="glass-panel" style="text-align: center; padding: 2.5rem 2rem;">
            <div style="font-size: 2.8rem; margin-bottom: 0.5rem;">👁️</div>
            <h2 class="brand-title" style="margin: 0; font-size: 2rem;">{txt['login_header']}</h2>
            <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 0.5rem; line-height: 1.5;">{txt['login_sub']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("auth_form", clear_on_submit=False):
        u_name = st.text_input(txt["name_lbl"], placeholder="e.g. Sankar Swain")
        u_phone = st.text_input(txt["phone_lbl"], placeholder="+91 9876543210")
        submit_btn = st.form_submit_button(txt["login_btn"])

        if submit_btn:
            clean_digits = "".join(filter(str.isdigit, u_phone))
            if len(clean_digits) >= 10:
                clean_phone = clean_digits[-10:]
                st.session_state.authenticated = True
                st.session_state.user_name = u_name.strip() if u_name.strip() else "Operator"
                st.session_state.user_phone = clean_phone

                # Persist in URL query parameters
                st.query_params["user_name"] = st.session_state.user_name
                st.query_params["user_phone"] = clean_phone
                st.rerun()
            else:
                st.error(txt["invalid_phone"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ---------------------------------------------------------------------------
# 6️⃣ SCREEN 2: Mission Control Enterprise Workspace
# ---------------------------------------------------------------------------
# Top Navbar: Operator status, language toggle, logout
nav_col1, nav_col2, nav_col3 = st.columns([3, 1.5, 1])

with nav_col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px; margin-top: 4px;">
            <span style="font-weight: 700; color: #94a3b8;">{txt['welcome']}:</span>
            <span class="operator-badge">👤 {st.session_state.user_name} (+91 {st.session_state.user_phone})</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with nav_col2:
    selected_lang = st.selectbox(
        "Language",
        options=["English", "Hindi"],
        index=0 if st.session_state.language == "English" else 1,
        label_visibility="collapsed",
    )
    if selected_lang != st.session_state.language:
        st.session_state.language = selected_lang
        st.rerun()

with nav_col3:
    if st.button(f"🔴 {txt['logout']}"):
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.session_state.user_phone = ""
        st.query_params.clear()
        st.rerun()

st.markdown("<hr style='border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 0.8rem 0 1.5rem 0;'>", unsafe_allow_html=True)

# Main Branding Header
st.markdown(
    f"""
    <div class="glass-panel" style="padding: 1.5rem 2rem; margin-bottom: 1.5rem;">
        <h1 class="brand-title" style="margin: 0; font-size: 2.3rem;">{txt['title']}</h1>
        <p style="margin: 6px 0 0 0; color: #94a3b8; font-size: 1rem; font-weight: 500;">{txt['subtitle']}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inspection Environment Mode
insp_mode = st.radio(
    txt["active_mode"],
    options=[txt["home"], txt["shop"]],
    horizontal=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Streamlined Input Hub: Zero Clutter Camera & File Tabs
input_tab1, input_tab2 = st.tabs([txt["cam_heading"], txt["upload_heading"]])
active_image = None
image_mime_type = "image/jpeg"

with input_tab1:
    camera_file = st.camera_input(txt["cam_btn"], label_visibility="collapsed")
    if camera_file is not None:
        active_image = camera_file
        image_mime_type = "image/jpeg"

with input_tab2:
    uploaded_file = st.file_uploader(
        txt["upload_btn"],
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=False,
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        active_image = uploaded_file
        ext = uploaded_file.name.split(".")[-1].lower()
        image_mime_type = f"image/{ext}" if ext in ["png", "webp", "jpeg"] else "image/jpeg"

# ---------------------------------------------------------------------------
# 7️⃣ Multimodal Gemini Analysis & Robust Backoff Retry Engine
# ---------------------------------------------------------------------------
if active_image is not None:
    st.markdown("<div style='margin-top: 1.2rem;'>", unsafe_allow_html=True)
    run_analysis = st.button(txt["analyze_btn"])
    st.markdown("</div>", unsafe_allow_html=True)

    if run_analysis:
        if not gemini_client:
            st.error("⚠️ GEMINI_API_KEY is not configured or client initialization failed. Please verify your .env file.")
        else:
            with st.spinner(txt["processing"]):
                # Read image bytes
                img_bytes = active_image.getvalue()
                
                # Structured prompt instructing Gemini to reliably extract Expiry Date & clinical/nutrition specs
                system_prompt = (
                    "You are MacroSnap AI, an expert industrial food-safety vision system, clinical nutritionist, and regulatory inspector. "
                    "Analyze the provided product image with high accuracy.\n\n"
                    "CRITICAL MANDATE FOR EXPIRY DATE:\n"
                    "You MUST extract or reliably calculate an EXACT or ESTIMATED Expiry Date / Best Before Date in a clear, readable plain-text format "
                    "(e.g., '24 months from Mfg (Check container base for Batch/Date)' or 'Best Before: 15 Oct 2026'). Never leave expiry unaddressed.\n\n"
                    "Return ONLY a strictly valid JSON object without any Markdown code blocks, HTML tags, or code fences (do NOT use ```json or ```html or ```). "
                    "Include exactly these keys:\n"
                    "- product: (string) Specific product name\n"
                    "- brand: (string) Manufacturer or brand name\n"
                    "- condition: (string) Exactly one of: 'SAFE', 'CAUTION', or 'EXPIRED / UNSAFE'\n"
                    "- expiry_date: (string) EXACT or ESTIMATED Expiry Date / Best Before Date in readable plain text format\n"
                    "- calorific_distribution: (object with keys 'protein', 'carbohydrates', 'fat', 'calories') e.g. {'protein': '27%', 'carbohydrates': '56%', 'fat': '17%', 'calories': '380 kcal / 100g'}\n"
                    "- serving_dosage: (string) Recommended serving and dosage instructions\n"
                    "- clinical_precautions: (list of strings) Clinical precautions, contraindications, or dietary alerts\n"
                    "- standard: (string) Certifications or standards (e.g. 'ISO 22000:2018 | WHO-GMP Certified' or 'FSSAI Grade')\n"
                    "- ingredients: (list of strings) Key ingredients identified\n"
                )

                # Retry logic with exponential backoff
                max_retries = 3
                inspection_data = None
                raw_response_text = ""

                for attempt in range(1, max_retries + 1):
                    try:
                        part = types.Part.from_bytes(data=img_bytes, mime_type=image_mime_type)
                        response = gemini_client.models.generate_content(
                            model="gemini-3.8-flash",
                            contents=[part, system_prompt],
                        )
                        raw_response_text = response.text or ""

                        # Strip any ```html, ```json, or ``` markdown code blocks from LLM output
                        cleaned_text = raw_response_text.strip()
                        if cleaned_text.startswith("```html"):
                            cleaned_text = cleaned_text[7:]
                        elif cleaned_text.startswith("```json"):
                            cleaned_text = cleaned_text[7:]
                        elif cleaned_text.startswith("```"):
                            cleaned_text = cleaned_text[3:]
                        if cleaned_text.endswith("```"):
                            cleaned_text = cleaned_text[:-3]
                        cleaned_text = cleaned_text.strip()

                        try:
                            inspection_data = json.loads(cleaned_text)
                        except Exception:
                            inspection_data = None
                        break  # Successful execution
                    except Exception as exc:
                        if attempt == max_retries:
                            st.error(f"❌ Analysis failed after {max_retries} attempts: {exc}")
                        else:
                            sleep_sec = 2 ** attempt
                            time.sleep(sleep_sec)

                # Render Ultra-High Contrast Inspection Report
                if inspection_data:
                    p_name = inspection_data.get("product") or inspection_data.get("product_name", "Unidentified Item")
                    brand = inspection_data.get("brand", "Unknown Brand")
                    expiry = inspection_data.get("expiry_date", "Check container base for Batch/Date")
                    health_status = (inspection_data.get("condition") or inspection_data.get("health_status", "SAFE")).upper()

                    cal_dist = inspection_data.get("calorific_distribution", {})
                    protein_val = cal_dist.get("protein", "N/A")
                    carbs_val = cal_dist.get("carbohydrates", "N/A")
                    fat_val = cal_dist.get("fat", "N/A")
                    cal_val = cal_dist.get("calories", "N/A")

                    serving = inspection_data.get("serving_dosage", "Follow standard package instructions.")
                    precautions = inspection_data.get("clinical_precautions", [])
                    if not precautions:
                        precautions = inspection_data.get("allergens", ["No special clinical precautions flagged."])
                    standards = inspection_data.get("standard", "ISO 22000:2018 | WHO-GMP Certified")
                    ingr = inspection_data.get("ingredients", [])

                    # Condition badge and emoji styling
                    if "SAFE" in health_status and "UNSAFE" not in health_status:
                        condition_emoji = "🟢"
                        pill_class = "status-safe"
                    elif "EXPIRED" in health_status or "UNSAFE" in health_status:
                        condition_emoji = "🔴"
                        pill_class = "status-danger"
                    else:
                        condition_emoji = "🟡"
                        pill_class = "status-warning"

                    # Format HTML Report without 4-space markdown indentations
                    ingr_str = ", ".join(ingr) if ingr else "Standard formulation"
                    precautions_html = "".join(f"<li>{p}</li>" for p in precautions)

                    report_html = (
                        f'<div class="report-card">'
                        f'<h3>{txt["report_header"]}</h3>'
                        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">'
                        f'<div>'
                        f'<span style="font-size: 1.3rem; font-weight: 800; color: #ffffff;">{p_name}</span>'
                        f'<span style="color: #94a3b8; font-size: 1rem; margin-left: 8px;">({brand})</span>'
                        f'</div>'
                        f'<span class="status-pill {pill_class}">{health_status}</span>'
                        f'</div>'
                        f'<p style="margin: 0.5rem 0;"><b style="color: #38bdf8;">🗓️ {txt["expiry"]}:</b> {expiry}</p>'
                        f'<div style="margin-top: 1rem;">'
                        f'<b style="color: #38bdf8;">📊 {txt["macros"]}:</b>'
                        f'<div class="macro-chip-container">'
                        f'<div class="macro-chip">Protein: <span>{protein_val}</span></div>'
                        f'<div class="macro-chip">Carbohydrates: <span>{carbs_val}</span></div>'
                        f'<div class="macro-chip">Fat: <span>{fat_val}</span></div>'
                        f'<div class="macro-chip">Energy: <span>{cal_val}</span></div>'
                        f'</div>'
                        f'</div>'
                        f'<p style="margin: 0.5rem 0;"><b style="color: #38bdf8;">🥄 Serving & Dosage:</b> {serving}</p>'
                        f'<div style="margin: 0.5rem 0;"><b style="color: #f87171;">⚠️ Clinical Precautions:</b><ul style="margin: 0.3rem 0 0.5rem 1.2rem; padding: 0;">{precautions_html}</ul></div>'
                        f'<p style="margin: 0.5rem 0;"><b style="color: #38bdf8;">📜 Standard:</b> {standards}</p>'
                        f'<p style="margin: 0.5rem 0;"><b style="color: #38bdf8;">🌿 {txt["ingredients"]}:</b> {ingr_str}</p>'
                        f'</div>'
                    )

                    st.markdown(report_html, unsafe_allow_html=True)

                    # -------------------------------------------------------
                    # 8️⃣ Automated WhatsApp Deep-Link Dispatch System (Strictly Plain Text / WhatsApp Markdown)
                    # -------------------------------------------------------
                    wa_phone = f"91{st.session_state.user_phone}" if len(st.session_state.user_phone) == 10 else st.session_state.user_phone
                    precautions_bullets = "\n".join(f"- {p}" for p in precautions)

                    wa_message = (
                        f"📋 MacroSnap AI - Inspection Report\n\n"
                        f"🔹 Product: {p_name}\n"
                        f"🔹 Brand: {brand}\n"
                        f"{condition_emoji} Condition: {health_status}\n\n"
                        f"📅 Expiry / Best Before: {expiry}\n\n"
                        f"📊 Calorific Distribution:\n"
                        f"- Protein: {protein_val}\n"
                        f"- Carbohydrates: {carbs_val}\n"
                        f"- Fat: {fat_val}\n\n"
                        f"🥄 Serving & Dosage:\n"
                        f"{serving}\n\n"
                        f"⚠️ Clinical Precautions:\n"
                        f"{precautions_bullets}\n\n"
                        f"📜 Standard: {standards}"
                    )

                    # Encode strictly plain text with urllib.parse.quote()
                    encoded_msg = quote(wa_message)
                    wa_url = f"https://wa.me/{wa_phone}?text={encoded_msg}"

                    st.markdown(
                        f"""
                        <a href="{wa_url}" target="_blank" class="whatsapp-btn">
                            {txt['send_wa']}
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )
                elif raw_response_text:
                    # Strip any markdown code fences before rendering in Streamlit
                    cleaned_html = raw_response_text.strip()
                    if cleaned_html.startswith("```html"):
                        cleaned_html = cleaned_html[7:]
                    elif cleaned_html.startswith("```json"):
                        cleaned_html = cleaned_html[7:]
                    elif cleaned_html.startswith("```"):
                        cleaned_html = cleaned_html[3:]
                    if cleaned_html.endswith("```"):
                        cleaned_html = cleaned_html[:-3]
                    cleaned_html = cleaned_html.strip()

                    report_html = (
                        f'<div class="report-card">'
                        f'<h3>{txt["report_header"]}</h3>'
                        f'{cleaned_html}'
                        f'</div>'
                    )
                    st.markdown(report_html, unsafe_allow_html=True)

                    # Clean plain text for WhatsApp - strictly strip ALL HTML tags
                    clean_wa_text = re.sub(r'<br\s*/?>', '\n', cleaned_html, flags=re.IGNORECASE)
                    clean_wa_text = re.sub(r'</p>', '\n\n', clean_wa_text, flags=re.IGNORECASE)
                    clean_wa_text = re.sub(r'</li>', '\n', clean_wa_text, flags=re.IGNORECASE)
                    clean_wa_text = re.sub(r'<[^>]+>', '', clean_wa_text).strip()

                    wa_phone = f"91{st.session_state.user_phone}" if len(st.session_state.user_phone) == 10 else st.session_state.user_phone
                    wa_message = f"📋 MacroSnap AI - Inspection Report\n\n{clean_wa_text}"
                    encoded_msg = quote(wa_message)
                    wa_url = f"https://wa.me/{wa_phone}?text={encoded_msg}"

                    st.markdown(
                        f"""
                        <a href="{wa_url}" target="_blank" class="whatsapp-btn">
                            {txt['send_wa']}
                        </a>
                        """,
                        unsafe_allow_html=True,
                    )
else:
    st.markdown(
        f"""
        <div class="glass-panel" style="text-align: center; padding: 2rem; color: #94a3b8;">
            <p style="margin: 0; font-size: 1rem; font-weight: 500;">{txt['no_image']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )