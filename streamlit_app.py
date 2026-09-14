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
            --card-bg: rgba(13, 13, 22, 0.84);
            --panel-bg: rgba(12, 14, 20, 0.82);
            --primary: #00f2ff;
            --primary-strong: #33d7ff;
            --quantum: #9d00ff;
            --safe: #08f7af;
            --danger: #ff2e63;
            --warning: #ffb800;
            --text: #f1f5f9;
            --muted: #94a3b8;
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
            padding-top: 20px;
            padding-bottom: 30px;
        }

        h1 {
            font-size: 4rem !important;
            letter-spacing: -1px;
            font-weight: 800;
            text-align: center;
            margin: 0 0 18px 0;
            color: #fff;
        }

        .glow {
            color: var(--primary);
            text-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
        }

        .problem-box {
            display: flex;
            gap: 24px;
            max-width: 1000px;
            margin: 0 auto 24px auto;
        }

        .problem-card {
            flex: 1;
            border-radius: 12px;
            padding: 18px 20px;
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-left: 4px solid var(--danger);
            background: rgba(255, 42, 95, 0.08);
            color: white;
        }

        .solution-card {
            flex: 1;
            border-radius: 12px;
            padding: 18px 20px;
            background: rgba(255,255,255,0.02);
            border: 1px solid var(--border);
            border-left: 4px solid var(--safe);
            background: rgba(16, 185, 129, 0.08);
            color: white;
        }

        .problem-label {
            display: block;
            font-size: 0.78rem;
            letter-spacing: 1px;
            text-transform: uppercase;
            font-weight: 800;
            margin-bottom: 8px;
        }

        .problem-card .problem-label { color: var(--danger); }
        .solution-card .problem-label { color: var(--safe); }

        .problem-card p, .solution-card p {
            margin: 0;
            font-size: 1rem;
            color: #dfe7f4;
            line-height: 1.4;
        }

        .panel {
            background: var(--panel-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 18px 20px 16px 20px;
            box-shadow: 0 15px 35px -15px rgba(0,0,0,0.7);
            height: 100%;
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
            margin-bottom: 14px;
        }

        .panel-header h2 {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
            color: white;
        }

        .badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 4px 8px;
            border-radius: 6px;
            font-size: 0.68rem;
            letter-spacing: 0.8px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge.live {
            background: rgba(0,229,255,0.15);
            color: var(--primary);
        }

        .badge.safe {
            background: rgba(8,247,175,0.15);
            color: var(--safe);
        }

        .neo-box {
            background: rgba(0,0,0,0.5);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 12px;
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.82rem;
            word-break: break-all;
            white-space: pre-wrap;
            line-height: 1.6;
        }

        .muted {
            color: var(--muted);
            font-size: 0.82rem;
        }

        .status-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            margin: 12px 0 8px 0;
        }

        .ai-chip {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 0.76rem;
            font-weight: 700;
            text-transform: uppercase;
            border: 1px solid var(--border);
            background: rgba(255,255,255,0.04);
            color: white;
        }

        .ai-chip.safe {
            background: rgba(8,247,175,0.15);
            color: var(--safe);
            border-color: rgba(8,247,175,0.3);
        }

        .ai-chip.spam {
            background: rgba(255,184,0,0.12);
            color: var(--warning);
            border-color: rgba(255,184,0,0.3);
        }

        .ai-chip.sensitive {
            background: rgba(255,46,99,0.12);
            color: var(--danger);
            border-color: rgba(255,46,99,0.3);
        }

        .stTextInput > div > div > input {
            background: rgba(0,0,0,0.55);
            color: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.7rem 0.8rem;
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
            padding: 0.75rem 1.1rem;
            width: 100%;
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
            box-shadow: 0 0 15px rgba(255,46,99,0.3) !important;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: 1fr auto;
            gap: 12px;
            align-items: end;
            margin: 10px 0 16px 0;
        }

        .metric-grid .small-label {
            font-size: 0.78rem;
            color: var(--muted);
            margin-bottom: 6px;
        }

        .metric-box {
            background: rgba(0,0,0,0.4);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.7rem 0.8rem;
            min-width: 90px;
            text-align: center;
            color: white;
        }

        .mini-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 14px;
        }

        .quantum-key {
            color: var(--primary);
            text-shadow: 0 0 10px rgba(0,229,255,0.18);
        }

        .safe-text { color: var(--safe); }
        .danger-text { color: var(--danger); }

        .metric-value {
            font-size: 0.85rem;
            font-weight: 700;
        }

        @media (max-width: 1200px) {
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
            <span class="badge live">Live</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    message = st.text_input("", key="message_input", placeholder="Type a message to encrypt...", label_visibility="collapsed")

    if st.button("Send Securely", key="send_button"):
        st.session_state.last_message = message
        if message:
            st.session_state.classification = get_message_classification(message)

    if "classification" not in st.session_state:
        st.session_state.classification = "Safe"

    st.markdown('<div class="status-row"> <span class="muted">AI Content Analysis:</span> <span class="ai-chip safe">'+st.session_state.classification+'</span></div>', unsafe_allow_html=True)

    if message:
        st.markdown(f'<div class="neo-box quantum-key">{message}</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel" style="margin-top: 18px; padding: 14px 16px;">
          <div class="panel-header" style="margin-bottom: 8px;">
            <h2 style="font-size: 1.15rem; margin: 0;">Receiver Interface</h2>
            <span class="badge safe">Secure</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if message:
        encrypted_bits, used_key, decrypted = xor_encrypt(message, st.session_state.current_key)
        st.markdown(f'<div class="neo-box">{decrypted}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="neo-box">System: Waiting for secure transmission.</div>', unsafe_allow_html=True)

with center_col:
    st.markdown(
        """
        <div class="panel">
          <div class="panel-header">
            <h2>Qiskit Real-Time Key Generation</h2>
          </div>
          <div class="muted" style="margin-bottom: 10px;">Utilizing Hadamard gates to achieve pure superposition prior to measurement.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    key_len = st.number_input("Key length", min_value=16, max_value=512, value=128, step=16, label_visibility="collapsed")
    
    if st.button("Generate Quantum Key", key="gen_button"):
        with st.spinner("Requesting quantum backend..."):
            time.sleep(0.4)
            new_key, desc = generate_quantum_key(int(key_len))
            st.session_state.current_key = new_key
            st.session_state.circuit_desc = desc
        st.success("Quantum key generated")

    st.markdown(
        f"""
        <div class="neo-box quantum-key" style="margin-top: 10px;">{st.session_state.current_key[:256]}</div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="muted" style="margin-top: 12px;">Circuit Log</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="neo-box" style="max-height: 180px; overflow: auto;">{st.session_state.circuit_desc}</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="panel" style="margin-top: 18px;">
          <div class="panel-header">
            <h2>Live XOR Encryption Sequence</h2>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if message:
        cipher_bits, used_key, decrypted = xor_encrypt(message, st.session_state.current_key)
        st.markdown(f'<div class="neo-box" style="margin-top: 10px;"><div class="muted">1. Original Plaintext:</div>{message}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="neo-box" style="margin-top: 10px;"><div class="muted">2. Quantum Key Stream:</div>{st.session_state.current_key[:200]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="neo-box" style="margin-top: 10px; color: var(--primary);"><div class="muted">3. Transmitted CipherStream:</div>{cipher_bits}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="neo-box" style="margin-top: 10px; color: var(--safe);"><div class="muted">4. Unlocked Decrypted Text:</div>{decrypted}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="neo-box" style="margin-top: 10px;">System: No active message to encrypt.</div>', unsafe_allow_html=True)

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

    attack = st.session_state.attack_result
    if attack is None:
        attack = {
            "classical_pct": 0,
            "quantum_pct": 0,
            "classical_bits": "-",
            "quantum_bits": "-",
        }

    st.markdown(
        f"""
        <div class="panel" style="margin-top: 12px;">
          <div style="margin-bottom: 10px;"><strong>Classical PRNG Vulnerability</strong></div>
          <div class="neo-box">PRNG String: {attack['classical_bits']}</div>
          <div class="mini-row" style="margin-top: 8px;">
            <span class="muted">Predictability</span>
            <span class="metric-value danger-text">{attack['classical_pct']:.1f}%</span>
          </div>
          <div style="margin-top: 18px;"><strong>Quantum TRNG Vulnerability</strong></div>
          <div class="neo-box" style="margin-top: 10px;">TRNG String: {attack['quantum_bits']}</div>
          <div class="mini-row" style="margin-top: 8px;">
            <span class="muted">Predictability</span>
            <span class="metric-value safe-text">{attack['quantum_pct']:.1f}%</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
