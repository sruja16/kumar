import streamlit as st
from PIL import Image

from backend import detect_pest, get_advice


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgroSight AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ============================================================
   MAIN APP
   ============================================================ */

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(34, 197, 94, 0.12),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 10%,
            rgba(16, 185, 129, 0.10),
            transparent 30%
        ),
        #06130d;
}

.main .block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #071d13,
            #03110a
        );

    border-right: 1px solid rgba(74, 222, 128, 0.18);
}


/* ============================================================
   HEADINGS
   ============================================================ */

h1, h2, h3 {
    color: #ecfdf5 !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero-container {
    background:
        linear-gradient(
            135deg,
            #064e3b,
            #166534
        );

    border-radius: 28px;

    padding: 45px 30px;

    text-align: center;

    border: 1px solid rgba(134, 239, 172, 0.28);

    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.35);

    margin-bottom: 30px;
}


/* ============================================================
   UPLOAD
   ============================================================ */

[data-testid="stFileUploader"] {
    background: rgba(15, 23, 42, 0.55);

    border: 1px dashed rgba(134, 239, 172, 0.30);

    border-radius: 18px;

    padding: 12px;
}


/* ============================================================
   CONTAINERS
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(
            145deg,
            rgba(15, 23, 42, 0.90),
            rgba(8, 30, 20, 0.88)
        ) !important;

    border:
        1px solid rgba(134, 239, 172, 0.14) !important;

    border-radius: 20px !important;

    box-shadow:
        0 12px 35px rgba(0,0,0,0.20);
}


/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    width: 100%;

    min-height: 45px;

    border-radius: 12px;

    border: 1px solid rgba(74, 222, 128, 0.35);

    background:
        linear-gradient(
            135deg,
            #16a34a,
            #059669
        );

    color: white;

    font-weight: 700;
}

.stButton > button:hover {
    border-color: #86efac;

    box-shadow:
        0 8px 25px rgba(34,197,94,0.25);
}


/* ============================================================
   INFO
   ============================================================ */

