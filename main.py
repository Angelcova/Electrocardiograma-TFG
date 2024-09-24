import numpy as np
import matplotlib.pyplot as plt
from random import randint

def generate_ecg_single_signal():
    # Generación de datos aleatorios de los puntos clave del ECG y el tiempo total de duracion del latido
    initial_transition_time = 20 # ¿quitar?
    pr_section_time = randint(130, 200)
    q_wave_time = randint(20, 30)
    p_wave_time = randint(80,120)
    pr_interlude_time = pr_section_time - p_wave_time
    s_wave_time = randint(15, 20)
    r_wave_time = randint(60, (119 - (q_wave_time + s_wave_time))) # Variable que debe variar entre 60 y 119 (ya que qrs no debe superar este valor) - los otros valores del complejo
    st_section_time = randint(50, 150)
    t_wave_time = randint(130, 150)
    qt_section_time = randint(s_wave_time + r_wave_time + st_section_time + t_wave_time, 450)

    partial_time = initial_transition_time + pr_section_time + qt_section_time
    total_time = randint(max(partial_time,600), 1000) # Tiempo que dura el latido calculado
    print(total_time)

    # Definición de los puntos en ambos ejes
    x = np.arange(0, total_time, 1)  # Tiempo en milisegundos
    y = np.zeros(len(x))

    # 1. Transición Inicial
    start = initial_transition_time
    y[:start] = 0  # Línea plana en 0 mV

    # 2. Onda P
    p_start = start
    p_time = np.linspace(0, p_wave_time, p_wave_time)
    p_wave = 0.15 * np.sin(np.pi * p_time / p_wave_time)
    y[p_start:p_start + p_wave_time] = p_wave

    # 3. Transición de P a Q (zona plana)
    pq_start = p_start + p_wave_time
    pq_end = pq_start + pr_interlude_time
    y[pq_start:pq_end] = 0  # Línea plana

    # 4. Complejo QRS
    qrs_start = pq_end

    # 4.1 Onda Q
    q_start = qrs_start
    q_end = qrs_start + q_wave_time
    q_wave = np.linspace(0, -0.15, q_wave_time)
    y[q_start:q_end] = q_wave

    # 4.2 Onda R
    r_start = q_end
    r_end = r_start + r_wave_time // 2
    r_wave = np.linspace(-0.15, 0.9, r_wave_time // 2)
    y[r_start:r_end] = r_wave

    # 4.3 Onda S (bajada hasta 0.3 mV)
    s_start = r_end
    s_end = s_start + r_wave_time // 2
    s_wave = np.linspace(0.9, -0.3, r_wave_time // 2)
    y[s_start:s_end] = s_wave

    # 4.4 Trasicion de S a T(subida desde 0.3 hasta 0)
    st_start = s_end
    st_end = st_start + s_wave_time
    st_wave = np.linspace(-0.3, 0, s_wave_time)
    y[st_start:st_end] = st_wave

    # 5. Trasicion de S a T(zona plana)
    st2_start = st_end
    st2_wave = np.zeros(st_section_time)
    y[st2_start:st2_start + st_section_time] = st2_wave

    # 6. Onda T
    t_start = st_start + st_section_time
    t_time = np.linspace(0, t_wave_time, t_wave_time)
    t_wave = 0.3 * np.sin(np.pi * t_time / t_wave_time)
    y[t_start:t_start + t_wave_time] = t_wave

    return y, total_time

def generate_ecg_one_minute_signal():
    total_ecg_time = 60000  # Duración del ECG sintetico
    ecg_signal = np.array([])  # Array encargado de guardar los latidos
    accumulated_time = 0  # Tiempo acumulado en milisegundos
    completed_beats = 0

    beat, time_beat = generate_ecg_single_signal() # Se calcula un solo latido con el que se generara todo el electrocardiograma

    # Generar latidos hasta aproximarse a los 60 segundos
    while accumulated_time < total_ecg_time:

        # Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
        if accumulated_time + time_beat > total_ecg_time:
            duracion_restante = total_ecg_time - accumulated_time
            beat = beat[:duracion_restante]  # Ajustar el último latido
            accumulated_time += duracion_restante
        else:
            accumulated_time += time_beat
            completed_beats+=1

        ecg_signal = np.concatenate((ecg_signal, beat))

    x = np.arange(0, len(ecg_signal), 1)  # Tiempo en milisegundos


    return x, ecg_signal,completed_beats

def ms_to_min(milisegundos):
    # MS --> S
    total_sec = milisegundos // 1000
    # MIM Y S
    min = total_sec // 60
    sec = total_sec % 60
    # Formato MM:SS
    return f"{min:02d}:{sec:02d}"

if __name__ == "__main__":
    # Obtención de los datos a mostrar
    x, y, lpm = generate_ecg_one_minute_signal()

    print(lpm)
    # Graficar la señal de ECG
    plt.figure(figsize=(20, 5))
    plt.plot(x / 1000, y)  # El eje X se muestra en segundos aunque se calcule en segundos

    # Etiquetas con el formato MM:SS
    ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
    tick_labels = [ms_to_min(t * 1000) for t in ticks]
    plt.xticks(ticks, tick_labels)

    # Titulo y etiquetas para cada dimensión
    plt.title("ECG Sintético de 1 Minuto")
    plt.xlabel("Tiempo (MM:SS)")
    plt.ylabel("Voltaje (mV)")
    plt.grid(True)
    plt.show()



