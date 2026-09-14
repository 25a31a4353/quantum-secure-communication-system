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

## Streamlit Deployment

You can run this project as a Streamlit app (no Flask server required).

1. Install requirements (see above).
2. Start Streamlit:

```bash
streamlit run streamlit_app.py
```

The Streamlit UI exposes the same core features: quantum key generation, XOR encryption, message classification, and the ML attack simulation. For lightweight demos you can skip `qiskit` (the project falls back to a simulated TRNG when Qiskit/Aer are unavailable).

### CI / Auto-deploy with GitHub Actions

This repository includes a GitHub Actions workflow that triggers a Streamlit Cloud redeploy on pushes to `main`:

- Workflow: [.github/workflows/deploy-streamlit.yml](.github/workflows/deploy-streamlit.yml)

Before the workflow can trigger a deploy, add these repository secrets in GitHub (Settings → Secrets → Actions):

- `STREAMLIT_CLOUD_TOKEN` — a deploy token from Streamlit Cloud (Teams/Enterprise) or an API token from your account.
- `STREAMLIT_APP_ID` — the Streamlit app ID to redeploy (visible in Streamlit Cloud app settings).

On push to `main` the workflow will call the Streamlit deploy API to request a new deployment for the specified app and branch.

If you don't have Streamlit Cloud tokens, you can still use the app by running locally with `streamlit run streamlit_app.py`.

---

*Developed by Medicharla Shanmukheswar for the Quantum Hackathon.*