[data-testid="stCaptionContainer"] {
    color: #94a3b8;
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer-line {
    margin-top: 50px;

    border-top: 1px solid rgba(148,163,184,0.12);

    padding-top: 25px;

    text-align: center;

    color: #64748b;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🌱 AgroSight AI"
    )

    st.caption(
        "Intelligent Pest Detection & Crop Protection"
    )

    st.divider()

    st.markdown(
        "### 🤖 How It Works"
    )

    st.markdown(
        """
        **📷 Step 1 — Upload**

        Upload a crop or pest image.

        **👁️ Step 2 — Detect**

        YOLOv8 analyzes the image.

        **🧠 Step 3 — Analyze**

        Gemini identifies the pest.

        **🌱 Step 4 — Protect**

        Get treatment and prevention recommendations.
        """
    )

    st.divider()

    st.markdown(
        "### 💡 Image Tips"
    )

    st.info(
        "Use a clear image with good lighting. "
        "Make sure the pest is visible."
    )

    st.divider()

    st.caption(
        "AgroSight AI\n\n"
        "YOLOv8 + Generative AI"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-container">',
    unsafe_allow_html=True
)

st.markdown(
    "# 🌾 AgroSight AI"
)

st.markdown(
    "### AI-Powered Pest Detection & Crop Protection"
)

st.write(
    "⚡ YOLOv8  •  🧠 Generative AI  •  🌱 Smart Agriculture"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# UPLOAD SECTION
# ============================================================

st.header(
    "📷 Analyze Your Crop"
)

st.write(
    "Upload an image of a crop, leaf, or suspected pest "
    "to start AI-powered analysis."
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp"
    ]
)


# ============================================================
# IF IMAGE UPLOADED
# ============================================================

if uploaded_file is not None:

    try:

        image = Image.open(
            uploaded_file
        ).convert("RGB")

    except Exception:

        st.error(
            "❌ Unable to read this image."
        )

        st.stop()


    st.divider()

    st.header(
        "🔍 Image Analysis"
    )


    # ========================================================
    # ORIGINAL IMAGE + DETECTION
    # ========================================================

    image_col, detection_col = st.columns(
        2,
        gap="large"
    )


    # --------------------------------------------------------
    # ORIGINAL
    # --------------------------------------------------------

    with image_col:

        st.subheader(
            "📷 Original Image"
        )

        with st.container(
            border=True
        ):

            st.image(
                image,
                use_container_width=True
            )


    # --------------------------------------------------------
    # YOLO
    # --------------------------------------------------------

    with st.spinner(
        "🤖 YOLOv8 is analyzing the image..."
    ):

        frame, pest_name = detect_pest(
            image
        )


    with detection_col:

        st.subheader(
            "🎯 AI Detection"
        )

        with st.container(
            border=True
        ):

            if pest_name:

                st.image(
                    frame,
                    channels="BGR",
                    use_container_width=True
                )

            else:

                st.warning(
                    "No pest was detected."
                )


    # ========================================================
    # PEST DETECTED
    # ========================================================

    if pest_name:

        st.divider()

        st.success(
            f"🐛 Pest Detected: {pest_name}"
        )


        st.subheader(
            "🧠 AI Detection Result"
        )

        result_col1, result_col2, result_col3 = st.columns(
            3
        )


        with result_col1:

            with st.container(
                border=True
            ):

                st.markdown(
                    "### 🐛"
                )

                st.caption(
                    "DETECTED PEST"
                )

                st.markdown(
                    f"**{pest_name}**"
                )


        


        # ====================================================
        # GEMINI
        # ====================================================

        with st.spinner(
            "🧠 Generating crop protection recommendations..."
        ):

            advice = get_advice(
                pest_name
            )


        # ====================================================
        # ERROR
        # ====================================================

        if not isinstance(
            advice,
            dict
        ):

            st.error(
                "Unexpected response from Gemini."
            )

            st.write(
                advice
            )


        elif "error" in advice:

            st.error(
                "❌ Unable to generate crop protection advice."
            )

            with st.expander(
                "Technical details"
            ):

                st.write(
                    advice
                )


        # ====================================================
        # SUCCESS
        # ====================================================

        else:

            st.divider()

            st.header(
                "🌱 Crop Protection Report"
            )

            st.caption(
                "AI-generated information about the detected pest"
            )


            # =================================================
            # BASIC INFORMATION
            # =================================================

            st.subheader(
                "🔬 Pest Information"
            )


            info1, info2, info3 = st.columns(
                3,
                gap="medium"
            )


            with info1:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🔬 Scientific Name"
                    )

                    st.write(
                        advice.get(
                            "pest",
                            "N/A"
                        )
                    )


            with info2:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🐛 English Name"
                    )

                    st.write(
                        advice.get(
                            "common_name_en",
                            "N/A"
                        )
                    )


            with info3:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🇮🇳 Hindi Name"
                    )

                    st.write(
                        advice.get(
                            "common_name_hi",
                            "N/A"
                        )
                    )


            st.markdown("")


            # =================================================
            # RECOMMENDATIONS
            # =================================================

            st.subheader(
                "🛡️ Crop Protection Recommendations"
            )


            left, right = st.columns(
                2,
                gap="large"
            )


            # -------------------------------------------------
            # CHEMICAL
            # -------------------------------------------------

            with left:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 💊 Chemical Solution"
                    )

                    st.write(
                        advice.get(
                            "chemical",
                            "N/A"
                        )
                    )


            # -------------------------------------------------
            # PREVENTION
            # -------------------------------------------------

            with right:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🛡️ Prevention Strategy"
                    )

                    st.write(
                        advice.get(
                            "prevention",
                            "N/A"
                        )
                    )


            # -------------------------------------------------
            # ORGANIC
            # -------------------------------------------------

            with left:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🌿 Organic Solution"
                    )

                    st.write(
                        advice.get(
                            "organic",
                            "N/A"
                        )
                    )


            # -------------------------------------------------
            # CROP STAGE
            # -------------------------------------------------

            with right:

                with st.container(
                    border=True
                ):

                    st.markdown(
                        "### 🌾 Crop Stage"
                    )

                    st.write(
                        advice.get(
                            "crop_stage",
                            "N/A"
                        )
                    )


            # =================================================
            # WARNING
            # =================================================

            st.warning(
                "⚠️ AI-generated agricultural advice is for "
                "guidance only. Always follow the pesticide "
                "product label and consult a qualified local "
                "agricultural professional before applying "
                "chemical treatments."
            )


            # =================================================
            # NEW ANALYSIS
            # =================================================

            st.divider()

            if st.button(
                "🔄 Analyze Another Image",
                use_container_width=True
            ):

                st.rerun()


# ============================================================
# EMPTY STATE
# ============================================================

else:

    st.divider()

    empty1, empty2, empty3 = st.columns(
        [1, 2, 1]
    )

    with empty2:

        with st.container(
            border=True
        ):

            st.markdown(
                "## 🌱 Ready to Protect Your Crops?"
            )

            st.write(
                "Upload a crop or pest image above "
                "to begin AI-powered analysis."
            )

            st.info(
                "💡 Best results come from clear images "
                "with the pest clearly visible."
            )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer-line">'
    '<b>AgroSight AI</b> · '
    'Intelligent Pest Detection & Crop Protection'
    '<br>'
    'Powered by YOLOv8 Computer Vision & Generative AI'
    '</div>',
    unsafe_allow_html=True
)