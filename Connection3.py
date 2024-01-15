import mysql.connector
from sqlalchemy import create_engine
import pandas as pd

def create_sqlalchemy_conn_string(config):
    user = config.get('user', 'root')
    password = config.get('password', '')
    host = config.get('host', '127.0.0.1')
    database = config.get('database', '')
    port = config.get('port', '3306')
    return f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}'

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.conn = None
        self.sqlalchemy_conn_string = create_sqlalchemy_conn_string(config)

    def open_connection(self):
        try:
            self.conn = mysql.connector.connect(**self.config)
            if self.conn.is_connected():
                print("Connection successful")
            else:
                print("Connection failed")
        except mysql.connector.Error as err:
            print("An error occurred: {}".format(err))
        except Exception as e:
            print("An unexpected error occurred: {}".format(e))

    def close_connection(self):
        if self.conn is not None and self.conn.is_connected():
            self.conn.close()

    def query(self, sql):
        engine = create_engine(self.sqlalchemy_conn_string)
        df = pd.read_sql_query(sql, engine)
        return df

# Uso da classe
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'filmes_ep_db2',
    'port': '3306',
    'auth_plugin': 'mysql_native_password',
    'raise_on_warnings': True
}

