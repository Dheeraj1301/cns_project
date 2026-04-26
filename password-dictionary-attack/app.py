"""Streamlit app: Password Cracking using Dictionary Attack (Educational Only)."""

from __future__ import annotations

import io
from typing import List

import pandas as pd
import plotly.express as px
import streamlit as st

from backend.cracker import dictionary_attack
from backend.hash_utils import SUPPORTED_ALGORITHMS, hash_password
from backend.sample_data import load_default_dictionary


st.set_page_config(
    page_title="Password Cracking using Dictionary Attack",
    page_icon="🔐",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 45%, #7e22ce 100%);
        color: #ffffff;
    }
    .card {
        background: rgba(255, 255, 255, 0.12);
        border-radius: 14px;
        padding: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        margin-bottom: 14px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    .warning-card {
        background: rgba(239, 68, 68, 0.20);
        border-left: 5px solid #fecaca;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔐 Password Cracking using Dictionary Attack")
st.caption("A safe, offline educational prototype for defensive cybersecurity learning.")

st.markdown(
    """
    <div class="warning-card">
    ⚠️ <b>Ethical Use Notice:</b> This app is for education only. Use only local, user-provided data.
    Do not use this project to target real systems, accounts, or external services.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("🧭 Navigation")
    st.write("Use the tabs in the main area:")
    st.write("• Generate Hash")
    st.write("• Dictionary Attack")
    st.write("• How It Works")

    algorithm = st.selectbox(
        "Select hashing algorithm",
        ["md5", "sha1", "sha256"],
        index=2,
        help="Choose which hash algorithm to use for generation and attack.",
    )

    st.info("Supported algorithms: MD5, SHA1, SHA256")


gen_tab, attack_tab, info_tab = st.tabs(["Generate Hash", "Dictionary Attack", "How It Works"])

with gen_tab:
    st.subheader("🧪 Generate Hash")
    st.markdown('<div class="card">Create a hash from a plain password.</div>', unsafe_allow_html=True)

    plain_password = st.text_input("Enter plain password", type="password", key="plain_password")

    if st.button("Generate Hash", type="primary"):
        if not plain_password:
            st.error("Please enter a password to hash.")
        else:
            try:
                generated = hash_password(plain_password, algorithm)
                st.success("Hash generated successfully.")
                st.code(generated, language="text")
            except ValueError as exc:
                st.error(str(exc))

with attack_tab:
    st.subheader("📚 Dictionary Attack Demo")
    st.markdown(
        '<div class="card">Try matching a target hash against a local dictionary list.</div>',
        unsafe_allow_html=True,
    )

    target_hash = st.text_input("Paste target hash", key="target_hash")
    use_default = st.checkbox("Use default sample dictionary", value=True)
    uploaded_file = st.file_uploader(
        "Or upload a custom dictionary (.txt)",
        type=["txt"],
        help="One word per line. Keep it small for learning.",
    )

    wordlist: List[str] = []

    try:
        if uploaded_file is not None:
            data = uploaded_file.read()
            text = io.BytesIO(data).read().decode("utf-8", errors="ignore")
            wordlist = [line.strip() for line in text.splitlines() if line.strip()]
            st.info(f"Loaded {len(wordlist)} words from uploaded dictionary.")
        elif use_default:
            wordlist = load_default_dictionary()
            st.info(f"Loaded {len(wordlist)} words from default dictionary.")
    except Exception as exc:  # noqa: BLE001 - display user-friendly upload/load errors
        st.error(f"Could not load dictionary file: {exc}")

    if st.button("Start Dictionary Attack", type="primary"):
        if not target_hash.strip():
            st.error("Target hash is required.")
        elif algorithm.lower() not in SUPPORTED_ALGORITHMS:
            st.error("Invalid hash algorithm selected.")
        elif not wordlist:
            st.error("Dictionary is empty. Upload a file or enable default sample dictionary.")
        else:
            try:
                progress = st.progress(0, text="Starting dictionary attack...")
                for i in range(1, 101):
                    progress.progress(i, text=f"Processing... {i}%")

                result = dictionary_attack(target_hash=target_hash, wordlist=wordlist, algorithm=algorithm)
                attempts_df = pd.DataFrame(result["attempt_log"])

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(
                        f'<div class="card"><b>🎯 Target Hash</b><br>{target_hash}</div>',
                        unsafe_allow_html=True,
                    )
                with c2:
                    st.markdown(
                        f'<div class="card"><b>⚙️ Algorithm</b><br>{algorithm.upper()}</div>',
                        unsafe_allow_html=True,
                    )
                with c3:
                    st.markdown(
                        f'<div class="card"><b>🔢 Words Tested</b><br>{result["attempts"]}</div>',
                        unsafe_allow_html=True,
                    )

                st.markdown("### 📊 Attack Results")
                if result["found"]:
                    st.success(f"Password found: {result['password']}")
                else:
                    st.warning("Password not found in the selected dictionary.")

                st.write(f"**Time taken:** {result['time_taken']:.6f} seconds")

                st.markdown("### 🧾 Attempt Log")
                st.dataframe(attempts_df, use_container_width=True)

                chart_df = pd.DataFrame(
                    {
                        "Status": ["Cracked", "Not Cracked"],
                        "Count": [1 if result["found"] else 0, 0 if result["found"] else 1],
                    }
                )
                fig = px.bar(
                    chart_df,
                    x="Status",
                    y="Count",
                    color="Status",
                    title="Dictionary Attack Outcome",
                    color_discrete_map={"Cracked": "#22c55e", "Not Cracked": "#f59e0b"},
                )
                st.plotly_chart(fig, use_container_width=True)
            except ValueError as exc:
                st.error(str(exc))
            except Exception as exc:  # noqa: BLE001 - catch to keep app beginner-friendly
                st.error(f"Unexpected error during attack: {exc}")

with info_tab:
    st.subheader("🧠 How It Works")
    st.markdown(
        """
        ### 1) What is hashing?
        Hashing transforms text (like a password) into a fixed-length fingerprint.
        Good hash functions are one-way, meaning you can't directly reverse them.

        ### 2) What is a dictionary attack?
        A dictionary attack tries candidate words from a list, hashes each one,
        and compares against a target hash until a match is found.

        ### 3) Why weak passwords are risky
        If passwords are common or predictable, attackers can guess them quickly
        with dictionary lists.

        ### 4) Defensive best practices
        - Use long, unique passwords for every account.
        - Use a password manager.
        - Enable multi-factor authentication (MFA).
        - Use salted password hashing in real applications.
        - Monitor and rate-limit login attempts.

        ✅ This demo is intentionally offline and simplified for education.
        """
    )
