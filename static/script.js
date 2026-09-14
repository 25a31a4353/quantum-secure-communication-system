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
    const systemTerminal = document.getElementById('system-terminal');
    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    const themeToggleLabel = document.getElementById('theme-toggle-label');

    // System Terminal Logger
    function log(message, type = '') {
        if (!systemTerminal) return;
        const entry = document.createElement('div');
        entry.className = `log-entry ${type}`;
        entry.textContent = `> [${new Date().toLocaleTimeString()}] ${message}`;
        systemTerminal.appendChild(entry);
        systemTerminal.scrollTop = systemTerminal.scrollHeight;
        
        // Keep log from getting too long
        if (systemTerminal.children.length > 50) {
            systemTerminal.removeChild(systemTerminal.firstChild);
        }
    }

    // Bloch Sphere Setup
    let scene, camera, renderer, sphere, arrow, wireframe;
    initBlochSphere();

    // Theme Management (Light / Dark Mode)
    const savedTheme = localStorage.getItem('quantum_theme');
    const systemPrefersLight = window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches;
    const initialTheme = savedTheme || (systemPrefersLight ? 'light' : 'dark');

    function applyTheme(theme, logChange = false) {
        const isLight = theme === 'light';
        document.documentElement.setAttribute('data-theme', isLight ? 'light' : 'dark');
        
        if (themeToggleLabel) {
            themeToggleLabel.textContent = isLight ? 'Light Mode' : 'Dark Mode';
        }
        
        localStorage.setItem('quantum_theme', isLight ? 'light' : 'dark');
        updateBlochSphereTheme(isLight ? 'light' : 'dark');
        
        if (logChange) {
            log(`Theme shifted to ${isLight ? 'LIGHT' : 'DARK'} mode`, 'cmd');
        }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const current = document.documentElement.getAttribute('data-theme') || 'dark';
            const nextTheme = current === 'dark' ? 'light' : 'dark';
            applyTheme(nextTheme, true);
        });
    }

    // Apply active theme immediately
    applyTheme(initialTheme, false);

    // System Status Monitor
    async function updateSystemStatus() {
        try {
            const res = await fetch('/system_status');
            const data = await res.json();
            log(`Hardware Probe: Temp=${data.qubit_temperature}, Error=${data.error_rate}`, 'status-update');
        } catch(err) {
            console.error('Status fetch failed');
        }
    }

    // Update status every 30 seconds
    setInterval(updateSystemStatus, 30000);

    // Auto-generate key on load
    setTimeout(() => {
        log('System online. Quantum kernel ready.', 'cmd');
        generateKey();
    }, 500);

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
        genKeyBtn.classList.add('loading');
        
        log('Initializing Quantum Circuit...', 'quantum');
        log('Applying Hadamard transformation matrix...', 'quantum');
        
        activeKeyDisp.textContent = "Synthesizing Quantum Entanglement...";
        updateBlochState(Math.PI / 2, 0); // H gate moves |0> to (|0>+|1>)/sqrt(2) which is on the X-axis
        
        try {
            const res = await fetch('/generate_key', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({length: keyLengthInput.value})
            });
            const data = await res.json();
            
            if(data.success) {
                // Simulate measurent collapse
                log('Measuring qubits... collapsing wave function.', 'quantum');
                log(`Key generated successfully: ${data.key.length} bits.`, 'cmd');

                // Return to a random ground or excited state for visual variety after measurement
                const finalState = data.key[0] === '0' ? 0 : Math.PI;
                updateBlochState(finalState, 0);

                setTimeout(() => {
                    activeKeyDisp.textContent = data.key;
                    circuitDescDisp.textContent = data.circuit;
                    
                    let displayKey = data.key;
                    if(displayKey.length > 64) displayKey = displayKey.slice(0, 64) + '...';
                    dispKey.textContent = displayKey;
                    
                    addMessageToLog(senderLogs, 'System: New Quantum Key Loaded.', 'cipher');
                    addMessageToLog(receiverLogs, 'System: New Quantum Key Loaded.', 'cipher');
                }, 500);
            } else {
                log('Circuit Error: ' + data.error, 'warn');
                activeKeyDisp.textContent = "Error generating key.";
            }
        } catch(err) {
            console.error(err);
            log('Connection to Q-Server failed.', 'warn');
            activeKeyDisp.textContent = "Connection error.";
        }
        
        genKeyBtn.disabled = false;
        genKeyBtn.classList.remove('loading');
    }

    async function sendMessage() {
        const text = msgInput.value.trim();
        if(!text) return;
        
        msgInput.value = '';
        log(`Encrypting message payload: "${text.substring(0, 15)}..."`, 'cmd');
        
        addMessageToLog(senderLogs, text, 'sent');
        
        try {
            const res = await fetch('/send_message', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            const data = await res.json();
            
            if(data.success) {
                log('XOR logic applied with Quantum OTP.', 'cmd');
                log('Packet transmitted via secure channel.', 'cmd');

                dispPlain.textContent = data.original;
                dispCipher.textContent = data.cipher_bits;
                dispDecrypted.textContent = data.decrypted;
                
                let keyStr = data.used_key;
                if(keyStr.length > 100) keyStr = keyStr.substring(0, 100) + '...';
                dispKey.textContent = keyStr;
                
                addMessageToLog(receiverLogs, `[ENCRYPTED] ${data.cipher_bits.substring(0, 40)}...`, 'cipher');
                
                setTimeout(() => {
                    log('Message decrypted by receiver.', 'cmd');
                    addMessageToLog(receiverLogs, data.decrypted, 'received');
                }, 800);

                aiResult.className = `ai-badge ${data.classifier_result.toLowerCase()}`;
                aiResult.textContent = data.classifier_result;
                if(data.classifier_result === 'Sensitive') {
                    log('AI Alert: Sensitive data detected in stream!', 'warn');
                }
            }
        } catch(err) {
            console.error(err);
            log('Transmission error.', 'warn');
        }
    }

    async function runAttackSim() {
        simAttackBtn.disabled = true;
        log('Starting ML Adversarial Simulation...', 'warn');
        log('Training Gradient Boosting Regressor on PRNG data...', 'warn');
        
        simAttackBtn.textContent = "Simulation Running...";
        barClassical.style.width = '0%';
        barQuantum.style.width = '0%';
        pctClassical.textContent = '0%';
        pctQuantum.textContent = '0%';
        classicalBitsDisp.textContent = 'Sniffing Traffic...';
        quantumBitsDisp.textContent = 'Sniffing Traffic...';
        attackExplanation.style.display = 'none';
        
        try {
            const res = await fetch('/simulate_attack');
            const data = await res.json();
            
            setTimeout(() => {
                classicalBitsDisp.textContent = data.classical_bits;
                quantumBitsDisp.textContent = data.quantum_bits;
                log('Bitstream analysis complete.', 'cmd');
                
                setTimeout(() => {
                    barClassical.style.width = data.classical_predictability;
                    pctClassical.textContent = data.classical_predictability;
                    
                    barQuantum.style.width = data.quantum_predictability;
                    pctQuantum.textContent = data.quantum_predictability;
                    
                    attackExplanation.textContent = data.explanation;
                    attackExplanation.style.display = 'block';
                    
                    log(`Predictability Result: C=${data.classical_predictability}, Q=${data.quantum_predictability}`, 'cmd');
                    log('Simulation complete.', 'cmd');
                    
                    simAttackBtn.disabled = false;
                    simAttackBtn.textContent = "Run ML Threat Simulation";
                }, 800);
            }, 1000);
            
        } catch(err) {
            console.error(err);
            simAttackBtn.disabled = false;
            simAttackBtn.textContent = "Run ML Threat Simulation";
        }
    }

    // Three.js Functions
    function initBlochSphere() {
        const container = document.getElementById('bloch-sphere-container');
        if (!container) return;
        const width = container.clientWidth || 300;
        const height = container.clientHeight || 200;

        scene = new THREE.Scene();
        camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
        camera.position.z = 2.5;

        renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(width, height);
        container.appendChild(renderer.domElement);

        // Sphere
        const geometry = new THREE.SphereGeometry(1, 32, 32);
        const material = new THREE.MeshPhongMaterial({
            color: 0x9d00ff,
            transparent: true,
            opacity: 0.15,
            wireframe: false
        });
        sphere = new THREE.Mesh(geometry, material);
        scene.add(sphere);

        // Wireframe
        const wireGeometry = new THREE.SphereGeometry(1.01, 16, 16);
        const wireMaterial = new THREE.MeshBasicMaterial({
            color: 0x9d00ff,
            wireframe: true,
            transparent: true,
            opacity: 0.1
        });
        wireframe = new THREE.Mesh(wireGeometry, wireMaterial);
        scene.add(wireframe);

        // Axes
        const axesHelper = new THREE.AxesHelper(1.2);
        axesHelper.material.opacity = 0.5;
        axesHelper.material.transparent = true;
        scene.add(axesHelper);

        // State Arrow
        const dir = new THREE.Vector3(0, 1, 0);
        const origin = new THREE.Vector3(0, 0, 0);
        arrow = new THREE.ArrowHelper(dir, origin, 1.1, 0x00f2ff, 0.2, 0.1);
        scene.add(arrow);

        // Lighting
        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(5, 5, 5);
        scene.add(light);
        scene.add(new THREE.AmbientLight(0x404040));

        animate();

        window.addEventListener('resize', () => {
            const w = container.clientWidth;
            const h = container.clientHeight;
            renderer.setSize(w, h);
            camera.aspect = w / h;
            camera.updateProjectionMatrix();
        });
    }

    function updateBlochSphereTheme(theme) {
        if (!sphere || !wireframe || !arrow) return;
        if (theme === 'light') {
            sphere.material.color.setHex(0x7928ca);
            sphere.material.opacity = 0.22;
            wireframe.material.color.setHex(0x7928ca);
            wireframe.material.opacity = 0.16;
            arrow.setColor(0x008fa0);
        } else {
            sphere.material.color.setHex(0x9d00ff);
            sphere.material.opacity = 0.15;
            wireframe.material.color.setHex(0x9d00ff);
            wireframe.material.opacity = 0.1;
            arrow.setColor(0x00f2ff);
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        if (sphere) sphere.rotation.y += 0.005;
        if (wireframe) wireframe.rotation.y += 0.005;
        if (renderer && scene && camera) renderer.render(scene, camera);
    }

    function updateBlochState(theta, phi) {
        if (!arrow || !sphere) return;
        const x = Math.sin(theta) * Math.cos(phi);
        const z = Math.cos(theta);
        const y = Math.sin(theta) * Math.sin(phi);
        
        const newDir = new THREE.Vector3(x, z, y);
        arrow.setDirection(newDir);
        
        // Glow effect on update
        const isLight = document.documentElement.getAttribute('data-theme') === 'light';
        sphere.material.opacity = 0.5;
        setTimeout(() => {
            sphere.material.opacity = isLight ? 0.22 : 0.15;
        }, 300);
    }
});
