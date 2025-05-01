import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from random import randint, choice, random
import random

def graph_funtion(y,q_wave_time,s_wave_time,r_wave_time,p_wave_time,pr_interlude_time,st_section_time,t_wave_time):
    # Transición Inicial
    start = 0
    y[:start] = 0  # Línea plana en 0 mV

    # Onda P
    p_start = start
    p_time = np.linspace(0, p_wave_time, p_wave_time)
    p_wave = 0.15 * np.sin(np.pi * p_time / p_wave_time)
    y[p_start:p_start + p_wave_time] = p_wave

    # Transición de P a Q (zona plana)
    pq_start = p_start + p_wave_time
    pq_end = pq_start + pr_interlude_time
    y[pq_start:pq_end] = 0  # Línea plana

    # Complejo QRS
    qrs_start = pq_end

    # Onda Q
    q_start = qrs_start
    q_end = qrs_start + q_wave_time
    q_wave = np.linspace(0, -0.15, q_wave_time)
    y[q_start:q_end] = q_wave

    # Onda R
    r_start = q_end
    r_end = r_start + r_wave_time // 2
    r_wave = np.linspace(-0.15, 0.9, r_wave_time // 2)
    y[r_start:r_end] = r_wave

    # Onda S (bajada hasta 0.3 mV)
    s_start = r_end
    s_end = s_start + r_wave_time // 2
    s_wave = np.linspace(0.9, -0.3, r_wave_time // 2)
    y[s_start:s_end] = s_wave

    # Trasicion de S a T(subida desde 0.3 hasta 0)
    st_start = s_end
    st_end = st_start + s_wave_time
    st_wave = np.linspace(-0.3, 0, s_wave_time)
    y[st_start:st_end] = st_wave

    # Trasicion de S a T(zona plana)
    st2_start = st_end
    st2_wave = np.zeros(st_section_time)
    y[st2_start:st2_start + st_section_time] = st2_wave

    # Onda T
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
    completed_beats = 0 # Latidos completados

    bpm_grap = [] # Se guardan los lpm en ese tiempo x
    hrv_graph = [] # Se guardan el hrv en ese tiempo x
    start = 0

    first_beat, parcial, time_beat, r1 = generate_ecg_single_signal() # Se calcula un solo latido con el que se generara todo el electrocardiograma
    ecg_signal = np.concatenate((ecg_signal,first_beat))
    accumulated_time += parcial
    completed_beats +=1
    rr = time_beat

    # Se generan los 10 primeros latidos en reposo
    while completed_beats < 10:
        beat, parcial_pos ,time_beat_pos, r_pos = generate_ecg_single_signal()
        time_0 = rr - ((parcial -r1) + r_pos)
        if time_0 < 0:
            time_0 = 0
        flat_section = np.zeros(time_0)
        # Si el tiempo de latido calculado es igual al rr, se tiene en cuenta el latido
        if ((parcial -r1) + r_pos + time_0)== rr:
            flat_section = np.concatenate((flat_section,beat))
            bpm_value = int(60000 / (parcial + time_0))
            bpm_grap.append((start + parcial + time_0, bpm_value))
            hrv_graph.append((start + parcial + time_0,rr-((parcial -r1) + r_pos + time_0)))

            #Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
            if accumulated_time + rr > total_ecg_time:
                duracion_restante = total_ecg_time - accumulated_time
                flat_section = flat_section[:duracion_restante]
                accumulated_time += duracion_restante
            else:
                accumulated_time += parcial_pos + time_0
                completed_beats+=1
            ecg_signal = np.concatenate((ecg_signal, flat_section))
            start = start + parcial + time_0
            parcial = parcial_pos
            r1 = r_pos


    flat_section = np.zeros(int(time_0/2))
    ecg_signal = np.concatenate((ecg_signal,flat_section))
    accumulated_time += int(time_0/2)

    resting_time = accumulated_time
    resting_beats = completed_beats

    # Se escoge un estado de estres aleatorio que modifica los hrv y lpm minimos y maximos a los que se puede llegar
    stress_status_list = ["muy alto","alto","medio","bajo","ninguno"]
    stress_status = choice([stress_status_list[0],stress_status_list[1],stress_status_list[2],stress_status_list[3],stress_status_list[4]])
    print(stress_status)
    hr_min = 0
    hr_max = 0
    hrv_min = 0
    hrv_max = 0

    if stress_status == "muy alto":
        hr_min = 170
        hr_max = 180
        hrv_min = 95
        hrv_max = 110

    elif stress_status == "alto":
        hr_min = 150
        hr_max = 169
        hrv_min = 80
        hrv_max = 100

    elif stress_status == "medio":
        hr_min = 140
        hr_max = 149
        hrv_min = 55
        hrv_max = 75

    elif stress_status == "bajo":
        hr_min = 120
        hr_max = 139
        hrv_min = 45
        hrv_max = 65

    elif stress_status == "ninguno":
        hr_min = 120
        hr_max = 180
        hrv_min = 39
        hrv_max = 85

    hr_target = randint(hr_min, hr_max)
    print("Objetivo de latidos:",hr_target)
    hrv = randint(hrv_min, hrv_max)
    rr_target = int(60000 / hr_target)

    # Se generan los latidos de transiccion
    while rr - hrv > rr_target and accumulated_time < total_ecg_time:
        rr -= hrv
        hrv = randint(hrv_min, hrv_max)
        beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma

        bpm_value = int(60000 / time_beat_pos)
        bpm_grap.append((start + time_beat_pos, bpm_value))

        hrv_graph.append((start + time_beat_pos,hrv))

        if accumulated_time + rr > total_ecg_time:
            duracion_restante = total_ecg_time - accumulated_time
            beat = beat[:duracion_restante]  # Ajustar el último latido
            accumulated_time += duracion_restante
        else:
            accumulated_time += rr
            completed_beats += 1
        start = start + time_beat_pos
        ecg_signal = np.concatenate((ecg_signal, beat))

    transition_time = accumulated_time
    transition_beats = completed_beats - resting_beats
    print("Latidos de transicion:",transition_beats)
    rr = rr_target
    fluctuation = 0
    #Dependiendo del nivel de estres, la fluctuacion de hrv va a ser mayor o menor
    if stress_status == "muy alto":
        hrv_min = 20
        hrv_max = 30
        fluctuation = 20

    elif stress_status == "alto":
        hrv_min = 31
        hrv_max = 44
        fluctuation = 35

    elif stress_status == "medio":
        hrv_min = 45
        hrv_max = 65
        fluctuation = 45

    elif stress_status == "bajo":
        hrv_min = 55
        hrv_max = 75
        fluctuation = 55

    elif stress_status == "ninguno":
        hrv_min = 39
        hrv_max = 85
        fluctuation = 55

    # Se generan los latidos en movimiento
    while accumulated_time < total_ecg_time:
        # Se escoge un valor aleatorio enter los maximos y los minimos de hrv, también su signo
        hrv = randint(hrv_min, hrv_max)
        hrv = choice([-hrv,hrv])
        rr_aux = rr
        rr += hrv

        # Si el nuevo rr se encuentra entre el minimo y el maximo posible en cuanto al objetivo de rr, se crea el latido
        if rr_target - fluctuation <= rr <= rr_target + fluctuation:
            beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma
            hrv_graph.append((start + time_beat_pos,abs(hrv)))
            bpm_value = int(60000 / time_beat_pos)
            bpm_grap.append((start + time_beat_pos, bpm_value))

            # Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
            if accumulated_time + rr > total_ecg_time:
                duracion_restante = total_ecg_time - accumulated_time
                beat = beat[:duracion_restante]  # Ajustar el último latido
                accumulated_time += duracion_restante
            else:
                accumulated_time += rr
                completed_beats += 1
            ecg_signal = np.concatenate((ecg_signal, beat))
            start = start + time_beat_pos
        else:
            rr = rr_aux

    x = np.arange(0, len(ecg_signal), 1)  # Tiempo en milisegundos
    bpm_x = np.arange(0,len(bpm_grap),1)
    hrv_x = np.arange(0,len(hrv_graph),1)


    movement_beats = completed_beats - (transition_beats + resting_beats)
    print("Latidos en moviemiento:", movement_beats)
    movement_time = accumulated_time


    return x, ecg_signal,completed_beats,resting_time,transition_time,movement_time,bpm_x,bpm_grap,hrv_x,hrv_graph,resting_beats,transition_beats,movement_beats

# Función encargada de pasar de ms a min
def ms_to_min(milisegundos):
    # MS --> S
    total_sec = milisegundos // 1000
    # MIM Y S
    min = total_sec // 60
    sec = total_sec % 60
    # Formato MM:SS
    return f"{min:02d}:{sec:02d}"

if __name__ == "__main__":
    print("1. Situación de estres 1 min")
    print("2. Situacion de movimiento (ejercicio intensivo)")
    print("3. Situación de reposo")
    opcion = input()
    if opcion == "1":
        # Obtención de los datos a mostrar
        x, y, lpm,resting,transition,movement,bpm_graph_x,bpm_graph_y,hrv_x,hrv_y,resting_beats,transition_beats,movement_beats = generate_ecg_one_minute_signal()
        print("Latidos totales:",lpm)

        data = pd.DataFrame({
            'Tiempo (ms)': x,
            'Voltaje (mV)': y
        })

        data.to_csv('ecg_signal.csv',index=False)

        # Mascaras para aplicar el color en el grafico
        resting_mask = np.arange(movement) < resting
        transition_mask = (np.arange(movement) >= resting) & (np.arange(movement) < transition)
        movement_mask = np.arange(movement) >= transition

        # Primer grafico (ECG)
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
        plt.xlim(0, 4)  # Zoom para los primeros 4 segundos
        plt.tight_layout()
        plt.grid(True)

        #Segundo grafico (lpm)
        plt.figure(figsize=(20,5))

        bpm_graph_x, bpm_graph_y = zip(*bpm_graph_y)  # Descomposicion de las tuplas
        bpm_graph_x = np.array(bpm_graph_x)
        bpm_graph_y = np.array(bpm_graph_y)
        plt.plot(bpm_graph_x / 1000, bpm_graph_y, marker='o', color='blue') #.scatter si solo se quieren los puntos y no las líneas

        #Representacion de los numeros en el gráfico
        for i in range(len(bpm_graph_x)):
            plt.text(bpm_graph_x[i] / 1000, bpm_graph_y[i], f'{bpm_graph_y[i]:.0f}', fontsize=8, ha='right', va='bottom')

        # Etiquetas con el formato MM:SS
        ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
        tick_labels = [ms_to_min(t * 1000) for t in ticks]
        plt.xticks(ticks, tick_labels)

        # Titulo y etiquetas para cada dimensión
        plt.title("LPM durante la simulacion")
        plt.xlabel("Tiempo (MM:SS)")
        plt.ylabel("Latidos por minuto (lpm)")
        plt.grid(True)

        # Tercer grafico (HRV)
        plt.figure(figsize=(20, 5))

        hrv_x, hrv_y = zip(*hrv_y)  # Descomposicion de las tuplas
        hrv_x = np.array(hrv_x)
        hrv_y = np.array(hrv_y)
        plt.plot(hrv_x / 1000, hrv_y, marker='o',
                 color='blue')  # .scatter si solo se quieren los puntos y no las lineas

        # Representacion de los numeros en el grafico
        for i in range(len(bpm_graph_x)):
            plt.text(hrv_x[i] / 1000, hrv_y[i], f'{hrv_y[i]:.0f}', fontsize=8, ha='right', va='bottom')

        # Etiquetas con el formato MM:SS
        ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
        tick_labels = [ms_to_min(t * 1000) for t in ticks]
        plt.xticks(ticks, tick_labels)

        # Titulo y etiquetas para cada dimensión
        plt.title("Variacion de HRV durante la simulacion")
        plt.xlabel("Tiempo (MM:SS)")
        plt.ylabel("HRV (ms)")
        plt.grid(True)

        acummulated_hrv = 0
        for i in range(resting_beats,len(hrv_y)):
            acummulated_hrv += hrv_y[i]

        average_hrv = int(acummulated_hrv/movement_beats)
        print("HRV medio:",average_hrv)

        plt.show()

    elif opcion == "2":
        total = 0

        total_ecg = []
        total_bpm = []
        bpm_min = []

        print("Selecciona los lpm medios")
        avgHR = input()

        hr_target = int(avgHR)
        hr_target = randint(hr_target - 5, hr_target)
        rr_target = int(60000 / hr_target)


        while total < 61:

            ecg_signal = np.array([])  # Array encargado de guardar los latidos
            bpm_grap = []  # Se guardan los lpm en ese tiempo x
            hrv_graph = []  # Se guardan el hrv en ese tiempo x

            hrv_min = 0
            hrv_max = 2
            fluctuation = 20

            accumulated_time = 0
            completed_beats = 0
            start = 0
            total_ecg_time = 60000

            if total % 3 == 0:
                # Se generan los latidos en movimiento de 1 min
                rr = rr_target
                while accumulated_time < total_ecg_time:
                    # Se escoge un valor aleatorio enter los máximos y los mínimos de hrv, también su signo
                    hrv = random.randrange(hrv_min, hrv_max,1)
                    hrv = choice([-hrv, hrv])
                    rr_aux = rr
                    rr += hrv

                    # Si el nuevo rr se encuentra entre el minimo y el maximo posible en cuanto al objetivo de rr, se crea el latido
                    if rr_target - fluctuation <= rr <= rr_target + fluctuation:
                        beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma
                        hrv_graph.append((start + time_beat_pos, abs(hrv)))
                        bpm_value = int(60000 / time_beat_pos)
                        bpm_grap.append((start + time_beat_pos, bpm_value))

                        # Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
                        if accumulated_time + rr > total_ecg_time:
                            duracion_restante = total_ecg_time - accumulated_time
                            beat = beat[:duracion_restante]  # Ajustar el último latido
                            accumulated_time += duracion_restante
                        else:
                            accumulated_time += rr
                            completed_beats += 1
                        ecg_signal = np.concatenate((ecg_signal, beat))
                        start = start + time_beat_pos
                    else:
                        rr = rr_aux

            else:
                while accumulated_time < total_ecg_time:

                    if random.random() < 0.25 and rr < rr_target + fluctuation+10:
                        hrv = 1
                    else:
                        hrv = 0

                    rr += hrv
                    beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_rr_based(rr)  # Se calcula un solo latido con el que se generara todo el electrocardiograma

                    bpm_value = int(60000 / time_beat_pos)
                    bpm_grap.append((start + time_beat_pos, bpm_value))

                    hrv_graph.append((start + time_beat_pos, hrv))

                    if accumulated_time + rr > total_ecg_time:
                        duracion_restante = total_ecg_time - accumulated_time
                        beat = beat[:duracion_restante]  # Ajustar el último latido
                        accumulated_time += duracion_restante
                    else:
                        accumulated_time += rr
                        completed_beats += 1
                    start = start + time_beat_pos
                    ecg_signal = np.concatenate((ecg_signal, beat))

            bpm_min.append(completed_beats + 1)
            x = np.arange(0, len(ecg_signal), 1)  # Tiempo en milisegundos
            bpm_x = np.arange(0, len(bpm_grap), 1)
            hrv_x = np.arange(0, len(hrv_graph), 1)

            total_ecg.append(ecg_signal)
            total_bpm.append(bpm_grap)

            total+=1

        bpm_min_x = np.arange(0,len(bpm_min),1)

        plt.figure(figsize=(20, 5))
        plt.plot(bpm_min_x, bpm_min, marker='o',
                    color='blue')  # .scatter si solo se quieren los puntos y no las líneas

        # Etiquetas con el formato MM:SS
        ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
        tick_labels = [ms_to_min(t * 1000 * 60) for t in ticks]
        plt.xticks(ticks, tick_labels)

        # Titulo y etiquetas para cada dimensión
        plt.title("LPM durante la simulacion")
        plt.xlabel("Tiempo (MM:SS)")
        plt.ylabel("Latidos por minuto (lpm) en 60 min")
        plt.grid(True)
        plt.xticks(rotation=45)

        while True:
            print("seleccione el minuto que quiere ver detalladamente")
            min = int(input())

            # Primer grafico (ECG)
            plt.figure(figsize=(20, 5))
            plt.plot(x / 1000, total_ecg[min])  # Fase de descanso

            # Etiquetas con el formato MM:SS
            ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
            tick_labels = [ms_to_min(t * 1000) for t in ticks]
            plt.xticks(ticks, tick_labels)
            plt.yticks(np.arange(-1, 1.1, 0.2))

            plt.grid(True, which='both', linestyle='--', linewidth=0.5)
            plt.minorticks_on()
            plt.gca().set_xticks(np.arange(0, 60.01, 0.04), minor=True)
            plt.gca().set_yticks(np.arange(-1, 1.1, 0.1), minor=True)


            # Titulo y etiquetas para cada dimensión
            plt.title("ECG Sintético de 1 Minuto")
            plt.xlabel("Tiempo (MM:SS)")
            plt.ylabel("Voltaje (mV)")
            plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            plt.xlim(0, 4)  # Zoom para los primeros 4 segundos
            plt.tight_layout()
            plt.grid(True)

            # Segundo grafico (lpm)
            plt.figure(figsize=(20, 5))

            bpm_graph_x, bpm_graph_y = zip(*total_bpm[min])  # Descomposicion de las tuplas
            bpm_graph_x = np.array(bpm_graph_x)
            bpm_graph_y = np.array(bpm_graph_y)
            plt.plot(bpm_graph_x / 1000, bpm_graph_y, marker='o',
                        color='blue')  # .scatter si solo se quieren los puntos y no las líneas

            # Representacion de los numeros en el gráfico
            for i in range(len(bpm_graph_x)):
                plt.text(bpm_graph_x[i] / 1000, bpm_graph_y[i], f'{bpm_graph_y[i]:.0f}', fontsize=8, ha='right',
                            va='bottom')

            # Etiquetas con el formato MM:SS
            ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
            tick_labels = [ms_to_min(t * 1000) for t in ticks]
            plt.xticks(ticks, tick_labels)

            # Titulo y etiquetas para cada dimensión
            plt.title("LPM durante la simulacion")
            plt.xlabel("Tiempo (MM:SS)")
            plt.ylabel("Latidos por minuto (lpm)")
            plt.grid(True)

            plt.show()

    elif opcion == '3':
        print("Cual es la frecuencia cardiaca que quieres que posea")
        lpm = int(input())
        rr = int((60/lpm)*1000)

        accumulated_time = 0
        start = 0
        total_ecg_time = 30000

        ecg_signal = np.array([])  # Array encargado de guardar los latidos
        first_beat, parcial, time_beat, r1 = generate_ecg_single_signal() # Se calcula un solo latido con el que se generara todo el electrocardiograma
        lpm_latido = int(60000 / time_beat)

        while lpm_latido != lpm:
            first_beat, parcial, time_beat, r1 = generate_ecg_single_signal()  # Se calcula un solo latido con el que se generara todo el electrocardiograma
            lpm_latido = int(60000 / time_beat)

        ecg_signal = np.concatenate((ecg_signal, first_beat))
        accumulated_time += parcial


        # Se generan los 10 primeros latidos en reposo
        while accumulated_time < total_ecg_time:
            beat, parcial_pos, time_beat_pos, r_pos = generate_ecg_single_signal()
            time_0 = rr - ((parcial - r1) + r_pos)
            if time_0 < 0:
                time_0 = 0
            flat_section = np.zeros(time_0)
            # Si el tiempo de latido calculado es igual al rr, se tiene en cuenta el latido
            if ((parcial - r1) + r_pos + time_0) == rr:
                flat_section = np.concatenate((flat_section, beat))
                bpm_value = int(60000 / (parcial + time_0))

                # Si se excede el tiempo del que se quiere el electro, se calcula la parte parcial a mostrar; sino se muestra el latido completo
                if accumulated_time + rr > total_ecg_time:
                    duracion_restante = total_ecg_time - accumulated_time
                    flat_section = flat_section[:duracion_restante]
                    accumulated_time += duracion_restante
                else:
                    accumulated_time += parcial_pos + time_0


                ecg_signal = np.concatenate((ecg_signal, flat_section))
                start = start + parcial + time_0
                parcial = parcial_pos
                r1 = r_pos

        x = np.arange(0, len(ecg_signal), 1)  # Tiempo en milisegundos


        # Primer grafico (ECG)
        plt.figure(figsize=(20, 5))
        plt.plot(x / 1000, ecg_signal)  # Fase de descanso

        # Etiquetas con el formato MM:SS
        ticks = np.arange(0, 61, 1)  # Etiquetas cada segundo, incluyendo 01:00(por eso se pone 61)
        tick_labels = [ms_to_min(t * 1000) for t in ticks]
        plt.xticks(ticks, tick_labels)
        plt.yticks(np.arange(-1, 1.1, 0.2))

        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.minorticks_on()
        plt.gca().set_xticks(np.arange(0, 60.01, 0.04), minor=True)
        plt.gca().set_yticks(np.arange(-1, 1.1, 0.1), minor=True)

        # Titulo y etiquetas para cada dimensión
        plt.title("ECG Sintético de 1 Minuto")
        plt.xlabel("Tiempo (MM:SS)")
        plt.ylabel("Voltaje (mV)")
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xlim(0, 4)  # Zoom para los primeros 4 segundos
        plt.tight_layout()
        plt.grid(True)

        plt.show()