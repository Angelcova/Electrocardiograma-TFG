import numpy as np
import wfdb
import matplotlib.pyplot as plt

record_name = "s1_high_resistance_bike"
record = wfdb.rdrecord("s1_high_resistance_bike")

# Variable que recoge la frecuencia de muestreo
fs = record.fs

#Se carga la señal ECG
ecg_signal = record.p_signal[:, 0]

# Se carga el documento de anotaciones
annotations = wfdb.rdann("s1_high_resistance_bike", "atr")

hr_list = []
time_hr = []
aux_pre = annotations.sample[0]/fs

#Se calcula la frecuencia cardiaca mediante la información de las anotaciones
for i in range(1,len(annotations.sample)):
    aux_post = annotations.sample[i]/fs
    time_hr.append(aux_post)
    lpm = 60/(abs(aux_pre-aux_post))
    hr_list.append(lpm)
    aux_pre = aux_post

# Se obtiene el eje X de la señal del ECG
time_ECG = np.arange(len(ecg_signal)) / fs

# Gráfica 1 (ECG) con cuadritos cada 0,04 s
plt.figure(figsize=(12, 4))
plt.plot(time_ECG, ecg_signal, label="ECG")

plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.minorticks_on()
plt.gca().set_xticks(np.arange(0, time_ECG[len(time_ECG)-1], 0.04), minor=True)
plt.gca().set_yticks(np.arange(-1, 1.1, 0.1), minor=True)

plt.title(f"ECG archivo {record_name}")
plt.xlabel("Tiempo (s)")
plt.ylabel("Voltaje (mV)")
plt.legend()

# Gráfica 2 (HR)
plt.figure(figsize=(12, 4))
plt.plot(time_hr, hr_list, label="FC", marker="o")
plt.ylabel("HR (bpm)")
plt.xlabel("Tiempo (s)")
plt.title("Frecuencia Cardiaca")

plt.grid()
plt.tight_layout()
plt.show()
