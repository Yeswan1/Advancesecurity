import sys
import os
import certifi
import pandas as pd
import streamlit as st

from dotenv import load_dotenv
from src.exception.customexception import NetworkSecurityException
from src.utilsfile.util  import load_object
from src.utilsfile.metrics.me import NetworkModel

# MongoDB connection
import pymongo
ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")
try:
    client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca) if mongo_db_url else None
except Exception:
    client = None

from src.constant.trainpipeline import (
    DATA_INGESTION_DATABASE,
    DATA_INGESTION_COLLECTION,
)

database = client[DATA_INGESTION_DATABASE] if client else None
collection = database[DATA_INGESTION_COLLECTION] if database else None


# ---------------- Streamlit UI ----------------
st.set_page_config(page_title="Network Security checker", layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: var(--background-color);
        color: var(--text-color);
        font-size: 16px;
        font-family: "Segoe UI", "Trebuchet MS", sans-serif;
    }
    [data-testid="stAppViewContainer"] {
        background: var(--background-color);
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    .stMarkdown p, .stMarkdown li, .stCaption, .stText {
        color: var(--text-color);
        font-size: 15px;
        line-height: 1.5;
    }
    .hero {
        background: linear-gradient(120deg, #0f4c81 0%, #136f63 100%);
        border-radius: 16px;
        padding: 20px 24px;
        color: #ffffff;
        box-shadow: 0 10px 24px rgba(15, 76, 129, 0.25);
        margin-bottom: 14px;
    }
    .hero h1 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
    .hero p {
        margin: 8px 0 0 0;
        font-size: 15px;
        opacity: 0.95;
    }
    .panel {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #dbe8f5;
        border-radius: 12px;
        padding: 14px 16px;
        box-shadow: 0 4px 14px rgba(16, 24, 40, 0.05);
        margin-bottom: 12px;
    }
    .pill {
        display: inline-block;
        background: #e9f5ff;
        color: #0f4c81;
        border: 1px solid #b7daf7;
        padding: 4px 10px;
        border-radius: 999px;
        margin: 4px 6px 0 0;
        font-size: 13px;
        font-weight: 600;
    }
    .helper {
        background: #f8fcff;
        border: 1px solid #d8ebff;
        border-radius: 10px;
        padding: 10px 12px;
        margin: 8px 0 10px 0;
        color: #1e3a5f;
        font-size: 14px;
    }
    .label-safe {
        display: inline-block;
        background: #e8f8ef;
        color: #136f3a;
        border: 1px solid #9fd8b3;
        border-radius: 8px;
        padding: 4px 10px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .label-phish {
        display: inline-block;
        background: #fdecec;
        color: #b42318;
        border: 1px solid #f5b5af;
        border-radius: 8px;
        padding: 4px 10px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-weight: 700;
    }
    .label-unknown {
        display: inline-block;
        background: #eef2f7;
        color: #344054;
        border: 1px solid #d0d5dd;
        border-radius: 8px;
        padding: 4px 10px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-weight: 700;
    }

    /* Dark mode support when Streamlit theme is Dark */
    [data-theme="dark"] .stApp,
    [data-theme="dark"] [data-testid="stAppViewContainer"] {
        background: linear-gradient(160deg, #0b1220 0%, #101827 45%, #111827 100%);
        color: #e5e7eb;
    }
    [data-theme="dark"] .stMarkdown p,
    [data-theme="dark"] .stMarkdown li,
    [data-theme="dark"] .stCaption,
    [data-theme="dark"] .stText,
    [data-theme="dark"] h1,
    [data-theme="dark"] h2,
    [data-theme="dark"] h3,
    [data-theme="dark"] h4 {
        color: #e5e7eb;
    }
    [data-theme="dark"] .panel {
        background: rgba(17, 24, 39, 0.88);
        border: 1px solid #334155;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.35);
    }
    [data-theme="dark"] .pill {
        background: #1f2937;
        color: #cde7ff;
        border: 1px solid #334155;
    }
    [data-theme="dark"] .helper {
        background: #111827;
        border: 1px solid #334155;
        color: #cbd5e1;
    }
    [data-theme="dark"] .label-safe {
        background: #123222;
        color: #7ee2a8;
        border-color: #1f5d40;
    }
    [data-theme="dark"] .label-phish {
        background: #3a1618;
        color: #ffb4ae;
        border-color: #7f1d1d;
    }
    [data-theme="dark"] .label-unknown {
        background: #1f2937;
        color: #cbd5e1;
        border-color: #475569;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Network Security Threat Detector</h1>
        <p>Upload network feature data or enter values manually to get ML-based threat predictions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader("Predict Network Security")
st.markdown(
    '<span class="label-safe">Class 1 = Legitimate URL</span>'
    '<span class="label-phish">Class 0 = Phishing URL</span>',
    unsafe_allow_html=True,
)

status_col1, status_col2, status_col3 = st.columns(3)
status_col1.metric("Detection Engine", "Active")
status_col2.metric("Input Modes", "2")
status_col3.metric("Model Type", "Binary Classifier")


def load_input_file(uploaded_file):
    file_name = uploaded_file.name.lower()
    if file_name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    if file_name.endswith(".xlsx") or file_name.endswith(".xls"):
        return pd.read_excel(uploaded_file)
    raise ValueError("Unsupported file type. Please upload CSV or Excel file.")


def prediction_text(value):
    if int(value) == 1:
        return "Legitimate URL"
    if int(value) == 0:
        return "Phishing URL"
    return f"Unknown Class ({value})"


def prediction_badge_html(value):
    class_value = int(value)
    if class_value == 1:
        return '<span class="label-safe">Class 1 = Legitimate URL</span>'
    if class_value == 0:
        return '<span class="label-phish">Class 0 = Phishing URL</span>'
    return f'<span class="label-unknown">Class {class_value} = Unknown</span>'


def get_manual_default_row(expected_features, preset_name):
    neutral_row = {feature: 0 for feature in expected_features}

    safe_example = {
        "having_IP_Address": 1,
        "URL_Length": -1,
        "Shortining_Service": 1,
        "having_At_Symbol": 1,
        "double_slash_redirecting": 1,
        "Prefix_Suffix": -1,
        "having_Sub_Domain": 1,
        "SSLfinal_State": 1,
        "Domain_registeration_length": 1,
        "Favicon": 1,
        "port": 1,
        "HTTPS_token": -1,
        "Request_URL": -1,
        "URL_of_Anchor": 1,
        "Links_in_tags": 1,
        "SFH": 0,
        "Submitting_to_email": 1,
        "Abnormal_URL": 1,
        "Redirect": 0,
        "on_mouseover": 1,
        "RightClick": 1,
        "popUpWidnow": 1,
        "Iframe": 1,
        "age_of_domain": 1,
        "DNSRecord": 1,
        "web_traffic": -1,
        "Page_Rank": -1,
        "Google_Index": 1,
        "Links_pointing_to_page": 1,
        "Statistical_report": 1,
    }

    suspicious_example = {
        "having_IP_Address": -1,
        "URL_Length": -1,
        "Shortining_Service": -1,
        "having_At_Symbol": 1,
        "double_slash_redirecting": -1,
        "Prefix_Suffix": -1,
        "having_Sub_Domain": 0,
        "SSLfinal_State": 0,
        "Domain_registeration_length": 1,
        "Favicon": 1,
        "port": 1,
        "HTTPS_token": -1,
        "Request_URL": -1,
        "URL_of_Anchor": -1,
        "Links_in_tags": 1,
        "SFH": -1,
        "Submitting_to_email": 1,
        "Abnormal_URL": -1,
        "Redirect": 1,
        "on_mouseover": 1,
        "RightClick": 1,
        "popUpWidnow": 1,
        "Iframe": 1,
        "age_of_domain": 1,
        "DNSRecord": 1,
        "web_traffic": -1,
        "Page_Rank": -1,
        "Google_Index": 1,
        "Links_pointing_to_page": 0,
        "Statistical_report": 1,
    }

    if preset_name == "Likely Safe Example":
        neutral_row.update({k: v for k, v in safe_example.items() if k in neutral_row})
    elif preset_name == "Likely Suspicious Example":
        neutral_row.update({k: v for k, v in suspicious_example.items() if k in neutral_row})

    return neutral_row

try:
    preprocessor = load_object("final_model/preprocessor.pkl")
    final_model = load_object("final_model/model.pkl")
    network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
    expected_features = list(getattr(preprocessor, "feature_names_in_", []))

    st.write("### Step 1: Choose Prediction Mode")
    st.write("1. Upload your file (CSV/Excel) or use demo file")
    st.write("2. Enter values manually (single row)")
    input_mode = st.radio(
        "Prediction options",
        ["Upload File (CSV/Excel)", "Enter Values Manually"],
        horizontal=True,
    )

    df_for_result = None
    model_input_df = None

    with st.expander("Step 2: View Required Model Columns", expanded=False):
        if expected_features:
            for col in expected_features:
                st.markdown(f'<span class="pill">{col}</span>', unsafe_allow_html=True)
        else:
            st.warning("Could not load feature names from preprocessor.")

    if input_mode == "Upload File (CSV/Excel)":
        demo_file_path = "prediction_output/demo_input.csv"
        source_mode = st.radio(
            "File source",
            ["Upload My File", "Use Demo Input File"],
            horizontal=True,
        )

        if source_mode == "Upload My File":
            uploaded_file = st.file_uploader(
                "Upload CSV or Excel file",
                type=["csv", "xlsx", "xls"],
            )

            if uploaded_file is not None:
                uploaded_df = load_input_file(uploaded_file)
                uploaded_df = uploaded_df.loc[:, ~uploaded_df.columns.str.startswith("Unnamed")]
                st.write("### Uploaded Data")
                st.dataframe(uploaded_df.head())
                model_input_df = uploaded_df.drop(columns=["predicted_column", "Result"], errors="ignore")
                df_for_result = uploaded_df.copy()

        else:
            if os.path.exists(demo_file_path):
                demo_df = pd.read_csv(demo_file_path)
                st.success(f"Demo file loaded: {demo_file_path}")
                st.write("### Demo Input Preview")
                st.dataframe(demo_df.head())
                st.download_button(
                    label="Download Demo Input File",
                    data=demo_df.to_csv(index=False).encode("utf-8"),
                    file_name="demo_input.csv",
                    mime="text/csv",
                )
                model_input_df = demo_df.drop(columns=["predicted_column", "Result"], errors="ignore")
                df_for_result = demo_df.copy()
            else:
                st.warning(
                    f"Demo file not found at {demo_file_path}. Add your demo file there to enable one-click demo prediction."
                )

        if model_input_df is not None and expected_features:
            missing_features = [col for col in expected_features if col not in model_input_df.columns]
            if missing_features:
                st.error(f"Missing required columns: {missing_features}")
                st.stop()

            extra_features = [col for col in model_input_df.columns if col not in expected_features]
            if extra_features:
                st.info(f"Ignoring extra columns not used by model: {extra_features}")

            model_input_df = model_input_df[expected_features]

    else:
        if not expected_features:
            st.error("Model feature names are not available. Please retrain the model.")
            st.stop()

        st.write("### Enter Values for Prediction")
        default_preset = st.selectbox(
            "Default values preset",
            ["Neutral (all 0)", "Likely Safe Example", "Likely Suspicious Example"],
            index=0,
        )

        st.markdown(
            """
            <div class="helper">
                Manual input tips: values are usually <b>-1</b>, <b>0</b>, or <b>1</b>.
                You can start from a preset and edit one row before clicking Predict.
            </div>
            """,
            unsafe_allow_html=True,
        )

        manual_df = pd.DataFrame([get_manual_default_row(expected_features, default_preset)])
        st.caption("Manual mode supports exactly one row.")
        edited_df = st.data_editor(manual_df, num_rows="fixed", use_container_width=True)

        if edited_df.shape[0] != 1:
            st.error("Manual mode supports exactly one row only.")
            st.stop()

        for col in expected_features:
            edited_df[col] = pd.to_numeric(edited_df[col], errors="coerce")

        if edited_df[expected_features].isnull().any().any():
            st.warning("Please fill all values with numeric data before prediction.")
        else:
            model_input_df = edited_df[expected_features].copy()
            df_for_result = edited_df.copy()

    if "latest_prediction_df" not in st.session_state:
        st.session_state["latest_prediction_df"] = None

    predict_clicked = st.button("Predict", type="primary", key="predict_btn")

    if not predict_clicked:
        # Never show old predictions unless user clicks Predict in this run.
        st.session_state["latest_prediction_df"] = None

    if predict_clicked:
        if model_input_df is None or df_for_result is None:
            st.warning("Please provide valid input data first.")
        else:
            y_pred = network_model.predict(model_input_df)
            df_for_result["predicted_column"] = y_pred
            df_for_result["predicted_label"] = df_for_result["predicted_column"].apply(prediction_text)
            st.session_state["latest_prediction_df"] = df_for_result.copy()

            os.makedirs("prediction_output", exist_ok=True)
            output_path = "prediction_output/output.csv"
            df_for_result.to_csv(output_path, index=False)

            st.write("### Prediction Summary")
            if len(df_for_result) == 1:
                single_class = int(df_for_result.loc[df_for_result.index[0], "predicted_column"])
                st.metric("Predicted Class", f"{single_class}")
                st.markdown(prediction_badge_html(single_class), unsafe_allow_html=True)
                if single_class == 1:
                    st.success("Result: Legitimate URL")
                elif single_class == 0:
                    st.error("Result: Phishing URL")
                else:
                    st.warning(f"Result: Unknown Class ({single_class})")
            else:
                class_counts = df_for_result["predicted_column"].value_counts().sort_index()
                cols = st.columns(len(class_counts))
                for idx, (class_value, class_count) in enumerate(class_counts.items()):
                    cols[idx].metric(f"Class {int(class_value)}", int(class_count))
                unique_classes = sorted(df_for_result["predicted_column"].astype(int).unique())
                badges_html = "".join(prediction_badge_html(class_value) for class_value in unique_classes)
                st.markdown(badges_html, unsafe_allow_html=True)

            st.caption("Legend: Class 1 = Legitimate URL, Class 0 = Phishing URL.")

            st.write("### Prediction Results")
            st.dataframe(df_for_result)

            st.write("### Predicted Column Output")
            st.dataframe(df_for_result[["predicted_column", "predicted_label"]])

            st.success(f"Predictions saved to {output_path}")

            st.download_button(
                label="Download Predictions",
                data=df_for_result.to_csv(index=False).encode("utf-8"),
                file_name="predictions.csv",
                mime="text/csv",
            )

except Exception as e:
    st.error(f"Prediction failed: {e}")
    raise NetworkSecurityException(e, sys)
