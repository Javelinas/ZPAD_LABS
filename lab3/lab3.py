from spyre import server
import pandas as pd
    
class lab(server.App):
    title = "LAB3"

    inputs = [{"type": "dropdown",
                "label": "Індекс",
                "options": [{"label": "VCI", "value": "VCI"},
                            {"label": "TCI", "value": "TCI"},
                            {"label": "VHI", "value": "VHI"},],
                "key": "data_type",
                "action_id": "update_data"},
            {"type": "dropdown",
                "label": "Область",
                "options": [{"label": "Вінницька", "value": "1"},
                            {"label": "Волинська", "value": "2"},
                            {"label": "Дніпропетровська", "value": "3"},
                            {"label": "Донецька", "value": "4"},
                            {"label": "Житомирська", "value": "5"},
                            {"label": "Закарпатська", "value": "6"},
                            {"label": "Запорізька", "value": "7"},
                            {"label": "Івано-Франківська", "value": "8"},
                            {"label": "Київська", "value": "9"},
                            {"label": "Кіровоградська", "value": "10"},
                            {"label": "Луганська", "value": "11"},
                            {"label": "Львівська", "value": "12"},
                            {"label": "Миколаївська", "value": "13"},
                            {"label": "Одеська", "value": "14"},
                            {"label": "Полтавська", "value": "15"},
                            {"label": "Рівенська", "value": "16"},
                            {"label": "Сумська", "value": "17"},
                            {"label": "Тернопільська", "value": "18"},
                            {"label": "Харківська", "value": "19"},
                            {"label": "Херсонська", "value": "20"},
                            {"label": "Хмельницька", "value": "21"},
                            {"label": "Черкаська", "value": "22"},
                            {"label": "Чернівецька", "value": "23"},
                            {"label": "Чернігівська", "value": "24"},
                            {"label": "Крим", "value": "25"}],
                "key": "reg",
                "action_id": "update_data"},
            {"type": "text",
                "label": "Інтервал тижнів",
                "key": "weeks",
                "value": "1-10",
                "action_id": "update_data"},
            {"type": "text",
                "label": "Рік(1981-2024)",
                "value": "",
                "key": "year",
                "action_id": "update_data"}]
    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{"type": "plot", 
                "id": "plot", 
                "control_id": 
                "update_data", 
                "tab": "Plot"},
            {"type": "table",
                "id": "table_id",
                "control_id": "update_data",
                "tab": "Table",
                "on_page_load": True}]
    def getData(self, params):
        reg = params["reg"]
        weeks = params["weeks"]
        year = params["year"]
        df = pd.read_csv("/home/kali/Documents/Lab3/my_test.csv")
        df = df[df["Region_Index"] == int(reg)]
        start_week, end_week = map(int, weeks.split("-"))
        df = df[(df["Week"] >= start_week) & (df["Week"] <= end_week) & (df["Year"] == int(year))]
        return df


    def getPlot(self, params):
        df = self.getData(params)
        data_type = params["data_type"]
        plt_obj = df.plot(x="Week", y=data_type)
        fig = plt_obj.get_figure()
        return fig
    
if __name__ == "__main__":
    print('Done')
    app = lab()
    app.launch()
