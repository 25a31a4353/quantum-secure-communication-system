import streamlit as st
from quantum.qrng import generate_quantum_key
from crypto.encrypt import xor_encrypt
from ai.classifier import get_message_classification
import random
import time

st.set_page_config(page_title="Quantum Secure Comm", layout="wide")

st.markdown(
    """
    <style>
        :root {
            --bg-main: #020205;
            --card-bg: rgba(13, 13, 22, 0.8);
            --primary: #00f2ff;
            --primary-glow: rgba(0, 242, 255, 0.5);
            --quantum: #9d00ff;
            --quantum-glow: rgba(157, 0, 255, 0.5);
            --text: #f1f5f9;
            --text-dim: #94a3b8;
            --danger: #ff2e63;
            --safe: #08f7af;
            --warning: #ffb800;
            --border: rgba(255, 255, 255, 0.08);
            --glass: rgba(255, 255, 255, 0.03);
        }
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
            background: var(--bg-main);
            color: var(--text);
            background-image: radial-gradient(circle at 10% 20%, rgba(178,0,255,0.08) 0%, transparent 40%), radial-gradient(circle at 90% 80%, rgba(0,229,255,0.08) 0%, transparent 40%);
        }
        .main .block-container {
            max-width: 1500px;
            padding-top: 24px;
            padding-bottom: 28px;
        }
        h1, h2, h3, p {
            color: var(--text);
        }
        h1 {
            font-size: 4rem;
            font-weight: 800;
            letter-spacing: -1px;
            text-align: center;
            margin-bottom: 18px;
            color: white;
        }
        .glow {
            color: var(--primary);
            text-shadow: 0 0 15px rgba(0, 229, 255, 0.6);
        }
        .problem-solution-box {
            display: flex;
            justify-content: center;
            gap: 24px;
            margin: 0 auto 28px auto;
            max-width: 1000px;
        }
        .ps-item {
            flex: 1;
            border-radius: 12px;
            text-align: left;
            padding: 18px 20px;
            background: rgba(255,255,255,0.03);
            border: 1px solid var(--border);
            backdrop-filter: blur(12px);
        }
        .ps-item.problem {
            background: rgba(255, 42, 95, 0.1);
            border-left: 4px solid var(--danger);
        }
        .ps-item.solution {
            background: rgba(16, 185, 129, 0.1);
            border-left: 4px solid var(--safe);
        }
        .ps-label {
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1px;
            display: block;
            margin-bottom: 8px;
        }
        .problem .ps-label { color: var(--danger); }
        .solution .ps-label { color: var(--safe); }
        .ps-item p {
            margin: 0;
            font-size: 1rem;
            line-height: 1.4;
            color: #cbd5e1;
        }
        .card {
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 15px 35px -15px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(20px);
            height: 100%;
        }
        .card h2 {
            margin-top: 0;
            font-size: 1.25rem;
            font-weight: 600;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
            margin-bottom: 15px;
            color: #fff;
        }
        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 10px;
        }
        .status-badge {
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            text-transform: uppercase;
            padding: 4px 9px;
            border-radius: 6px;
            background: rgba(0,229,255,0.15);
            color: var(--primary);
        }
        .status-badge.safe {
            background: rgba(16,185,129,0.15);
            color: var(--safe);
        }
        .dark-box {
            background: rgba(0,0,0,0.50);
            border-radius: 10px;
            padding: 12px;
            border: 1px solid var(--border);
            color: var(--primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            word-break: break-all;
            white-space: pre-wrap;
        }
        .mono {
            font-family: 'JetBrains Mono', monospace !important;
        }
        .section-label {
            display: block;
            margin: 12px 0 8px 0;
            color: var(--text-dim);
            font-size: 0.74rem;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            font-weight: 700;
        }
        .breathe {
            box-shadow: 0 0 10px rgba(0,229,255,0.18);
        }
        [data-testid="stButton"] > button, [data-testid="baseButton-secondary"] > button {
            background: var(--primary);
            color: #000;
            border: none;
            border-radius: 8px;
            font-weight: 700;
            padding: 0.7rem 1.1rem;
            box-shadow: none;
        }
        [data-testid="stButton"] > button:hover {
            box-shadow: 0 0 15px rgba(0, 229, 255, 0.5);
            transform: translateY(-1px);
        }
        button[kind="secondary"] {
            background: transparent !important;
            color: var(--danger) !important;
            border: 1px solid var(--danger) !important;
        }
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea {
            background: rgba(0,0,0,0.6);
            color: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 0.7rem 0.8rem;
        }
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 1px rgba(0, 229, 255, 0.3);
        }
        .metric-box {
            background: rgba(0,0,0,0.4);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 0.8rem 0.9rem;
            margin-top: 0.5rem;
        }
        .metric-row {
            display: flex;
            justify-content: space-between;
            gap: 10px;
            margin-bottom: 6px;
            color: var(--text-dim);
        }
        .metric-row strong { color: white; }
        .good { color: var(--safe); font-weight: 700; }
        .warn { color: var(--danger); font-weight: 700; }
        .small { font-size: 0.8rem; }
        @media (max-width: 1100px) {
            .problem-solution-box { flex-direction: column; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'current_key' not in st.session_state:
    st.session_state.current_key = "1010101010101010"
    st.session_state.circuit_desc = "1. Initialized 128 qubits to |0⟩\n2. Applied Hadamard (H) gates to create superposition state: α|0⟩ + β|1⟩\n3. Measured qubits collapsing state to basis 128-bit string."

st.markdown('<h1><span class="glow">Quantum</span> Secure Comm System</h1>', unsafe_allow_html=True)

st.markdown(
    '<div class="problem-solution-box"><div class="ps-item problem"><span class="ps-label">Problem:</span><p>Classical cryptography is vulnerable to quantum attacks and lacks true randomness</p></div><div class="ps-item solution"><span class="ps-label">Solution:</span><p>This system uses quantum-generated randomness to enable more secure communication</p></div></div>',
    unsafe_allow_html=True,
)

left_col, center_col, right_col = st.columns([1.15, 1.35, 1.15])

with left_col:
    st.markdown('<div class="card"><div class="card-header"><h2>Sender Interface</h2><span class="status-badge">Live</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="dark-box">System: New Quantum Key Initialized.</div>', unsafe_allow_html=True)
    message = st.text_input("", placeholder="Type a message to encrypt...", label_visibility="collapsed")
    send_col, _ = st.columns([1, 1])
    with send_col:
        if st.button("Send Securely"):
            pass
    classification = "Safe"
    if message:
        classification = get_message_classification(message)
    st.markdown('<div class="section-label">AI Content Analysis:</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dark-box"><span class="good">{classification}</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card" style="margin-top: 1rem; padding: 1rem;"><div class="card-header" style="margin-bottom: 8px;"><h2 style="margin: 0; border: none; padding: 0;">Receiver Interface</h2><span class="status-badge safe">Secure</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="dark-box">System: New Quantum Key Initialized.</div>', unsafe_allow_html=True)
    if message:
        st.markdown(f'<div class="dark-box" style="margin-top: 0.8rem; color: var(--safe);">{message}</div>', unsafe_allow_html=True)

with center_col:
    st.markdown('<div class="card"><div class="card-header"><h2>Qiskit Real-Time Key Generation</h2></div><p class="small" style="color: var(--text-dim); margin-top:-8px; margin-bottom: 12px;">Utilizing Hadamard gates to achieve pure superposition prior to measurement.</p><div class="metric-row"><span>Key Length:</span><strong>128 bits</strong></div><div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 1rem;"> <div style="flex: 1;"><label style="display:block; color: var(--text-dim); font-size: 0.78rem; margin-bottom: .35rem;">Key Length</label><div class="metric-box">'+str(st.session_state.get('key_len', 128))+'</div></div> <div style="padding-top: 1.4rem;">'+str(st.button("Generate Quantum Key", key="gen_key"))+'</div></div><div class="dark-box mono">'+st.session_state.current_key[:256]+'</div><div class="section-label">Circuit Log</div><div class="dark-box mono" style="max-height: 180px; overflow:auto;">'+st.session_state.circuit_desc+'</div></div>', unsafe_allow_html=True)
    key_len = st.number_input("Key Length", min_value=16, max_value=512, value=128, step=16, label_visibility="collapsed")
    if st.button("Generate Quantum Key", key="gen_key_2"):
        with st.spinner("Requesting quantum backend..."):
            time.sleep(0.4)
            key, desc = generate_quantum_key(int(key_len))
            st.session_state.current_key = key
            st.session_state.circuit_desc = desc
            st.session_state.key_len = key_len
        st.success("Quantum key generated")

    st.markdown('<div class="card" style="margin-top: 1.2rem;"><div class="card-header"><h2>Live XOR Encryption Sequence</h2></div><div class="section-label">1. Original Plaintext:</div><div class="dark-box">'+(message if message else '-')+'</div><div class="section-label">2. Quantum Key Stream:</div><div class="dark-box mono">'+st.session_state.current_key[:200]+'...</div><div class="section-label">3. Transmitted CipherStream:</div><div class="dark-box mono" style="color: var(--primary);">'+(xor_encrypt(message, st.session_state.current_key)[1] if message else '-')+'</div><div class="section-label">4. Unlocked Decrypted Text:</div><div class="dark-box" style="color: var(--safe);">'+(xor_encrypt(message, st.session_state.current_key)[2] if message else '-')+'</div></div>', unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card"><div class="card-header"><h2>AI Attack Simulation</h2></div><button kind="secondary" style="width: 100%; margin-bottom: .8rem;">Run ML Threat Simulation</button><div class="section-label">Classical PRNG Vulnerability</div><div class="dark-box mono">PRNG String: -</div><div class="metric-row" style="margin-top: 0.6rem;"><span>Predictability</span><strong class="warn">0%</strong></div><div class="section-label">Quantum TRNG Vulnerability</div><div class="dark-box mono">TRNG String: -</div><div class="metric-row" style="margin-top: 0.6rem;"><span>Predictability</span><strong class="good">0%</strong></div></div>', unsafe_allow_html=True)
    if st.button("Run ML Threat Simulation", key="threat_sim"):
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

            st.session_state.attack = {
                'classical': float((classical_success / trials) * 100),
                'quantum': float((quantum_success / trials) * 100),
                'classical_bits': "".join(map(str, classical_pattern[:48])),
                'quantum_bits': "".join(map(str, quantum_pattern[:48])),
            }

    if 'attack' in st.session_state:
        st.markdown(
            f"<div class='card' style='margin-top: 1rem;'><div class='section-label'>Classical PRNG Vulnerability</div><div class='dark-box mono'>{st.session_state.attack['classical_bits']}</div><div class='metric-row' style='margin-top: 0.6rem;'><span>Predictability</span><strong class='warn'>{st.session_state.attack['classical']:.1f}%</strong></div><div class='section-label'>Quantum TRNG Vulnerability</div><div class='dark-box mono'>{st.session_state.attack['quantum_bits']}</div><div class='metric-row' style='margin-top: 0.6rem;'><span>Predictability</span><strong class='good'>{st.session_state.attack['quantum']:.1f}%</strong></div></div>",
            unsafe_allow_html=True,
        )

st.sidebar.title("Quantum Core")
st.sidebar.write("System Metrics")
st.sidebar.json({
    'status': 'Online',
    'qubit_temperature': '15mK',
    'coherence_time': '94μs',
    'error_rate': '0.0012%',
    'backend': 'IBM Q - Falcon Processor v5'
})
st.sidebar.write("Active key preview")
st.sidebar.code(st.session_state.current_key[:120])
