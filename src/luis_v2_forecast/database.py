import psycopg2

class database:
    def __init__(self, username: object, password: object, host: object, port: object, dbname: object) -> None:
        self.connection = psycopg2.connect(
            user=username,
            password=password,
            host=host,
            port=port,
            dbname=dbname
        )
        self.cursor = self.connection.cursor()
        print("Database connection opened")

    def insert_data(self, table_name, data: dict):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        values = list(data.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders}) ON CONFLICT DO NOTHING"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
        except psycopg2.DatabaseError as e:
            print(f"Insert error: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed")