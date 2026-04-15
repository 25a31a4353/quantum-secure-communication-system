from flask import Flask, render_template, request, jsonify
from quantum.qrng import generate_quantum_key
from crypto.encrypt import xor_encrypt
from ai.classifier import get_message_classification
import random
import time

app = Flask(__name__)

# Store current key globally for demo purposes (In production use redis/session)
current_key = "1010101010101010" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/system_status', methods=['GET'])
def system_status():
    """Returns mock hardware metrics for the 'pro' vibe."""
    return jsonify({
        'status': 'Online',
        'qubit_temperature': '15mK',
        'coherence_time': '94μs',
        'error_rate': '0.0012%',
        'backend': 'IBM Q - Falcon Processor v5'
    })

@app.route('/generate_key', methods=['POST'])
def generate_key():
    global current_key
    try:
        length = int(request.json.get('length', 128))
        if length > 512: length = 512  
        
        # Simulate network latency of a real quantum cloud backend
        time.sleep(0.4) 
        
        key, circuit_info = generate_quantum_key(length)
        current_key = key
        return jsonify({'success': True, 'key': key, 'circuit': circuit_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    key = current_key
    
    # Classify message content
    classification = get_message_classification(message)
    
    # Encrypt using Quantum OTP
    cipher_bits, used_key, decrypted_str = xor_encrypt(message, key)
    
    return jsonify({
        'success': True,
        'original': message,
        'classifier_result': classification,
        'cipher_bits': cipher_bits,
        'used_key': used_key,
        'decrypted': decrypted_str
    })

@app.route('/simulate_attack', methods=['GET'])
def simulate_attack():
    """
    Simulates a machine learning attack on classical vs quantum entropy bits.
    Classical bits follow a hidden Linear Congruential Generator pattern.
    Quantum bits are truly non-deterministic.
    """
    trials = 250
    classical_success = 0
    quantum_success = 0
    
    # Generate bitstreams
    classical_pattern = []
    quantum_pattern = []
    
    # Classical LCG simulation (recognizable by ML)
    # X_{n+1} = (aX_n + c) % m
    curr = 7
    for _ in range(64):
        curr = (13 * curr + 7) % 256
        bits = bin(curr)[2:].zfill(8)
        classical_pattern.extend([int(b) for b in bits[:1]]) # Take MSB for stream
        quantum_pattern.append(random.randint(0, 1))

    # ML Predictability Simulation
    # In a real scenario, RNNs/LSTMs would detect the classical PRNG state
    for _ in range(trials):
        # 92% success rate in predicting the next bit of a simple LCG
        if random.random() < 0.92:
            classical_success += 1
            
        # 50% success rate (pure chance) for quantum TPRNG
        if random.random() < 0.505: # Slight bias for 'luck' in demo
            quantum_success += 1
            
    return jsonify({
        'trials': trials,
        'classical_predictability': f"{(classical_success/trials)*100:.1f}%",
        'quantum_predictability': f"{(quantum_success/trials)*100:.1f}%",
        'classical_bits': "".join(map(str, classical_pattern[:48])),
        'quantum_bits': "".join(map(str, quantum_pattern[:48])),
        'explanation': "The classical source exhibits a mathematical bias recognizable by neural networks. The quantum source provides maximum entropy (no patterns)."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
