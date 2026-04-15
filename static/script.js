document.addEventListener('DOMContentLoaded', () => {
    
    // UI Elements
    const msgInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const senderLogs = document.getElementById('sender-logs');
    const receiverLogs = document.getElementById('receiver-logs');
    
    const genKeyBtn = document.getElementById('gen-key-btn');
    const keyLengthInput = document.getElementById('key-length');
    const activeKeyDisp = document.getElementById('active-key');
    const circuitDescDisp = document.getElementById('circuit-desc');
    
    const dispPlain = document.getElementById('disp-plain');
    const dispKey = document.getElementById('disp-key');
    const dispCipher = document.getElementById('disp-cipher');
    const dispDecrypted = document.getElementById('disp-decrypted');
    
    const aiResult = document.getElementById('ai-result');
    const simAttackBtn = document.getElementById('sim-attack-btn');
    const barClassical = document.getElementById('bar-classical');
    const barQuantum = document.getElementById('bar-quantum');
    const pctClassical = document.getElementById('pct-classical');
    const pctQuantum = document.getElementById('pct-quantum');
    const classicalBitsDisp = document.getElementById('classical-bits-disp');
    const quantumBitsDisp = document.getElementById('quantum-bits-disp');
    const attackExplanation = document.getElementById('attack-explanation');

    // Auto-generate key on load
    generateKey();

    // Event Listeners
    genKeyBtn.addEventListener('click', generateKey);
    
    sendBtn.addEventListener('click', sendMessage);
    msgInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') sendMessage();
    });

    simAttackBtn.addEventListener('click', runAttackSim);

    function addMessageToLog(logElement, text, classes) {
        const div = document.createElement('div');
        div.className = `msg ${classes}`;
        div.textContent = text;
        logElement.appendChild(div);
        logElement.scrollTop = logElement.scrollHeight;
    }

    async function generateKey() {
        genKeyBtn.disabled = true;
        genKeyBtn.textContent = "Processing...";
        activeKeyDisp.textContent = "Querying IBM Qiskit Backend...";
        circuitDescDisp.textContent = "Initializing Hadamard gates...";
        
        try {
            const res = await fetch('/generate_key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({length: keyLengthInput.value})
            });
            const data = await res.json();
            
            if(data.success) {
                activeKeyDisp.textContent = data.key;
                circuitDescDisp.textContent = data.circuit;
                
                let displayKey = data.key;
                if(displayKey.length > 64) displayKey = displayKey.slice(0, 64) + '...';
                dispKey.textContent = displayKey;
                
                addMessageToLog(senderLogs, 'System: New Quantum Key Initialized.', 'cipher');
                addMessageToLog(receiverLogs, 'System: New Quantum Key Initialized.', 'cipher');
            } else {
                activeKeyDisp.textContent = "Error generating key.";
            }
        } catch(err) {
            console.error(err);
            activeKeyDisp.textContent = "Connection error.";
        }
        
        genKeyBtn.disabled = false;
        genKeyBtn.textContent = "Generate Quantum Key";
    }

    async function sendMessage() {
        const text = msgInput.value.trim();
        if(!text) return;
        
        msgInput.value = '';
        
        // Show in sender immediately
        addMessageToLog(senderLogs, text, 'sent');
        
        try {
            const res = await fetch('/send_message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            const data = await res.json();
            
            if(data.success) {
                // Update Security Panel Visualizations
                dispPlain.textContent = data.original;
                dispCipher.textContent = data.cipher_bits;
                dispDecrypted.textContent = data.decrypted;
                
                let keyStr = data.used_key;
                if(keyStr.length > 100) keyStr = keyStr.substring(0, 100) + '...';
                dispKey.textContent = keyStr;
                
                // Receiver sees cipher first, then decrypts
                addMessageToLog(receiverLogs, `[ENCRYPTED] ${data.cipher_bits.substring(0, 40)}...`, 'cipher');
                
                setTimeout(() => {
                    addMessageToLog(receiverLogs, data.decrypted, 'received');
                }, 800); // simulated transit time

                // Update AI badge
                aiResult.className = `ai-badge ${data.classifier_result.toLowerCase()}`;
                aiResult.textContent = data.classifier_result;
            }
        } catch(err) {
            console.error(err);
        }
    }

    async function runAttackSim() {
        simAttackBtn.disabled = true;
        simAttackBtn.textContent = "Running Neural Network...";
        barClassical.style.width = '0%';
        barQuantum.style.width = '0%';
        pctClassical.textContent = '0%';
        pctQuantum.textContent = '0%';
        classicalBitsDisp.textContent = 'Analyzing...';
        quantumBitsDisp.textContent = 'Analyzing...';
        attackExplanation.style.display = 'none';
        
        try {
            const res = await fetch('/simulate_attack');
            const data = await res.json();
            
            // Show side-by-side bits immediately
            classicalBitsDisp.textContent = data.classical_bits;
            quantumBitsDisp.textContent = data.quantum_bits;

            setTimeout(() => {
                barClassical.style.width = data.classical_predictability;
                pctClassical.textContent = data.classical_predictability;
                
                barQuantum.style.width = data.quantum_predictability;
                pctQuantum.textContent = data.quantum_predictability;
                
                attackExplanation.textContent = data.explanation;
                attackExplanation.style.display = 'block';
                
                simAttackBtn.disabled = false;
                simAttackBtn.textContent = "Run ML Threat Simulation";
            }, 600);
            
        } catch(err) {
            console.error(err);
            simAttackBtn.disabled = false;
            simAttackBtn.textContent = "Run ML Threat Simulation";
        }
    }
});
