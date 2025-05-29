import json
import glob
from datetime import datetime, timezone

allData = []
heartRateData = []

jsonFiles = glob.glob("Health detail data & description/*.json")

# Se extraen aquellos datos que solo son de la frecuencia cardiaca
for file in jsonFiles:
    with open(file,'r',encoding='utf-8') as f:
        data = json.load(f)
        allData.extend(data)
        for i in data:
            if i["type"] == 7:
                heartRateData.extend(i["samplePoints"])

#Se pasan todos los valores de fecha al formato Y/M/D H/M/S
for i in heartRateData:

    startTime = i["startTime"]
    endTime = i["endTime"]

    startTimeNew = datetime.fromtimestamp(startTime / 1000, tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')
    endTimeNew = datetime.fromtimestamp(endTime / 1000, tz=timezone.utc).strftime('%d-%m-%Y %H:%M:%S')

    i["startTime"] = startTimeNew
    i["endTime"] = endTimeNew


with open('heartRate_DataRaw.json','w',encoding='utf-8') as file:
    json.dump(heartRateData, file, indent=4, ensure_ascii=False)


#Se carga el archivo con los datos extraidos
with open("heartRate_DataRaw.json", "r", encoding="utf-8") as file:
    info = json.load(file)


#Se eliminan los datos duplicados pasando de diccionario a tuplas
dataWD = list({tuple(i.items()) for i in info})

#Se vuelven a convertir al estado original (diccionario)
cleanData = [dict(t) for t in dataWD]

#Se ordenan los datos de más antiguos a más nuevos
sortedData = sorted(cleanData, key=lambda x: datetime.strptime(x["startTime"], "%d-%m-%Y %H:%M:%S"))

#Se guardan en un nuevo json
with open("heartRate_DataWD.json", "w", encoding="utf-8") as file:
    json.dump(sortedData, file, indent=4, ensure_ascii=False)



