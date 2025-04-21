import cx_Oracle

class database:
    def __init__(self, username, password, host, port, service_name):
        dsn = cx_Oracle.makedsn(host, port, service_name=service_name)
        self.connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        self.cursor = self.connection.cursor()
        print("Database connection opened")

    def insert_data(self, table_name, data: dict):
        """
        Insert data in the given table
        :param table_name: table name
        :param data: Dictionary with column name as key and value as value
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join([f":{i+1}" for i in range(len(data))])
        values = list(data.values())
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            print(f"Daten inserted into {table_name}.")
        except cx_Oracle.DatabaseError as e:
            print(f"Error while inserting data: {e}")
            self.connection.rollback()

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Database connection closed")
