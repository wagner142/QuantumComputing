import qiskit
from qiskit import QuantumCircuit
import matplotlib.pyplot as plt
import numpy as np
from qiskit.quantum_info import Statevector
from qiskit.visualization import (
    plot_state_city,
    plot_bloch_multivector,
    plot_histogram
)

# Configuración inicial
n_qubits = 4
marked_state = '1101'  # Estado objetivo que Grover debe buscar

# Oracle: marca el estado '1101'
oracle = QuantumCircuit(n_qubits, name="Oracle")

# Transformar '1101' en '1111' para usar compuerta multi-controlada
oracle.x(0)
oracle.x(2)
oracle.h(3)
oracle.mcx([0, 1, 2], 3)  # Compuerta X con 3 controles
oracle.h(3)
oracle.x(0)
oracle.x(2)

oracle_gate = oracle.to_gate(label="Oracle")

# Difusor (inversión sobre la media)
diffuser = QuantumCircuit(n_qubits, name="Diffuser")
diffuser.h(range(n_qubits))
diffuser.x(range(n_qubits))
diffuser.h(n_qubits - 1)
diffuser.mcx(list(range(n_qubits - 1)), n_qubits - 1)
diffuser.h(n_qubits - 1)
diffuser.x(range(n_qubits))
diffuser.h(range(n_qubits))

diffuser_gate = diffuser.to_gate(label="Diffuser")

# Circuito completo con medición
grover = QuantumCircuit(n_qubits, n_qubits)
grover.h(range(n_qubits))                      # Inicialización en superposición
grover.append(oracle_gate, range(n_qubits))    # Aplicar oracle
grover.append(diffuser_gate, range(n_qubits))  # Aplicar difusor
grover.measure(range(n_qubits), range(n_qubits))  # Medición final

# Visualizar el circuito
grover.draw(output='mpl')
plt.show()

# Estado cuántico sin medidas (para análisis)
grover_sv = QuantumCircuit(n_qubits)
grover_sv.h(range(n_qubits))
grover_sv.append(oracle_gate, range(n_qubits))
grover_sv.append(diffuser_gate, range(n_qubits))

# Calcular el vector de estado final
statevector = Statevector.from_instruction(grover_sv)

# Visualizar el estado en formato "city plot"
plot_state_city(statevector, title="Estado cuántico final (City plot)")
plt.show()

# Visualizar en esfera de Bloch (todos los cúbits)
plot_bloch_multivector(statevector, title="Esfera de Bloch (todos los cúbits)")
plt.show()

# Simulación de conteos
# Generar conteos ideales a partir del vector de estado
counts_no_noise = statevector.sample_counts(shots=1024)

# Simular ruido básico: perturbar ligeramente los conteos ideales
counts_noise = counts_no_noise.copy()
for key in counts_noise:
    # Restar hasta 9 cuentas aleatoriamente (imitando errores)
    counts_noise[key] = max(counts_noise[key] - np.random.randint(0, 10), 0)

# Visualizar comparación de resultados
plot_histogram(
    [counts_no_noise, counts_noise],
    legend=["Ideal", "Con ruido simulado"],
    title="Resultado del algoritmo de Grover"
)
plt.show()

