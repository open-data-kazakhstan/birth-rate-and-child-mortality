import os
import pandas as pd
from datapackage import Package
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# путь к файлу Excel
input_directory = "C:\\Users\\admin\\Desktop\\birth_rate\\archive"
excel_file_path = os.path.join(input_directory, "birthrate.xlsx")

# считываем данные из файла Excel
df = pd.read_excel(excel_file_path)
# определяем и упаковываем ресурсы данных и их метаданные.
package = Package()

# определяем схему ресурса данных, указываем имена, типы и форматы полей (столбцов) данных.
schema = {
    "fields": [
        {"name": "Year", "type": "integer", "format": "default"},
        {"name": "Birthrate", "type": "number", "format": "default"},
        {"name": "Fatality", "type": "number", "format": "default"}
    ],
    "missingValues": [""]
}
# Определение ресурса, которое описывает данные, которые включены в пакет данных.
resource = {
    "path": "data/birthrate.csv",
    "profile": "tabular-data-resource",
    "name": "birthrate",
    "format": "csv",
    "mediatype": "text/csv",
    "encoding": "utf-8",
    "schema": schema,
}
# добавляем определение ресурса в пакет данных
package.add_resource(resource)

# определяем имя файла CSV, указываем полный путь, где его сохраним
csv_name_same_format = "birthrate.csv"
csv_path_same_format = "C:\\Users\\admin\\Desktop\\birth_rate\\Data\\birthrate.csv"
df.to_csv(csv_path_same_format, index=False)

# определим структуру пакета данных, которая включает информацию о данных и их ресурсах.
data_package = {
    "profile": "tabular-data-package",
    "resources": [
        {
            "path": "data/birthrate.csv",
            "profile": "tabular-data-resource",
            "name": "birthrate",
            "format": "csv",
            "mediatype": "text/csv",
            "encoding": "utf-8",
            "schema": {
                "fields": [
                    {
                        "name": "Year",
                        "type": "integer",
                        "format": "default"
                    },
                    {
                        "name": "Birthrate",
                        "type": "number",
                        "format": "default"
                    },
                    {
                        "name": "Fatality",
                        "type": "number",
                        "format": "default"
                    }
                ],
                "missingValues": [""]
            },
            "data": df.to_dict(orient="records")
        }
    ]
}
# новый Package экземпляр, включающий указанный ресурс
package = Package(data_package)

# определяем имя и полный путь к файлу JSON, сохраним пакет данных в виде файла JSON
json_filename = os.path.join("C:\\Users\\admin\\Desktop\\birth_rate\\Data\\datapackage.json")
package.save(json_filename)

# Анимированный сюжет с Matplotlib
fig, ax = plt.subplots() # создание новой фигуры ( fig) и соответствующих ей осей ( ax)
x_data = df['Year'] # переменная для хранения данных из DataFrame ( df).
y_data = df['Birthrate'] # переменная для хранения данных из DataFrame ( df).
fatality_column = df['Fatality'] # переменная для хранения данных из DataFrame ( df).
fatality_y_data = fatality_column
line, = ax.plot([], [], lw=4, label='Коэффициент рождаемости (на 1000 жен\n возрастом 15-19 лет)')
new_line_fatality, = ax.plot([], [], lw=4, color='red', label='Коэффициент женской смертности\n (на 100 000 живых детей)')
ax.set_xlim(min(x_data), 2024) # предел для оси x
ax.set_ylim(0, 60) # предел для оси у
ax.set_xlabel('Год') # метка оси
ax.set_ylabel('Индекс') # метка оси
ax.set_title('Уровень рождаемости и женской смертности') # заголовок графика
ax.legend(loc='upper left') # расположение легенды.

def animate(frame): # функция animate, которая обновляет данные для анимированных линий.
    line.set_data(x_data[:frame], y_data[:frame])
    new_line_fatality.set_data(x_data[:frame], fatality_y_data[:frame])
    return line, new_line_fatality
#  создает объект анимации и её параметры
ani = FuncAnimation(fig, animate, frames=len(x_data), blit=True, repeat=True, interval=1000)
# отображаем анимацию
plt.show()

# Сохранить анимацию в виде анимированного GIF-файла
gif_filename = os.path.join("C:\\Users\\admin\\Desktop\\birth_rate\\gif\\gifbirthrate.gif")
ani.save(gif_filename, writer='pillow', fps=1)
