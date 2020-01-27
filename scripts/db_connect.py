import psycopg2


class PsqlManager:
    """ Class with basic funtions to access and modify databases from python """
    def __init__(self, ip, port, dbname, user, password):
        self.ip, self.port, self.dbname, self.user, self.password = ip, port, dbname, user, password

    def get_connection(self):
        conn = psycopg2.connect(host=self.ip, port=self.port,
                                database=self.dbname, user=self.user, password=self.password)
        self._conn = conn
        # print(conn.get_dsn_parameters())
        print("******* CONNECTED ******** \n")

    def close_connection(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.commit()
            self._conn.close()
        print("******* DISCONNECTED ******* \n")

    def get_cursor(self):
        if self._conn and (not hasattr(self, '_cursor') or not self._cursor or self._cursor.closed):
                self._cursor = self._conn.cursor()

    def select_table(self, table_name):
        self.get_cursor()
        self._cursor.execute("""SELECT * FROM {}""".format(table_name))
        result = self._cursor.fetchone()
        print('Record is : ', result, '\n')

    def create_table(self, table_name, data):
        self.get_cursor()
        data_definition = ', '.join(list(' '.join(list(i)) for i in data))
        sql = ("""CREATE TABLE "{}" ({})""".format(table_name, data_definition))
        self._cursor.execute(sql)

    def inherit_table(self, table_name, data, inherit_table):
        self.get_cursor()
        data_definition = ', '.join(list(' '.join(list(i)) for i in data))
        sql = ("""CREATE TABLE "{}" ({}) INHERITS ("{}")""".format(table_name, data_definition, inherit_table))
        self._cursor.execute(sql)

    def rename_table(self, old_name, new_name):
        self.get_cursor()
        self._cursor.execute("""ALTER TABLE "{}" RENAME TO "{}";""".format(old_name, new_name))

    def drop_table(self, table_name):
        self.get_cursor()
        self._cursor.execute("""DROP TABLE "{}";""".format(table_name))

    def add_column(self, table_name, data):
        self.get_cursor()
        self._cursor.execute("""ALTER TABLE "{}" ADD COLUMN "{}" {};""".format(table_name, data[0], data[1]))

    def drop_column(self, table_name, column):
        self.get_cursor()
        self._cursor.execute("""ALTER TABLE "{}" DROP COLUMN "{}" CASCADE;""".format(table_name, column))

    def insert_records(self, table_name, columns, records):
        self.get_cursor()
        columns = ', '.join(columns)
        records = ', '.join(list(str(i) for i in records))
        print(records)
        sql = ("""INSERT INTO {} ({}) VALUES {};""".format(table_name, columns, records))
        self._cursor.execute(sql)


# if __name__ == '__main__':
#     psql_manager = PsqlManager('localhost', '5432', 'dbweb', 'reymon', 'reymon')
#     psql_manager.get_connection()
#     # EXAMPLES
#     psql_manager.drop_table('res_user_test')
#     data = [('id', 'serial'),
#             ('name', 'text'),
#             ('expectation', 'numeric', 'default', '5', 'check', '(expectation > 0 AND expectation < 10)')]
#     psql_manager.create_table('res_user_test', data)
#     psql_manager.add_column('res_user_test', ('age', 'integer'))
#     columns = ['name', 'expectation', 'age']
#     records = [('Ramon', 0.95, 25),
#                ('Empresa', 0.67, 4)]
#     psql_manager.insert_records('res_user_test', columns, records)
#     psql_manager.select_table('res_user_test')
#     # IMPORTANT
#     psql_manager.close_connection()
