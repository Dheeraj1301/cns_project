# Password Cracking using Dictionary Attack

## Overview
This project is a **safe educational prototype** that demonstrates how dictionary attacks work against hashed passwords in a local, controlled environment.

It is designed for beginners learning defensive cybersecurity concepts with Python + Streamlit.

## Ethical Disclaimer
> ⚠️ This project is strictly for educational and defensive cybersecurity learning only.
> Do **not** use it against real systems, websites, online accounts, Wi-Fi, APIs, databases, SSH services, or any external targets.

The app only accepts:
- User-provided hashes
- Local dictionary files
- Offline demo inputs

## Features
- Streamlit web UI with colorful cards and sections
- Hash generation tab (MD5, SHA1, SHA256)
- Dictionary attack tab using local dictionary words
- Supports uploaded `.txt` dictionary file (one word per line)
- Option to use built-in sample dictionary
- Progress bar and detailed attempt log
- Result summary (found/not found, attempts, time taken)
- Plotly chart for cracked vs not cracked outcome
- Beginner-friendly explanations in “How It Works” tab

## Folder Structure
```text
password-dictionary-attack/
│
├── app.py
├── requirements.txt
├── README.md
├── backend/
│   ├── __init__.py
│   ├── cracker.py
│   ├── hash_utils.py
│   └── sample_data.py
│
├── dictionaries/
│   └── sample_dictionary.txt
│
└── assets/
    └── .gitkeep
```

## Installation
1. Clone or download this project.
2. Go into the project directory:
   ```bash
   cd password-dictionary-attack
   ```
3. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux/macOS
   .venv\Scripts\activate      # Windows PowerShell
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the App
```bash
streamlit run app.py
```

Then open the local URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## How the Code Works

### 1) Hash generation (`backend/hash_utils.py`)
- `hash_password(password, algorithm)`
- Uses Python `hashlib`
- Supports `md5`, `sha1`, `sha256`
- Raises `ValueError` for unsupported algorithms

### 2) Dictionary attack logic (`backend/cracker.py`)
- `dictionary_attack(target_hash, wordlist, algorithm)`
- Iterates through each dictionary word
- Hashes the word and compares to target hash
- Returns:
  - `found` (bool)
  - `password` (matched plain text, or `None`)
  - `attempts` (number tested)
  - `time_taken` (seconds)
  - `attempt_log` (per-word test details)

### 3) Sample dictionary loader (`backend/sample_data.py`)
- `load_default_dictionary()`
- Reads local file: `dictionaries/sample_dictionary.txt`
- Returns cleaned list of words

### 4) Streamlit UI (`app.py`)
- Uses tabs:
  - **Generate Hash**
  - **Dictionary Attack**
  - **How It Works**
- Uses sidebar for algorithm selection and navigation hints
- Includes error handling for:
  - Empty hash input
  - Empty dictionary
  - Invalid algorithm
  - File upload/read issues

## Explanation of Each File
- `app.py`: Main UI and user interaction flow
- `backend/hash_utils.py`: Hashing utility function
- `backend/cracker.py`: Dictionary attack engine and result logging
- `backend/sample_data.py`: Default dictionary loader
- `dictionaries/sample_dictionary.txt`: Small demo wordlist
- `requirements.txt`: Python package dependencies
- `assets/.gitkeep`: Placeholder for static assets

## Example Workflow
1. Open **Generate Hash** tab.
2. Enter a password (for example: `streamlit`) and generate hash.
3. Copy the hash output.
4. Go to **Dictionary Attack** tab.
5. Paste the hash into the target hash input.
6. Keep default dictionary enabled (or upload your own local `.txt` file).
7. Click **Start Dictionary Attack**.
8. Review result cards, attempts table, and chart.

## Limitations
- Intentionally simple and sequential (no multiprocessing)
- Uses small local dictionaries only
- Not suitable for real password auditing or penetration testing
- No salted-hash verification flow (for simplicity)

## Future Improvements (Safe & Educational)
- Add optional salting demonstration mode
- Add hash format auto-detection hints
- Add export of attack logs to CSV
- Add classroom quiz section on password security

## Defensive Cybersecurity Lessons
- Weak/reused passwords are vulnerable to guessing attacks
- Hashing alone is not enough without salting and secure storage practices
- Strong passphrases and unique credentials reduce risk
- MFA significantly improves account security
- Password managers help maintain long unique passwords safely

---
**Reminder:** Keep all experiments local, ethical, and authorized.
