"""
Training Feedback Survey Application - Home Page.

This is the main landing page featuring the AI introduction and navigation.
"""

from pathlib import Path
from typing import Optional
import streamlit as st

st.set_page_config(page_title="Training Feedback Survey", layout="wide")

_ASSETS_DIR = Path(__file__).resolve().parent / "assets"
_VIDEO_CANDIDATES = [
    "avatar_intro.mp4",
    "Survey Intro.mp4",
]


def _is_valid_media(path: Path) -> bool:
    try:
        return path.exists() and path.stat().st_size > 0
    except OSError:
        return False


def _find_avatar_video() -> Optional[Path]:
    for candidate in _VIDEO_CANDIDATES:
        video_path = _ASSETS_DIR / candidate
        if _is_valid_media(video_path):
            return video_path

    fallback_videos = sorted(
        (
            video
            for video in _ASSETS_DIR.glob("*.mp4")
            if video.name not in _VIDEO_CANDIDATES and _is_valid_media(video)
        ),
        key=lambda video: video.stat().st_mtime,
        reverse=True,
    )

    return fallback_videos[0] if fallback_videos else None

def _get_asset_path(filename: str) -> Path:
    return _ASSETS_DIR / filename

# Enhanced styling with tan clipboard design
st.markdown(
    """
    <style>
        /* Main background with Results page color scheme */
        .stApp {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
            min-height: 100vh;
            position: relative;
        }

        /* Constrain main column for large screens and improve horizontal rhythm */
        main .block-container {
            max-width: min(1100px, 96vw);
            margin: 0 auto;
            padding: clamp(1.25rem, 2vw, 2.25rem) clamp(0.75rem, 4vw, 2.25rem) 4rem;
        }
        
        /* Header styling with gradient glowing effect */
        .main-header {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 50%, #2F1B14 100%);
            background-size: 200% 200%;
            animation: gradientShift 4s ease infinite;
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            margin: 2rem 1rem;
            box-shadow: 
                0 0 20px rgba(139, 38, 53, 0.4),
                0 0 40px rgba(47, 27, 20, 0.3),
                0 0 60px rgba(139, 38, 53, 0.2),
                0 8px 32px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            position: relative;
            overflow: hidden;
        }
        
        .main-header::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: rotate 8s linear infinite;
            pointer-events: none;
        }
        
        .main-header h1 {
            color: white;
            margin: 0;
            font-size: 2.5em;
            text-shadow: 
                0 0 10px rgba(255,255,255,0.5),
                2px 2px 4px rgba(0,0,0,0.7);
            position: relative;
            z-index: 2;
        }
        
        .main-header h3 {
            color: rgba(255,255,255,0.95);
            margin: 10px 0 0 0;
            font-weight: 300;
            text-shadow: 
                1px 1px 2px rgba(0,0,0,0.5);
            position: relative;
            z-index: 2;
        }
        
        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Content containers with Results page color scheme */
        .content-container {
            background: linear-gradient(135deg, #FFFEF7 0%, #F8F6F0 100%);
            padding: 2rem;
            border-radius: 8px;
            margin: 1.5rem auto;
            max-width: 900px;
            box-shadow: 
                0 4px 15px rgba(139, 38, 53, 0.2),
                inset 0 1px 0 rgba(255,255,255,0.8);
            border: 1px solid #8B2635;
            position: relative;
        }
        
        .content-container::before {
            content: '';
            position: absolute;
            left: 2rem;
            top: 0;
            bottom: 0;
            width: 1px;
            background: #D8C4C8;
            opacity: 0.7;
        }
        
        /* Enhanced text visibility */
        .content-container h3 {
            color: #000000 !important;
            text-align: center;
            margin-bottom: 1rem;
            font-weight: 700;
            text-shadow: 1px 1px 2px rgba(255,255,255,0.8);
        }
        
        /* Gradient burgundy section header banners */
        .gradient-header {
            background: linear-gradient(135deg, #8B2635 0%, #2F1B14 50%, #8B2635 100%);
            background-size: 200% 200%;
            animation: gradientText 3s ease infinite;
            color: white;
            text-align: center;
            font-weight: 700;
            font-size: 1.3em;
            margin: 2rem auto 1rem auto;
            padding: 1.5rem 2rem;
            border-radius: 12px;
            box-shadow: 
                0 0 15px rgba(139, 38, 53, 0.3),
                0 0 30px rgba(47, 27, 20, 0.2),
                0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.2);
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            max-width: 900px;
        }
        
        @keyframes gradientText {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        .content-container p,
        .content-container div,
        .content-container li {
            color: #2F1B14 !important;
            line-height: 1.6;
            font-weight: 500;
            text-shadow: none;
        }
        
        /* Flush-aligned text under banners */
        .banner-text {
            color: #FFFFFF !important;
            text-align: left;
            margin: 1rem auto;
            padding: 0 2rem;
            line-height: 1.6;
            font-weight: 600;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
            max-width: 900px;
        }

        .banner-text--indented {
            padding-left: clamp(1.5rem, 5vw, 4rem);
        }
        
        /* Centered button container */
        /* Centered QR Code styling */
        .qr-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 2rem auto;
            text-align: center;
            max-width: 320px;
            width: 100%;
        }
        
        .qr-caption {
            color: #FFFFFF !important;
            font-weight: 600;
            font-size: 1.1em;
            margin-top: 1rem;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        
        /* General text styling for better visibility on burgundy background */
        p, div:not(.stButton) {
            color: #F9F5F2 !important;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }

        .stVideo iframe, .stVideo video {
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            width: 100% !important;
            min-height: clamp(220px, 45vw, 420px);
        }

        .qr-container img {
            border-radius: 12px;
            box-shadow: 0 6px 30px rgba(0,0,0,0.35);
            width: 100%;
            height: auto;
            max-width: 260px;
        }
        
        /* Navigation buttons with Results page style */
        .stButton > button {
            background: linear-gradient(135deg, #2F1B14 0%, #8B2635 100%);
            color: white !important;
            border: 2px solid #8B2635;
            border-radius: 8px;
            padding: 1rem 2rem;
            font-size: 1.1em;
            font-weight: 600;
            box-shadow: 
                0 4px 15px rgba(139, 38, 53, 0.3),
                inset 0 1px 0 rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            width: 100%;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 6px 20px rgba(139, 38, 53, 0.4),
                inset 0 1px 0 rgba(255,255,255,0.3);
            background: linear-gradient(135deg, #8B2635 0%, #2F1B14 100%);
        }

        /* Responsive layout adjustments */
        @media (max-width: 1024px) {
            main .block-container {
                padding: 1.5rem 1.5rem 3rem;
            }

            .main-header {
                margin: 1.5rem auto;
                padding: 1.75rem 1.25rem;
            }

            .gradient-header {
                margin: 1.5rem auto 0.75rem auto;
                padding: 1.25rem 1.5rem;
            }

        }

        @media (max-width: 768px) {
            main .block-container {
                padding: 1.25rem 0.85rem 2.5rem;
            }

            .main-header {
                margin: 1rem auto;
                padding: 1.5rem 1rem;
            }

            .main-header h1 {
                font-size: 1.9em;
            }

            .main-header h3 {
                font-size: 1.1em;
            }

            .gradient-header {
                font-size: 1.1em;
                margin: 1.25rem auto 0.5rem auto;
                padding: 1rem 1.15rem;
            }

            .banner-text {
                margin: 0.85rem auto;
                padding: 0 1rem;
                text-align: center;
            }

            .banner-text--indented {
                padding-left: 1rem;
            }

            .content-container {
                margin: 1rem auto;
                padding: 1.5rem;
            }

            .content-container::before {
                display: none;
            }

            .qr-container {
                margin: 1.5rem 0;
                max-width: 240px;
            }

            .stButton > button {
                font-size: 1em;
                padding: 0.9rem 1.25rem;
            }

            [data-testid="column"] {
                flex: 1 1 100% !important;
                min-width: 100% !important;
            }
        }

        @media (max-width: 540px) {
            main .block-container {
                padding: 1.1rem 0.65rem 2.25rem;
            }

            .main-header h1 {
                font-size: 1.7em;
            }

            .gradient-header {
                padding: 0.9rem 1rem;
            }

            .stButton > button {
                padding: 0.85rem 1.1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Enhanced banner header
st.markdown(
    """
    <div class="main-header">
        <h1>📊 Training Feedback Survey</h1>
        <h3>Excellence Through Training!</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# AI Introduction Video Section
st.markdown('<div class="gradient-header">🤖 Meet Your AI Survey Assistant</div>', unsafe_allow_html=True)

video_file = _find_avatar_video()
if video_file:
    st.video(str(video_file))
else:
    st.info("🎬 AI Introduction Video will be displayed here")
    st.markdown(
        "*Place your video in the 'assets' folder (e.g., avatar_intro.mp4 or Survey Intro.mp4).*"
    )

st.markdown('<div class="gradient-header">📋 Survey System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="banner-text">This application helps us gather valuable feedback about our training programs to continuously improve the quality and effectiveness of our training offerings.</div>',
    unsafe_allow_html=True
)

# How to Use This System
st.markdown('<div class="gradient-header">🚀 How To Use This System:</div>', unsafe_allow_html=True)

# Center navigation buttons with responsive column layout
col_take, col_results = st.columns(2, gap="large")
with col_take:
    if st.button(
        "📝 Take Survey",
        key="survey_nav",
        help="Complete the comprehensive training feedback survey",
        use_container_width=True,
    ):
        st.switch_page("pages/2_Survey.py")

with col_results:
    if st.button(
        "📊 View Results",
        key="results_nav",
        help="Analyze survey results and trends (for administrators)",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Results.py")

# Getting Started Section
st.markdown('<div class="gradient-header">🎯 Getting Started</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="banner-text banner-text--indented">In case you missed the instructions from our AI Assistant, please scan the QR Code below for quick access to the survey.</div>',
    unsafe_allow_html=True
)

# QR Code positioned to align right edge with "Started" text
qr_path = _get_asset_path("survey_qr.png")
if qr_path.exists():
    qr_left, qr_center, qr_right = st.columns([1, 1.1, 1])
    with qr_center:
        st.image(
            str(qr_path),
            use_container_width=True,
            caption="Scan for quick access or visit survey.soulwaresystems.com",
        )
else:
    st.info("🧾 QR Code will be displayed here (assets/survey_qr.png)")
