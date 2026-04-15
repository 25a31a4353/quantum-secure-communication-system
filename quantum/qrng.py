import random

# Attempt robust imports of qiskit components
try:
    from qiskit import QuantumCircuit
    has_qiskit = True
    try:
        from qiskit_aer import AerSimulator
        has_aer = True
    except ImportError:
        try:
            # Fallback for older qiskit versions
            from qiskit import Aer
            has_aer = True
        except ImportError:
            has_aer = False
except ImportError:
    has_qiskit = False
    has_aer = False

def generate_quantum_key(length):
    """
    Generates a random sequence of bits measuring qubits in superposition.
    Returns the key string and a descriptive log of the circuit.
    """
    try:
        if not has_qiskit:
            raise Exception("Qiskit not installed.")
            
        qc = QuantumCircuit(length, length)
        # Apply Hadamard gates to put all qubits in superposition
        for i in range(length):
            qc.h(i)
        # Measure all qubits
        qc.measure(range(length), range(length))
        
        circuit_desc = f"1. Initialized {length} qubits to |0⟩\n2. Applied Hadamard (H) gates to create superposition state: α|0⟩ + β|1⟩\n3. Measured qubits collapsing state to basis {length}-bit string."
        
        if has_aer:
            try:
                simulator = AerSimulator()
            except NameError:
                simulator = Aer.get_backend('qasm_simulator')
            
            job = simulator.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            
            # The counts dict has only one element because shots=1
            key = list(counts.keys())[0]
            # Reverse key to match standard ordering
            key = key[::-1]
            return key, circuit_desc
        else:
            raise Exception("No Aer simulator available.")
            
    except Exception as e:
        print("Fallback to simulated quantum system due to error:", e)
        # Safe fallback so demo doesn't crash if Qiskit environment breaks
        circuit_desc = f"SIMULATED SYSTEM:\nFallback engaged due to lack of Quantum environment.\n1. Target Length: {length}\n2. System Generated Randomness as substitute for collapse."
        return "".join([str(random.randint(0, 1)) for _ in range(length)]), circuit_desc
