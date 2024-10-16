import numpy as np
import matplotlib.pyplot as plt
from random import randint, choice


def graph_funtion(y,q_wave_time,s_wave_time,r_wave_time,p_wave_time,pr_interlude_time,st_section_time,t_wave_time):
    # 1. Transición Inicial
    start = 0
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

    return r_end

def generate_ecg_single_signal():
    # Generación de datos aleatorios de los puntos clave del ECG y el tiempo total de duracion del latido
    q_wave_time = randint(20, 30)
    s_wave_time = randint(15, 20)
    r_wave_time = randint(60, (119 - (q_wave_time + s_wave_time))) # Variable que debe variar entre 60 y 119 (ya que qrs no debe superar este valor) - los otros valores del complejo
    qrs_time = q_wave_time + r_wave_time + s_wave_time  # Tiempo total del complejo QRS

    p_wave_time = randint(80, 120)
    pr_section_time = randint(130, 200)
    pr_interlude_time = pr_section_time - p_wave_time

    st_section_time = randint(50, 150)
    t_wave_time = randint(130, 150)
    qt_section_time = qrs_time + st_section_time + t_wave_time  # Tiempo total del segmento QT


    partial_time = pr_section_time + qt_section_time
    total_time = randint(max(partial_time, 600), 1000)  # Tiempo que dura el latido calculado

    # Definición de los puntos en ambos ejes
    x = np.arange(0, partial_time, 1)  # Tiempo en milisegundos
    y = np.zeros(len(x))
    r_end = graph_funtion(y,q_wave_time, s_wave_time, r_wave_time, p_wave_time, pr_interlude_time, st_section_time, t_wave_time)

    return y, partial_time, total_time,r_end

def generate_ecg_rr_based(total_time):
    # Porcentajes aproximados basados en proporciones típicas de un ECG
    p_wave_percentage = 0.15  # 10% del RR
    pr_section_percentage = 0.2  # 20% del RR (incluye onda P)
    q_wave_percentage = 0.05  # 5% del RR
    r_wave_percentage = 0.15  # 15% del RR
    s_wave_percentage = 0.05  # 5% del RR
    st_section_percentage = 0.10  # 20% del RR
    t_wave_percentage = 0.2  # 15% del RR

    # Parametros porcentuales a rr pasados a int
    p_wave_time = int(p_wave_percentage * total_time)
    pr_section_time = int(pr_section_percentage * total_time)
    q_wave_time = int(q_wave_percentage * total_time)
    r_wave_time = int(r_wave_percentage * total_time)
    s_wave_time = int(s_wave_percentage * total_time)
    st_section_time = int(st_section_percentage * total_time)
    t_wave_time = int(t_wave_percentage * total_time)
    pr_interlude_time = pr_section_time - p_wave_time

    # Tiempo total del segmento QT (QRS + ST + T)
    qrs_time = q_wave_time + r_wave_time + s_wave_time
    qt_section_time = qrs_time + st_section_time + t_wave_time

    # Definición de los puntos en ambos ejes
    partial_time = pr_section_time + qt_section_time  # Tiempo parcial del ECG (excluye la porción final plana)
    x = np.arange(0, total_time, 1)  # Tiempo en milisegundos
    y = np.zeros(len(x))

    r_end = graph_funtion(y,q_wave_time,s_wave_time,r_wave_time,p_wave_time,pr_interlude_time,st_section_time,t_wave_time)

    return y, partial_time, total_time, r_end

