import urllib.request
from datetime import datetime
import os
import pandas as pd
def VHI_data(region_id, directory):
    
    # Словник для відображення старих індексів на нові назви областей
    region_ch = {
        1: '22',
        2: '24',
        3: '23',
        4: '25',
        5: '3',
        6: '4',
        7: '8',
        8: '19',
        9: '20',
        10: '21',
        11: '9',
        12: '9',
        13: '10',
        14: '11',
        15: '12',
        16: '13',
        17: '14',
        18: '15',
        19: '16',
        20: '25',
        21: '17',
        22: '18',
        23: '6',
        24: '1',
        25: '2',
        26: '7',
        27: '5'
    }

    
    url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2024&type=Mean'.format(region_id)
    
    # Відкриття веб-сторінки та отримання тексту
    wp = urllib.request.urlopen(url)
    text = wp.read()
    
    # Форматування дати та часу для назви файлу
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    
    directory = '/home/kali/Documents/Lab3/TOP'
    # Створення папки, якщо вона не існує
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Заміна індексу області на назву за словником
    region_name = region_ch.get(region_id)
    
    # Збереження файлу з датою та часом завантаження та ім'ям області
    filename = os.path.join(directory, 'VHI_{}_{}.csv'.format(region_name, date_time))
    with open(filename, 'wb') as file:
        file.write(text)
def clear():      
    directory = '/home/kali/Documents/Lab3/TOP'
    if os.path.exists(directory):
# Отримуємо список файлів у директорії
        files = os.listdir(directory)

# Проходимо по кожному файлу та видаляємо його
        for file in files:
            os.remove(os.path.join(directory, file))
    else:
        print('Перший запуск')  
clear()         

def files_to_dataframe(directory_path, output_path):
    # Визначив назви колонок та створив порожій DataFrame
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'Region_Index', 'empty']
    dataframe = pd.DataFrame(columns=headers)

    # Проходжу по всіх CSV-файлах у заданій директорії
    for file_name in os.listdir(directory_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(directory_path, file_name)
            try:
                # Зчитую дані з CSV-файлу пропускаючи перші два рядки та вказуючи назви колонок
                # Також прибрав табличні теги за допомогою str.replace
                df = pd.read_csv(file_path, skiprows=2, names=headers[:-1])
                df['Year'] = df['Year'].str.replace('<tt><pre>', '').str.replace('</pre></tt>', '')
                df = df.drop(df.loc[df['VHI'] == -1].index)
               
                #df = df.drop('empty', axis='columns')
                # Визначив індекс регіону з імені файлу та додав його до DataFrame
                region_index = int(file_name.split('_')[1])
                df['Region_Index'] = region_index

                # Об'єднав DataFrame кожного файлу з загальним DataFrame
                dataframe = pd.concat([dataframe, df], ignore_index=True)
                print(f'Successfully read file: {file_name}')
                
            except pd.errors.ParserError:
                print(f'Error reading {file_name}: ParserError')
    dataframe = dataframe.drop('empty', axis='columns')
    dataframe = dataframe.dropna()
    dataframe.to_csv(output_path, index=False)
    print(f'DataFrame saved to: {output_path}')
    print(dataframe.isnull().sum())
    
    print(dataframe)
    return dataframe
    



for i in range(1, 28):
    VHI_data(i, 'TOP')
print("end")
files_to_dataframe('/home/kali/Documents/Lab3/TOP/', '/home/kali/Documents/Lab3/my_test.csv')