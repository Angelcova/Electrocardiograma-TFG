import csv
import wfdb
import neurokit2 as nk
import numpy as np
from matplotlib import pyplot as plt
from numpy.ma.extras import average

# Se obtiene los datos del fichero
record_name = "0001"
record = wfdb.rdrecord("0001")
fs = record.fs

#Se guarda la señal del ECG
ecg = record.p_signal[:, 0]

signals, info = nk.ecg_process(ecg, sampling_rate=fs)

#Se calcula y se muestra información util por consola
total_instances = len(ecg)
r_peaks = info["ECG_R_Peaks"]
num_beats = len(r_peaks)
min_time = total_instances / fs / 60
avg_hr = num_beats / min_time
rr_intervals = np.diff(r_peaks) / fs
avgRR = np.mean(rr_intervals)

print(f"Total de muestras: {total_instances}")
print(f"Total de latidos: {num_beats}")
print(f"Frecuencia cardíaca media: {avg_hr:.2f} bpm")
print(f"Duración media entre latidos (R-R): {avgRR:.3f} s")


# Se detectan los picos R del ECG
_, rpeaks = nk.ecg_peaks(ecg, sampling_rate=fs)
r_peaks = rpeaks["ECG_R_Peaks"]

#Se eliminan aquellos que son nulos
r_peaks = r_peaks[r_peaks != 0]

# Se calculan los intervalos R-R
rr_intervals = np.diff(r_peaks) / fs  # en segundos

# Se calcula la frecuencia cardiaca en cada punto
hr_values = 60 / rr_intervals

# Se calcula información util sobre la FC y se muestra
hr_diffs = np.abs(np.diff(hr_values))
hr_jump_max = np.max(hr_diffs)
hr_min = np.min(hr_values)
hr_max = np.max(hr_values)

print(f"FC mínimo: {hr_min:.2f} bpm")
print(f"HR máximo: {hr_max:.2f} bpm")
print(f"Mayor salto entre HR consecutivos: {hr_jump_max:.2f} bpm")

# Se pasa a segundos
time_beats = r_peaks[1:] / fs  # usar los latidos después del primero (por eso 1:), ya que RR y HR empiezan desde ahí
option = 1

time_hr_sint = []
hr_sint = []

with open('HRreposo.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        time_hr_sint.append(float(row[0])/1000)
        hr_sint.append(float(row[1]))


n_samples = len(record.p_signal)

tiempo_ECG = [i / fs for i in range(n_samples)]


while option != 0:
    print("Que intervalo de 30s deseas ver")
    option = int(input())
    if option != 0:
        tiempo_aux = [i + (30 * (option - 1)) for i in time_hr_sint]

        #Grafico 1, Comparación FC
        plt.figure(figsize=(12, 4))
        plt.plot(time_beats, hr_values, marker='o', linestyle='-', color='green', label='FC Base de datos(lpm)')
        plt.plot(tiempo_aux,hr_sint,marker='o', linestyle='-', color='blue', label='FC Sintetico (lpm)')
        plt.title(f'Comparación frecuencias cardiacas en reposo ({record_name})')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('FC (lpm)')
        plt.grid(True)
        plt.legend()
        plt.xlim(30*(option-1),(30 * (option-1)) + 30) #limitación a 30 segundos

        #Se muestra por consola la media de la FC en dicho intervalo
        print(average(hr_values[30*(option-1):30 * (option-1) + 30]))

        #Grafico 2, ECG real del intervalo
        plt.figure(figsize=(12, 4))
        plt.plot(tiempo_ECG, record.p_signal[:, 0], label=record.sig_name[0])

        #Representación de los cuadritos de 0,04 s
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.gca().set_xticks(np.arange(30*(option-1), (30 * (option-1)) + 30, 0.04), minor=True)
        plt.gca().set_yticks(np.arange(-1, 1.6, 0.1), minor=True)

        plt.title('ECG en reposo de la BD')
        plt.xlabel('Tiempo (s)')
        plt.ylabel('Voltaje (mV)')
        plt.legend()
        plt.xlim(30 * (option - 1), (30 * (option - 1)) + 30)  # limitación a 30 segundos

        plt.tight_layout()
        plt.show()