def generate_ecg_one_minute_signal():
    total_ecg_time = 60000  # Duración del ECG sintetico
    ecg_signal = np.array([])  # Array encargado de guardar los latidos
    accumulated_time = 0  # Tiempo acumulado en milisegundos
    completed_beats = 0

    first_beat, parcial, time_beat, r1 = generate_ecg_single_signal() # Se calcula un solo latido con el que se generara todo el electrocardiograma
    ecg_signal = np.concatenate((ecg_signal,first_beat))
    accumulated_time += parcial
    completed_beats +=1
    rr = time_beat

    # Generar latidos hasta aproximarse a los 60 segundos
    while completed_beats < 10:
        beat, parcial_pos ,time_beat_pos, r_pos = generate_ecg_single_signal()  # Se calcula un solo latido con el que se generara todo el electrocardiograma
        time_0 = rr - ((parcial -r1) + r_pos)
        if time_0 < 0:
            time_0 = 0
        flat_section = np.zeros(time_0)
        if ((parcial -r1) + r_pos + time_0)== rr:
            flat_section = np.concatenate((flat_section,beat))
            # Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
            if accumulated_time + rr > total_ecg_time:
                duracion_restante = total_ecg_time - accumulated_time
                flat_section = flat_section[:duracion_restante]
                accumulated_time += duracion_restante
            else:
                accumulated_time += parcial_pos + time_0
                completed_beats+=1
            ecg_signal = np.concatenate((ecg_signal, flat_section))
            parcial = parcial_pos
            r1 = r_pos

    flat_section = np.zeros(int(time_0/2))
    ecg_signal = np.concatenate((ecg_signal,flat_section))
    accumulated_time += int(time_0/2)

    resting_time = accumulated_time
    resting_beats = completed_beats
    hr_target = randint(120, 180)
    print("Objetivo de latidos:",hr_target)
    hrv = randint(39, 85)
    rr_target = int(60000 / hr_target)

    while rr - hrv > rr_target and accumulated_time < total_ecg_time:
        rr -= hrv
        hrv = randint(39, 85)
        beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma

        if accumulated_time + rr > total_ecg_time:
            duracion_restante = total_ecg_time - accumulated_time
            beat = beat[:duracion_restante]  # Ajustar el último latido
            accumulated_time += duracion_restante
        else:
            accumulated_time += rr
            completed_beats += 1

        ecg_signal = np.concatenate((ecg_signal, beat))
    transition_time = accumulated_time
    transition_beats = completed_beats - resting_beats
    print("Latidos de transicion:",transition_beats)
    rr = rr_target
    while accumulated_time < total_ecg_time:
        hrv = randint(39, 85)
        hrv = choice([-hrv,hrv])
        rr_aux = rr
        rr += hrv
        if rr_target - 50 <= rr <= rr_target + 50:
            beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma
            if accumulated_time + rr > total_ecg_time:
                duracion_restante = total_ecg_time - accumulated_time
                beat = beat[:duracion_restante]  # Ajustar el último latido
                accumulated_time += duracion_restante
            else:
                accumulated_time += rr
                completed_beats += 1
            ecg_signal = np.concatenate((ecg_signal, beat))
        else:
            rr = rr_aux
    x = np.arange(0, len(ecg_signal), 1)  # Tiempo en milisegundos
    movement_beats = completed_beats - (transition_beats + resting_beats)
    print("Latidos en moviemiento:", movement_beats)
    movement_time = accumulated_time
    return x, ecg_signal,completed_beats,resting_time,transition_time,movement_time

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
    x, y, lpm,resting,transition,movement = generate_ecg_one_minute_signal()
    print("Latidos totales:",lpm)

    resting_mask = np.arange(movement) < resting
    transition_mask = (np.arange(movement) >= resting) & (np.arange(movement) < transition)
    movement_mask = np.arange(movement) >= transition

    # Graficar la señal de ECG
    plt.figure(figsize=(20, 5))
    plt.plot(x[resting_mask] / 1000, y[resting_mask], color='green', label='Reposo')  # Fase de descanso
    plt.plot(x[transition_mask] / 1000, y[transition_mask], color='orange', label='Transición')  # Fase de transición
    plt.plot(x[movement_mask] / 1000, y[movement_mask], color='red', label='Movimiento')  # Fase de movimiento

    # Etiquetas con el formato MM:SS
    ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
    tick_labels = [ms_to_min(t * 1000) for t in ticks]
    plt.xticks(ticks, tick_labels)

    # Titulo y etiquetas para cada dimensión
    plt.title("ECG Sintético de 1 Minuto")
    plt.xlabel("Tiempo (MM:SS)")
    plt.ylabel("Voltaje (mV)")
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.xlim(0, 4)  # Limitar el eje X de 0 a 2 segundos
    plt.tight_layout()  # Ajustar el layout para evitar solapamientos
    plt.grid(True)
    plt.show()



