import unittest
import pandas as pd
from sqlalchemy import create_engine
import json
config = json.load(open("config.json", encoding='utf-8'))

class MyTestCase(unittest.TestCase):
    def test_something(self):
        engine = create_engine(
            f"{config['dbtype']}://{config['user']}:{config['password']}@{config['host']}/{config['database']}",
            echo=False
            )
        df = pd.read_excel('basereport_test.xlsx')
        new_df = df[df['Сеансы'].isna() == False].reset_index(drop=True)
        df_from_db = pd.read_sql("""select * from basereport_test""", engine)
        for i in new_df.columns:
            assert new_df[i].dropna().to_list() == df_from_db[i].dropna().to_list()


if __name__ == '__main__':
    unittest.main()
