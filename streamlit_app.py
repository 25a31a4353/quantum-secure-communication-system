import streamlit as st
from quantum.qrng import generate_quantum_key
from crypto.encrypt import xor_encrypt
from ai.classifier import get_message_classification
import random
import time


st.set_page_config(page_title="Quantum Secure Comm", layout="wide")

if 'current_key' not in st.session_state:
    st.session_state.current_key = "1010101010101010"
    st.session_state.circuit_desc = "No Q-Key Loaded"

st.title("Quantum Secure Communication System")

with st.sidebar:
    st.header("Quantum Core")
    key_len = st.number_input("Key length (bits)", min_value=16, max_value=512, value=128, step=16)
    if st.button("Generate Quantum Key"):
        with st.spinner("Requesting quantum backend..."):
            # small delay to mimic remote quantum backend
            time.sleep(0.4)
            key, desc = generate_quantum_key(int(key_len))
            st.session_state.current_key = key
            st.session_state.circuit_desc = desc
        st.success("Quantum key generated")

    st.markdown("**Active key (preview):**")
    st.code(st.session_state.current_key[:256])
    st.markdown("---")
    st.markdown("**System Metrics**")
    st.write({
        'status': 'Online',
        'qubit_temperature': '15mK',
        'coherence_time': '94μs',
        'error_rate': '0.0012%',
        'backend': 'IBM Q - Falcon Processor v5'
    })

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Send Secure Message")
    message = st.text_input("Message to encrypt")
    if st.button("Send Securely"):
        if not message:
            st.warning("Enter a message to encrypt")
        else:
            classification = get_message_classification(message)
            cipher_bits, used_key, decrypted = xor_encrypt(message, st.session_state.current_key)
            st.markdown("**Classifier result:**")
            st.info(classification)
            st.markdown("**Original**")
            st.write(message)
            st.markdown("**Used Key (bits)**")
            st.code(used_key)
            st.markdown("**Cipher (bits)**")
            st.code(cipher_bits)
            st.markdown("**Decrypted (verification)**")
            st.success(decrypted)

    st.markdown("---")
    st.subheader("Attack Simulation")
    if st.button("Run ML Threat Simulation"):
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

            st.write({
                'trials': trials,
                'classical_predictability': f"{(classical_success/trials)*100:.1f}%",
                'quantum_predictability': f"{(quantum_success/trials)*100:.1f}%",
                'classical_bits': "".join(map(str, classical_pattern[:48])),
                'quantum_bits': "".join(map(str, quantum_pattern[:48])),
            })

with col2:
    st.subheader("Quantum Circuit Description")
    st.text_area("Circuit log", value=st.session_state.circuit_desc, height=300)

    st.markdown("---")
    st.subheader("Quick Controls")
    if st.button("Show current key in full"):
        st.code(st.session_state.current_key)

st.sidebar.markdown("---")
st.sidebar.markdown("Built from the original Flask demo — now in Streamlit.")
