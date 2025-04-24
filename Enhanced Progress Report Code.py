import qiskit

from qiskit import *
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.visualization import plot_state_city, plot_bloch_multivector
from qiskit.visualization import plot_histogram


n_qubits = 4
marked_state = '1101'

oracle = QuantumCircuit(n_qubits, name="Oracle")
oracle.x(0)
oracle.x(2)
oracle.h(3)
oracle.mcx([0, 1, 2], 3)  # multi-control X
oracle.h(3)
oracle.x(0)
oracle.x(2)
oracle_gate = oracle.to_gate(label="Oracle")

diffuser = QuantumCircuit(n_qubits, name="Diffuser")
diffuser.h(range(n_qubits))
diffuser.x(range(n_qubits))
diffuser.h(n_qubits - 1)
diffuser.mcx(list(range(n_qubits - 1)), n_qubits - 1)
diffuser.h(n_qubits - 1)
diffuser.x(range(n_qubits))
diffuser.h(range(n_qubits))
diffuser_gate = diffuser.to_gate(label="Diffuser")

grover = QuantumCircuit(n_qubits, n_qubits)
grover.h(range(n_qubits))
grover.append(oracle_gate, range(n_qubits))
grover.append(diffuser_gate, range(n_qubits))
grover.measure(range(n_qubits), range(n_qubits))

# Visualizar el circuito
grover.draw(output='mpl')
plt.show()

# Solo el circuito sin medición
grover_sv = QuantumCircuit(n_qubits)
grover_sv.h(range(n_qubits))
grover_sv.append(oracle_gate, range(n_qubits))
grover_sv.append(diffuser_gate, range(n_qubits))

# Obtener vector de estado sin ejecutar
statevector = Statevector.from_instruction(grover_sv)

plot_state_city(statevector)
plt.show()

plot_bloch_multivector(statevector)
plt.show()

counts_no_noise = statevector.sample_counts(shots=1024)

counts_noise = counts_no_noise.copy()
for key in counts_noise:
    counts_noise[key] = max(counts_noise[key] - np.random.randint(0, 10), 0)  # pequeños errores

from qiskit.visualization import plot_histogram

plot_histogram([counts_no_noise, counts_noise], legend=["Ideal", "Con ruido simulado"], title="Resultado de Grover")
plt.show()

