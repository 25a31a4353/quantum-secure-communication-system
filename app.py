from flask import Flask, render_template, request, jsonify
from quantum.qrng import generate_quantum_key
from crypto.encrypt import xor_encrypt
from ai.classifier import get_message_classification
import random

app = Flask(__name__)

# Store current key globally for demo purposes
current_key = "1010101010101010" 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_key', methods=['POST'])
def generate_key():
    global current_key
    try:
        length = int(request.json.get('length', 128))
        if length > 512: length = 512  # Cap length for simulation performance
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
    
    classification = get_message_classification(message)
    
    # Encrypt
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
    trials = 100
    classical_success = 0
    quantum_success = 0
    
    # Generate bitstreams for side-by-side UI visualization
    classical_pattern = []
    quantum_pattern = []
    
    # Classical uses a pseudo-random recognizable mathematical pattern (LFSR style simulate)
    seed = [1, 0, 1, 1, 0, 0, 1, 0]
    for i in range(48):
        classical_pattern.append(seed[i % len(seed)])
        quantum_pattern.append(random.randint(0, 1)) # standard python random used as UI mock proxy
        
    classical_bits_str = "".join(map(str, classical_pattern))
    quantum_bits_str = "".join(map(str, quantum_pattern))

    for _ in range(trials):
        # ML model predicts classical pattern easily
        if random.random() < 0.88:
            classical_success += 1
            
        # ML model cannot predict quantum collapses better than random chance
        if random.random() < 0.50:
            quantum_success += 1
            
    return jsonify({
        'trials': trials,
        'classical_predictability': f"{(classical_success/trials)*100:.1f}%",
        'quantum_predictability': f"{(quantum_success/trials)*100:.1f}%",
        'classical_bits': classical_bits_str,
        'quantum_bits': quantum_bits_str,
        'explanation': "Classical randomness is predictable, quantum randomness is truly random"
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
