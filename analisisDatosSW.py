import csv
import json
from datetime import datetime
from matplotlib import pyplot as plt

dataxDay = []

for _ in range(16):
    dataxDay.append([])

# Se cargan los datos del SW
with open('heartRate_DataWD.json', 'r', encoding='utf-8') as file:
    dataWD = json.load(file)


total_hr = []
# Se cargan los datos sintéticos
with open('HRmovimiento.csv', mode='r') as file:
    reader = csv.reader(file)
    for row in reader:
        total_hr.append(float(row[0]))

#Se obtienen las fechas y tiempos generales
i = 0
time_pre = datetime.strptime(dataWD[0]["startTime"], "%d-%m-%Y %H:%M:%S").date()

for j in dataWD:
    time_post = datetime.strptime(j["startTime"],"%d-%m-%Y %H:%M:%S").date()

    if time_pre == time_post:
        dataxDay[i].append(j)

    else:
        i+=1
        time_pre = time_post

total_bpm = []
total_time = []
total_day = []

#Se obtienen las frecuencias cardiacas y los tiempos de cada día
for i, day in enumerate(dataxDay):
    time = []
    bpm = []

    for j in day:
        time.append(datetime.strptime(j["startTime"], "%d-%m-%Y %H:%M:%S").strftime("%H:%M"))
        bpm.append(float(j["value"]))

    dayDisplayed = datetime.strptime(day[0]["startTime"], "%d-%m-%Y %H:%M:%S").strftime("%d-%m")
    total_day.append(dayDisplayed)
    total_bpm.append(bpm)
    total_time.append(time)

option = 1
interval = 1

#Se representan los datos eligiendo el día y el intervalo
while option != 0 and interval != 0:

    print("dime dia")
    option = int(input())

    if 0 < option < 17:

        print("dime intervalo de 60 min")
        interval = int(input())

        if interval != 0:
            plt.figure(figsize=(20, 5))
            plt.plot(total_time[option - 1], total_bpm[option - 1], marker="o", linestyle="-",
                     label="FC SmartWatch (lpm)",color="green")
            size = len(total_time[option - 1])
            if size >= 61 * interval:
                plt.plot(total_time[option-1][0+(61* (interval -1)): 61 * interval], total_hr, marker="o", linestyle="-", label="FC Sintético (lpm)")

            else:
                dif = 61 * interval - size
                long = len(total_time[option - 1][0 + (61 * (interval - 1)): size - dif])
                plt.plot(total_time[option - 1][0 + (61 * (interval - 1)): size - dif], total_hr[0:long], marker="o",
                         linestyle="-", label="FC Sintético (lpm)")

            plt.xlabel("Hora")
            plt.ylabel("Frecuencia cardiaca (LPM)")
            plt.title(f"Frecuencia cardiaca en movimiento - Día {total_day[option - 1]}")
            plt.xlim(60 * (interval - 1), 60 * interval)
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.legend()

            plt.show()

    elif option >= 17:
        while option >= 17:
            print("Día entre 1 y 16")
            option = int(input())



