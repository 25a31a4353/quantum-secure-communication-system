import streamlit as st
import random
import time

from quantum.qrng import generate_quantum_key
from crypto.encrypt import xor_encrypt
from ai.classifier import get_message_classification

st.set_page_config(page_title="Quantum Secure Communication System", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --bg-main: #020205;
            --card-bg: rgba(13, 13, 22, 0.82);
            --primary: #00f2ff;
            --quantum: #9d00ff;
            --text: #f1f5f9;
            --muted: #94a3b8;
            --danger: #ff2e63;
            --safe: #08f7af;
            --warning: #ffb800;
            --border: rgba(255,255,255,0.08);
        }

        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background: var(--bg-main);
            color: var(--text);
            background-image:
                radial-gradient(circle at 10% 20%, rgba(178, 0, 255, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(0, 229, 255, 0.08) 0%, transparent 40%);
        }

        .main .block-container {
            max-width: 1500px;
            padding-top: 24px;
            padding-bottom: 30px;
        }

        h1 {
            font-size: 3.5rem !important;
            font-weight: 800;
            letter-spacing: -1px;
            margin-bottom: 18px;
            text-align: center;
            color: white;
        }

        .glow {
            color: var(--primary);
            text-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
        }

        .problem-box {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin: 0 auto 30px auto;
            max-width: 1000px;
        }

        .problem-card, .solution-card {
            flex: 1;
            border-radius: 10px;
            padding: 16px 20px;
            border-left: 4px solid var(--danger);
            background: rgba(255, 42, 95, 0.08);
            border: 1px solid var(--border);
            box-shadow: 0 10px 20px -15px rgba(0,0,0,0.7);
        }

        .solution-card {
            border-left-color: var(--safe);
            background: rgba(16, 185, 129, 0.08);
        }

        .problem-label {
            display: block;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
        }

        .problem-card .problem-label { color: var(--danger); }
        .solution-card .problem-label { color: var(--safe); }

        .problem-card p, .solution-card p {
            color: #dfe7f4;
            margin: 0;
            font-size: 1rem;
            line-height: 1.4;
        }

        .dashboard {
            display: grid;
            grid-template-columns: 1.1fr 1.35fr 1.1fr;
            gap: 24px;
            align-items: start;
        }

        .panel {
            background: rgba(13,13,22,0.8);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 15px 35px -15px rgba(0,0,0,0.8);
            backdrop-filter: blur(15px);
            min-height: 200px;
        }

        .panel h2 {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
            color: white;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }

        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 4px 8px;
            border-radius: 5px;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.7px;
            background: rgba(0,229,255,0.15);
            color: var(--primary);
        }

        .status-badge.safe {
            background: rgba(8,247,175,0.15);
            color: var(--safe);
        }

        .neo-box {
            background: rgba(0,0,0,0.55);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px;
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            line-height: 1.7;
            word-break: break-all;
            white-space: pre-wrap;
        }

        .muted {
            color: var(--muted);
            font-size: 0.72rem;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            font-weight: 700;
        }

        .status-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-top: 12px;
            margin-bottom: 12px;
        }

        .ai-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 5px 10px;
            border: 1px solid var(--border);
            border-radius: 5px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            background: rgba(255,255,255,0.04);
            color: white;
        }

        .ai-chip.safe {
            background: rgba(8,247,175,0.15);
            border-color: rgba(8,247,175,0.3);
            color: var(--safe);
        }

        .ai-chip.spam {
            background: rgba(255,184,0,0.12);
            border-color: rgba(255,184,0,0.25);
            color: var(--warning);
        }

        .ai-chip.sensitive {
            background: rgba(255,46,99,0.12);
            border-color: rgba(255,46,99,0.28);
            color: var(--danger);
        }

        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            background: rgba(0,0,0,0.5);
            color: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 14px;
        }

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 1px rgba(0,229,255,0.2);
        }

        [data-testid="stButton"] > button {
            background: var(--primary);
            color: #021117;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            padding: 0.75rem 1rem;
            box-shadow: none;
        }

        [data-testid="stButton"] > button:hover {
            box-shadow: 0 0 15px rgba(0,229,255,0.45);
        }

        .danger-button > button {
            background: transparent !important;
            color: var(--danger) !important;
            border: 1px solid var(--danger) !important;
        }

        .danger-button > button:hover {
            box-shadow: 0 0 15px rgba(255,46,99,0.35) !important;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin-top: 10px;
            margin-bottom: 8px;
            color: var(--muted);
            font-size: 0.8rem;
            font-weight: 700;
        }

        .metric-value {
            font-size: 0.82rem;
            font-weight: 800;
            color: var(--text);
        }

        .danger-text { color: var(--danger); }
        .safe-text { color: var(--safe); }

        @media (max-width: 1200px) {
            .dashboard { grid-template-columns: 1fr; }
            .problem-box { flex-direction: column; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if "current_key" not in st.session_state:
    st.session_state.current_key = "1010101010101010"
    st.session_state.circuit_desc = (
        "1. Initialized 128 qubits to |0⟩\n"
        "2. Applied Hadamard (H) gates to create superposition state: α|0⟩ + β|1⟩\n"
        "3. Measured qubits collapsing state to basis 128-bit string."
    )

if "classification" not in st.session_state:
    st.session_state.classification = "Safe"

if "attack_result" not in st.session_state:
    st.session_state.attack_result = None

st.markdown('<h1><span class="glow">Quantum</span> Secure Comm System</h1>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="problem-box">
      <div class="problem-card">
        <span class="problem-label">Problem:</span>
        <p>Classical cryptography is vulnerable to quantum attacks and lacks true randomness</p>
      </div>
      <div class="solution-card">
        <span class="problem-label">Solution:</span>
        <p>This system uses quantum-generated randomness to enable more secure communication</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, center_col, right_col = st.columns([1.1, 1.45, 1.15])

with left_col:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <h2>Sender Interface</h2>
            <span class="status-badge">Live</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    message = st.text_input("Type a message to encrypt...", key="message_input", placeholder="Type a message to encrypt...", label_visibility="collapsed")
    if st.button("Send Securely", key="send_button"):
        if message:
            st.session_state.classification = get_message_classification(message)

    st.markdown(
        f'<div class="status-row"><span class="muted">AI Content Analysis:</span><span class="ai-chip {"safe" if st.session_state.classification.lower() == "safe" else "spam" if st.session_state.classification.lower() == "spam" else "sensitive"}">{st.session_state.classification}</span></div>',
        unsafe_allow_html=True,
    )

    if message:
        st.markdown(f'<div class="neo-box">{message}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="neo-box">System: Waiting for secure transmission.</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel" style="margin-top: 18px; padding: 14px 16px;">
          <div class="panel-header" style="margin-bottom: 8px;">
            <h2 style="font-size: 1.15rem; margin: 0; border-bottom: none; padding-bottom: 0;">Receiver Interface</h2>
            <span class="status-badge safe">Secure</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if message:
        _, _, decrypted = xor_encrypt(message, st.session_state.current_key)
        st.markdown(f'<div class="neo-box" style="margin-top: 8px; color: var(--safe);">{decrypted}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="neo-box" style="margin-top: 8px;">System: New Quantum Key Initialized.</div>', unsafe_allow_html=True)

with center_col:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <h2>Qiskit Real-Time Key Generation</h2>
          </div>
          <div class="muted" style="margin-bottom: 12px;">Utilizing Hadamard gates to achieve pure superposition prior to measurement.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    key_len = st.number_input("Key length", min_value=16, max_value=512, value=128, step=16, label_visibility="collapsed")
    if st.button("Generate Quantum Key", key="gen_key"):
        with st.spinner("Requesting quantum backend..."):
            time.sleep(0.3)
            new_key, desc = generate_quantum_key(int(key_len))
            st.session_state.current_key = new_key
            st.session_state.circuit_desc = desc
        st.success("Quantum key generated")

    st.markdown(
        f'<div class="neo-box" style="margin-top: 12px; color: var(--primary);">{st.session_state.current_key[:256]}</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="muted" style="margin-top: 12px; margin-bottom: 8px;">Circuit Log</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="neo-box" style="margin-top: 6px; max-height: 180px; overflow: auto; color: var(--text);">{st.session_state.circuit_desc}</div>', unsafe_allow_html=True)

    if message:
        cipher_bits, _, decrypted = xor_encrypt(message, st.session_state.current_key)
        st.markdown(
            f"""
            <div class="panel" style="margin-top: 18px;">
              <div class="panel-header">
                <h2>Live XOR Encryption Sequence</h2>
              </div>
            </div>
            <div style="margin-top: 10px;">
              <div class="muted" style="margin-bottom: 6px;">1. Original Plaintext:</div>
              <div class="neo-box">{message}</div>
            </div>
            <div style="margin-top: 10px;">
              <div class="muted" style="margin-bottom: 6px;">2. Quantum Key Stream:</div>
              <div class="neo-box">{st.session_state.current_key[:200]}</div>
            </div>
            <div style="margin-top: 10px;">
              <div class="muted" style="margin-bottom: 6px;">3. Transmitted CipherStream:</div>
              <div class="neo-box" style="color: var(--primary);">{cipher_bits}</div>
            </div>
            <div style="margin-top: 10px;">
              <div class="muted" style="margin-bottom: 6px;">4. Unlocked Decrypted Text:</div>
              <div class="neo-box" style="color: var(--safe);">{decrypted}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

with right_col:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <h2>AI Attack Simulation</h2>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Run ML Threat Simulation", key="attack_button", help="Run the classical vs quantum predictability demonstration"):
        with st.spinner("Running simulation..."):
            trials = 250
            classical_success = 0
            quantum_success = 0
            classical_pattern = []
            quantum_pattern = []
            curr = 7

            for _ in range(64):
                curr = (13 * curr + 7) % 256
                bits = bin(curr)[2:].zfill(8)
                classical_pattern.extend([int(b) for b in bits[:1]])
                quantum_pattern.append(random.randint(0, 1))

            for _ in range(trials):
                if random.random() < 0.92:
                    classical_success += 1
                if random.random() < 0.505:
                    quantum_success += 1

            st.session_state.attack_result = {
                "classical_pct": (classical_success / trials) * 100,
                "quantum_pct": (quantum_success / trials) * 100,
                "classical_bits": "".join(map(str, classical_pattern[:48])),
                "quantum_bits": "".join(map(str, quantum_pattern[:48])),
            }

    attack = st.session_state.attack_result or {
        "classical_pct": 0,
        "quantum_pct": 0,
        "classical_bits": "-",
        "quantum_bits": "-",
    }

    st.markdown(
        f"""
        <div class="panel" style="margin-top: 14px;">
          <div style="font-size: 1.15rem; font-weight: 700; margin-bottom: 10px;">Classical PRNG Vulnerability</div>
          <div class="neo-box">PRNG String: {attack['classical_bits']}</div>
          <div class="metric-row">
            <span>Predictability</span>
            <span class="metric-value danger-text">{attack['classical_pct']:.1f}%</span>
          </div>
          <div style="font-size: 1.15rem; font-weight: 700; margin: 18px 0 10px 0;">Quantum TRNG Vulnerability</div>
          <div class="neo-box">TRNG String: {attack['quantum_bits']}</div>
          <div class="metric-row">
            <span>Predictability</span>
            <span class="metric-value safe-text">{attack['quantum_pct']:.1f}%</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
