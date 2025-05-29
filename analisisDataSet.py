import pandas as pd
from matplotlib import pyplot as plt

if __name__ == "__main__":

    #Se extrae la información del archivo
    dataFile = pd.read_csv('merged_data.csv', low_memory=False)

    # Se obtienen solo las columnas que importan
    data = dataFile[['id', 'EDA', 'HR', 'TEMP']]

    #Se agrupa por ID
    grouped_data = data.groupby('id').describe()

    #Configuración
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    #Se muestra por consola información útil
    print(grouped_data)

    # Se filtra el dataframe por id
    for subject_id in dataFile['id'].unique():
        data_subset = dataFile[dataFile['id'] == subject_id]

        #Se junta en un solo gráfico las tres variables para ver así su relación
        plt.figure(figsize=(14, 9))

        # 1. Gráfico del EDA
        plt.subplot(3, 1, 1)
        plt.plot(data_subset['EDA'], color='blue', label='EDA')
        plt.title(f'EDA para ID {subject_id}')
        plt.ylabel('EDA')
        plt.legend()

        # 2. Gráfico del HR
        plt.subplot(3, 1, 2)
        plt.plot(data_subset['HR'], color='red', label='HR')
        plt.title(f'HR para ID {subject_id}')
        plt.ylabel('Heart Rate (HR)')
        plt.legend()

        # Gráfico de TEMP
        plt.subplot(3, 1, 3)
        plt.plot(data_subset['TEMP'], color='green', label='TEMP')
        plt.title(f'TEMP para ID {subject_id}')
        plt.ylabel('Temperature')
        plt.legend()

        plt.tight_layout()
        plt.show()


