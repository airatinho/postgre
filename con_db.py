import pandas as pd
from sqlalchemy import create_engine
import json


class Postgre_download_upload:
    def __init__(self,parent=None):
        __slots__=('switcher','path')
        print("Введите режи upload- загрузить таблицу \ndownload- скачать таблицу")
        self.switcher=input()
        print("Введите путь без имени самого файла")
        self.path=input()
        if self.switcher=='upload':
            self.create_table(path=self.path)
        elif self.switcher=='download':
            self.create_excel(path=self.path)
        else:
            print("Вы неправильно ввели режим или путь")

    def postgre_create_engine(self):
        try:
            config = json.load(open("config.json", encoding='utf-8'))
            return create_engine(
                f"{config['dbtype']}://{config['user']}:{config['password']}@{config['host']}/{config['database']}",
                echo=False
            )
        except:
            print("Не найден конфигурационный файл config.json !")

    def create_table(self,path):
        try:
            df=pd.read_excel(path + r"\basereport_test.xlsx")
            df[df['Сеансы'].isna() == False].reset_index(drop=True).to_sql('basereport_test', con=self.postgre_create_engine())
        except Exception:
            print("Не удалось создать таблицу")
    def create_excel(self,path):
        try:
            pd.read_sql("""select * from basereport_test""",con=self.postgre_create_engine()).to_excel(path+r"\basereport_test.xlsx")
        except Exception:
            print("Не удалось получить таблицу")

if __name__ == '__main__':
    Postgre_download_upload()