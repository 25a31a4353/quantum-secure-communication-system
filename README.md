# Quantum Secure Communication System

**Developed by: Medicharla Shanmukheswar**

A high-impact hackathon project demonstrating quantum-secure communication. We leverage Qiskit to create true randomness via quantum superposition collapses, providing an unbreakable XOR key stream. The project visualizes real-time encryption and simulates an AI-driven attack, comparing Classical PRNG predictability vs. Quantum TRNG unpredictability.

## Core Features
1. **Quantum Key Generation:** Integrates `qiskit` and `qiskit-aer` to measure superposition states and extract true random bits.
2. **Real-Time Encryption:** Applies the quantum keys directly onto messages via bitwise XOR.
3. **Attack Simulation:** Runs statistical prediction scenarios showing the weakness of classical randomness compared to quantum randomness.
4. **AI Message Classifier:** Scikit-Learn based multinomial naive-bayes model detecting `Safe`, `Spam`, or `Sensitive` information in transmitted messages.

## Tech Stack
* **Backend**: Python, Flask
* **Quantum Toolkit**: Qiskit, Qiskit-Aer
* **AI/ML**: Scikit-Learn
* **Frontend**: HTML5, Vanilla JS, Custom CSS (Dark Theme, Glassmorphism)

---

## Instructions to Run Local Demo

### 1. Prerequisite
Ensure you have Python 3.8+ installed.

### 2. Install Packages
Run the following command inside the project directory:
```bash
pip install -r requirements.txt
```

### 3. Start the Server
Start the Flask backend by running:
```bash
python app.py
```

### 4. Open Application
Navigate to `http://127.0.0.1:5000` in your web browser.

---

*Developed by Medicharla Shanmukheswar for the Quantum Hackathon.*

