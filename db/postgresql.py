import psycopg2
from configs import config


class PostgresqlConnector():
    def __init__(self):
        # Construct connection string
        connString = "host={0} user={1} dbname={2} password={3}".format(
            config.POSTGRESQL_URL, config.POSTGRESQL_DB_USER, config.POSTGRESQL_DB_NAME, config.POSTGRESQL_DB_PASSWORD)
        # Connect to the PostgreSQL database server
        self.conn = psycopg2.connect(connString)
        print("Connect to the PostgreSQL database server successfully")

        self.cur = self.conn.cursor()
        # cur.execute('''CREATE TABLE COMPANY
        #     (ID INT PRIMARY KEY     NOT NULL,
        #     NAME           TEXT    NOT NULL,
        #     AGE            INT     NOT NULL,
        #     ADDRESS        CHAR(50),
        #     SALARY         REAL);''')
        # print("Table created successfully")

        # conn.commit()
        # conn.close()
