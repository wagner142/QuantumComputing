from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram

# Define the oracle for |11⟩
circuit = QuantumCircuit(2)
circuit.cz(0, 1)  # Phase inversion for |11⟩
circuit.draw()

